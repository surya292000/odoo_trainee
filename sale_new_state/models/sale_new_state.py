from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    new_state = fields.Selection([
        ('open', 'Open'),
        ('close', 'Close'),
    ], string="Delivery Status", default='open', tracking=True, compute="_compute_new_state", inverse="_inverse_new_state")

    def _compute_new_state(self):
        for order in self:
            qty_ordered_sum = sum(self.order_line.mapped('product_uom_qty'))
            qty_delivered_sum = sum(self.order_line.mapped('qty_delivered'))
            if qty_ordered_sum == qty_delivered_sum:
                order.new_state = 'close'
            elif qty_delivered_sum == 0:
                order.new_state = 'open'
            else:
                order.new_state = 'open' or 'close'

    def _inverse_new_state(self):
        for order in self:
            qty_ordered_sum = sum(self.order_line.mapped('product_uom_qty'))
            qty_delivered_sum = sum(self.order_line.mapped('qty_delivered'))
            if order.new_state == 'close' and qty_delivered_sum == 0:
                order.new_state = 'open'
            elif qty_ordered_sum == qty_delivered_sum:
                order.new_state = 'close'
