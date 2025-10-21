from odoo import models, fields, api, _


class CrmCommission(models.Model):
    _name = 'crm.commission'

    product_line_ids = fields.One2many('product.line','crm_commission_id')
    name = fields.Char(string="Name", required=True)
    active = fields.Boolean(string='Active')
    from_date = fields.Datetime(string="From Date")
    to_date = fields.Datetime(string="To Date")
    type = fields.Selection([('product_wise', 'Product Wise'),('revenue_wise', 'Revenue Wise')])
    product = fields.Many2one('product.product', string="Product")

    def _get_sale_person(self):
        users_search = self.env['res.users'].search([])
        users = []
        for user in users_search:
            if user.has_group('sales_team.group_sale_salesman'):
                users.append(user.id)
        return [('id', 'in', users)]

    sale_person = fields.Many2one('res.users', domain=_get_sale_person)

