from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    customer_top_lines_ids = fields.One2many('account.move.line','move_id',
        string='Customer Top Invoice Lines')

    @api.depends('partner_id')
    def _compute_customer_top_lines(self):
        MoveLine = self.env['account.move.line']

        for move in self:
            invoice_lines = MoveLine.search([
                ('move_id.move_type', 'in', ('out_invoice', 'out_refund')),
                ('move_id.partner_id', '=', move.partner_id.id),
                ('move_id.state', '=', 'posted'),
                ('product_id', '!=', False),
            ], order='price_unit desc')

            unique_lines = {}
            for line in invoice_lines:
                if line.product_id.id not in unique_lines:
                    unique_lines[line.product_id.id] = line
                if len(unique_lines) >= 20:
                    break

            move.customer_top_lines_ids = list(unique_lines.values())

    def button_to_add_invoice_lines(self):
        print('hai')
