# -*- coding: utf-8 -*-
from dateutil.utils import today
from odoo import fields, models, Command
from odoo.exceptions import UserError


class MaterialRequest(models.Model):
    _name = "material.request"
    _description = "Material Request"

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
    internal_ids = fields.Many2many('stock.picking', copy=False)
    company_id = fields.Many2one("res.company", string="Company")

    def _compute_po_count(self):
        self.po_count = self.env['purchase.order'].search_count([('id', 'in', self.po_ids.ids)])

    def action_do_draft(self):
        self.states = 'draft'

    def action_do_submit(self):
        self.states = 'submit'

    def action_do_approve_by_manager(self):
        self.states = "approved_by_manager"

    # noinspection PyUnresolvedReferences
    def action_do_approve_by_head(self):
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
                    ('state', '=', 'draft'), ('product_id', '=', line.component_id.id)
                ], )
                if purchase:
                    po_line = purchase.order_line.filtered(lambda lin: lin.product_id.id == line.component_id.id)
                    if po_line:
                        po_line.write({'product_qty': line.quantity})
                    self.write({'po_ids': [fields.Command.link(purchase.id)]})
                else:
                    purchase = self.env['purchase.order'].create([{
                        'partner_id': vendor.id,
                        'order_line': [fields.Command.create({
                            'product_id': line.component_id.id,
                            'product_qty': line.quantity
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
                })]
            }])
            self.write({'internal_ids': [fields.Command.link(internal.id)]})
        if self.states != "approved_by_manager":
            raise UserError("You can only approve as Head when Manager has already approved.")
        self.states = "approved_by_head"

            # if purchase:
            #     return {
            #         "type": 'ir.actions.act_window',
            #         'res_model': 'purchase.order',
            #         "view_mode": 'list,form',
            #         'res_id': purchase.id,
            #     }

    def action_to_view_po(self):
        return {
            "type": 'ir.actions.act_window',
            'res_model': 'purchase.order',
            'view_mode': 'list,form',
            'domain': [('id', 'in', self.po_ids.ids)],
            'context': {'create': False},
        }

    def action_do_reject(self):
        self.states = "rejected"
