from odoo import models, fields, api, Command


class AccountMove(models.Model):
    _inherit = 'account.move'

    related_so_ids = fields.Many2many('sale.order', 'account_move_related_so_rel', 'move_id',
                                      'related_so_id', string="Related SO")
    invoice_line_ids = fields.One2many('account.move.line', 'move_id', string="Invoice Lines")

    @api.onchange('related_so_ids')
    def _onchange_related_so_ids(self):
        self.invoice_line_ids = [Command.clear()]
        if self.related_so_ids:
            invoice_line = self.related_so_ids.mapped('order_line')
            for line in invoice_line:
                invoice_lines = [
                    Command.create({
                        'product_id': line.product_id.id,
                        'quantity': line.product_uom_qty,
                        'price_unit': line.price_unit,
                    })
                ]
                self.invoice_line_ids = invoice_lines
