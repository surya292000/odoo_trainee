from odoo import models, fields, api, Command

class AccountMove(models.Model):
    _inherit = 'account.move'

    related_so_ids = fields.Many2many('sale.order', 'account_move_related_so_rel','move_id',
        'related_so_id',string="Related SO")

    @api.onchange('related_so_ids')
    def _onchange_related_so_ids(self):
        invoice_line_ids = []
        if self.related_so_ids:
            for order in self.related_so_ids:
                for line in order.order_line:
                    invoice_line_ids.append(
                        fields.Command.create({
                            'product_id': line.product_id.id,
                            'quantity': line.product_uom_qty,
                            'price_unit': line.price_unit
                        })
                    )
                self.invoice_line_ids = invoice_line_ids
