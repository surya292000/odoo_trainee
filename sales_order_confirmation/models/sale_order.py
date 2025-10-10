from odoo import models, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        super().action_confirm()
        total_amount = float(self.env['ir.config_parameter'].sudo().get_param('sale_order_configuration.max_amount'))
        if not self.env.user.has_group('sales_team.group_sale_manager') and self.amount_total > total_amount:
            raise ValidationError(_("At total amount should be less than (%s)",total_amount))
