from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order.line'

    def automatic_discount(self):
        print('hai')
