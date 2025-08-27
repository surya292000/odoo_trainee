# -*- coding: utf-8 -*-
from dateutil.utils import today
from odoo import api, fields, models, Command, _
from odoo.exceptions import UserError


class MaterialRequest(models.Model):
    _name = "material.request"
    _description = "Material Request"

    name = fields.Char(string='reference', readonly="1")
    material_line_ids = fields.One2many("material.request.lines", "request_id", string="request Lines")
    employee_id = fields.Many2one("res.partner", string="Requested Employee", required=True)
    date_needed = fields.Datetime(string="Date Needed", required=True)
    today = fields.Date(default=today())
    states = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submit'),
        ('approved_by_manager', 'Approved By Manager'),
        ('approved_by_head', 'Approved By Head'),
        ('rejected', 'Rejected'),
    ], default="draft", required=True, tracking=True)
    po_count = fields.Integer(string="PO count", compute="_compute_po_count")
    po_ids = fields.Many2many(
        'purchase.order',
        string="Purchase Orders"
    )
    int_ids = fields.Many2many("stock.picking",string="Internal Transfers", copy=False)
    int_count = fields.Integer(string="Int count", compute="_compute_int_count")
    company_id = fields.Many2one("res.company", string="Company")

    def _compute_po_count(self):
        """compute function for purchase order count"""
        self.po_count = self.env['purchase.order'].search_count([('id', 'in', self.po_ids.ids)])

    def _compute_int_count(self):
        """compute function for internal transfer count"""
        self.int_count = self.env['stock.picking'].search_count([('id', 'in', self.int_ids.ids)])

    @api.model
    def create(self, vals):
        """generating unique sequence number"""
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('material.request.ref') or _('New')
        return super(MaterialRequest, self).create(vals)

    def action_do_draft(self):
        """action button for draft"""
        self.states = 'draft'

    def action_do_submit(self):
        """action button for submit"""
        self.states = 'submit'

    def action_do_approve_by_manager(self):
        """action for approve button by manager"""
        self.states = "approved_by_manager"

    # noinspection PyUnresolvedReferences
    def action_do_approve_by_head(self):
        """action for approve button by head"""
        po_list = self.material_line_ids.filtered(lambda rec: rec.request_type == 'purchase_order')
        internal_trans_list = self.material_line_ids.filtered(lambda rec: rec.request_type == 'internal_transfer')
        picking_types = self.env['stock.picking.type'].search([
            ('code', '=', 'internal'),
            ('company_id', '=', self.env.company.id),
        ])
        for line in po_list:
            for vendor in line.vendor_ids:
                purchase = self.env['purchase.order'].search([
                    ('partner_id', '=', vendor.id),
                    ('state', '=', 'draft')
                ], limit=1)
                if purchase:
                    existing_product_ids = set(purchase.order_line.mapped('product_id').ids)
                    if line.component_id.id in existing_product_ids:
                        for lin in purchase.order_line:
                            if lin.product_id.id == line.component_id.id:
                                lin.product_qty += line.quantity
                                break
                    else:
                        purchase.write({
                            'order_line': [fields.Command.create({
                                'product_id': line.component_id.id,
                                'product_qty': line.quantity,
                            })]
                        })
                    self.write({'po_ids': [fields.Command.link(purchase.id)]})
                else:
                    purchase = self.env['purchase.order'].create([{
                        'partner_id': vendor.id,
                        'order_line': [fields.Command.create({
                            'product_id': line.component_id.id,
                            'product_qty': line.quantity,
                        })]
                    }])
                    self.write({'po_ids': [fields.Command.link(purchase.id)]})

        for line in internal_trans_list:
            internal = self.env['stock.picking'].create([{
                'location_id': line.src_location_id.id,
                'location_dest_id': line.dest_location_id.id,
                'picking_type_id': picking_types[:1].id,
                'move_ids': [fields.Command.create({
                    'name': line.component_id.name,
                    'product_id': line.component_id.id,
                    'location_id': line.src_location_id.id,
                    'location_dest_id': line.dest_location_id.id,
                    'product_uom_qty' : line.quantity,
                })]
            }])
            self.write({'int_ids': [fields.Command.link(internal.id)]})
        if self.states != "approved_by_manager":
            raise UserError("You can only approve as Head when Manager has already approved.")
        self.states = "approved_by_head"

    def action_to_view_po(self):
        """action view for purchase order"""
        return {
            "type": 'ir.actions.act_window',
            'res_model': 'purchase.order',
            'view_mode': 'list,form',
            'domain': [('id', 'in', self.po_ids.ids)],
            'context': {'create': False},
        }

    def action_to_view_int(self):
        """action view for internal transfer"""
        return {
            "type": 'ir.actions.act_window',
            'res_model': 'stock.picking',
            'view_mode': 'list,form',
            'domain': [('id', 'in', self.int_ids.ids)],
            'context': {'create': False},
        }

    def action_do_reject(self):
        """action button for rejection"""
        self.states = "rejected"
