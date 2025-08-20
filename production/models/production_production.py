# -*- coding: utf-8 -*-
from dateutil.utils import today
from odoo import fields, models, Command


class ProductionProduction(models.Model):
    _name = "production.production"
    _description = "Production"

    name = fields.Char(string="Reference", required=True, copy=False, default="New")
    product_line_ids = fields.One2many("production.product.lines","production_id", string="Product Lines")
    employee_id = fields.Many2one("res.partner", string="Requested Employee", required=True)
    date_needed = fields.Datetime(string="Date Needed", required=True)
    today = fields.Date(default=today())
    states = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submit'),
        ('approved_by_manager', 'Approved By Manager'),
        ('approved_by_head', 'Approved By Head'),
        ('rejected', 'Rejected'),
    ],default="draft", required=True, tracking=True)
    # po_ids = fields.Many2many('purchase.order', copy=False)
    po_count = fields.Integer(string="PO count", compute="_compute_po_count")
    po_ids = fields.Many2many(
        'purchase.order',
        'production_purchase_rel',   # relation table
        'production_id',
        'purchase_id',
        string="Purchase Orders"
    )
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
        po_list = self.product_line_ids.filtered(lambda rec: rec.request_type == 'purchase_order')
        for line in po_list:
            for vendor in line.vendor_ids:
                print(vendor, 'vendor')
                purchase = self.env['purchase.order'].search([
                    ('partner_id', '=', vendor.id),
                    ('state', '=', 'draft')
                ], limit=1)
                print(purchase, 'purchase')
                if purchase:
                    po_line = self.env['product.template'].search(['name', '=', line.component_id.name])
                    # po_line = purchase.order_line.filtered(lambda lin: lin.product_id == line.component_id)
                    po_line.write({'order_line.quantity': line.quantity})
                    # print(order_line.product_qty, 'sdfghjkl')
                    print(line.quantity, 'quantity')
                    print('sdfghj')
                    self.write({'po_ids': [fields.Command.link(purchase.id)]})
                else:
                    purchase = self.env['purchase.order'].create([{
                        'partner_id': vendor.id,
                        'order_line': [fields.Command.create({
                            'product_id': line.component_id.id,
                            'product_qty' : line.quantity
                        })]
                    }])
                    # print(purchase.id, 'purchase id')
                self.write({'po_ids': [fields.Command.link(purchase.id)]})

            if self.states == "approved_by_manager":
                self.states = "approved_by_head"
            if purchase:
                return {
                    "type": 'ir.actions.act_window',
                    'res_model': 'purchase.order',
                    "view_mode": 'list,form',
                    'res_id': purchase.id,
                }
    #
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
