from odoo import models, fields, api, _


class CrmCommission(models.Model):
    _name = 'crm.commission'

    name = fields.Char(string="Name")
    active = fields.Boolean(string='Active')
    from_date = fields.Datetime(string="From Date")
    to_date = fields.Datetime(string="To Date")
    type = fields.Selection([('product_wise', 'Product Wise'),('revenue_wise', 'Revenue Wise')])
