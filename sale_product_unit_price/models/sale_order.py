from odoo import models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        product = self.order_line.filtered(lambda line: line.product_id.list_price < line.product_id.standard_price
                                                        + ((15/100)*line.product_id.standard_price))
        if len(product) > 0:
            raise ValidationError(f'Cannot confirm order. Some items are sold below allowed margin."')
        super(SaleOrder, self).action_confirm()
