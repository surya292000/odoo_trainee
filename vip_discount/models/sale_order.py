from odoo import models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('partner_id', 'order_line')
    def _onchange_partner_id(self):
        if self.partner_id.is_vip:
            for line in self.order_line:
                line.write({'discount': self.partner_id.vip_discount})
