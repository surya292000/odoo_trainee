# -*- coding: utf-8 -*-
from dateutil.utils import today

from odoo import fields, models, Command


class ProductionProduction(models.Model):
    _name = "production.production"
    _description = "Production"

    product_ids = fields.One2many("production.product.lines","production_product_id", string="Product")
    employee_id = fields.Many2one("res.partner", string="Requested Employee", required=True)
    date_needed = fields.Datetime(string="Date Needed", required=True)
    today = fields.Datetime.now()
    states = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submit'),
        ('approved_by_manager', 'Approved By Manager'),
        ('approved_by_head', 'Approved By Head'),
        ('rejected', 'Rejected'),
    ],default="draft", required=True, tracking=True)
    company_id = fields.Many2one("res.company", string="Company")

    def action_do_draft(self):
        self.states = 'draft'

    def action_do_submit(self):
        self.states = 'submit'

    def action_do_approve_by_manager(self):
        self.states = "approved_by_manager"

    def action_do_approve_by_head(self):
        if self.states == "approved_by_manager":
            self.states = "approved_by_head"
            for line in self.product_ids:

                create_rfq = self.env['purchase.order'].create({
                    'partner_id' : line.vendors_ids,
                    'date_order' : self.today,
                    'date_planned' : self.date_needed,
                    
                })

        else:
            ValueError('order not approved by manager')

    def action_do_reject(self):
        self.states = "rejected"

