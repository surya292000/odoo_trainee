from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'purchase.order'

    restrict = fields.Boolean(related='partner_id.restricted',string="Restricted",store=True)
    count = fields.Integer(related='partner_id.count', string='Count')

    @api.constrains('order_line', 'count')
    def _check_order_lines_count(self):
        for order in self:
            if len(self.order_line) > self.count:
                print(len(self.order_line))
                raise ValidationError(
                    _("The number of order lines for this partner cannot exceed %s.") % (order.count,))
