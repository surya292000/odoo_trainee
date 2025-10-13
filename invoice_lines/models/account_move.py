from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    customer_top_lines_ids = fields.Many2many('account.move.line',string='Customer Top 20 Invoice Lines',
        compute='_compute_customer_top_lines',store=False)

    @api.depends('partner_id', 'invoice_line_ids')
    def _compute_customer_top_lines(self):
        MoveLine = self.env['account.move.line']
        for move in self:
            if not move.partner_id:
                move.customer_top_lines_ids = False
                continue

            invoice_lines = MoveLine.search([
                ('move_id.move_type', 'in', ('out_invoice', 'out_refund')),
                ('move_id.partner_id', '=', move.partner_id.id),
                ('move_id.state', '=', 'posted'),
                ('product_id', '!=', False),
                ('price_unit', '>', 0),
            ], order='price_unit desc', limit=20)

            existing_products = move.invoice_line_ids.mapped('product_id').ids
            filtered_lines = invoice_lines.filtered(lambda l: l.product_id.id not in existing_products)

            move.customer_top_lines_ids = filtered_lines

    def action_add_all_top_lines(self):
        """Add all 20 top lines to the current draft invoice and remove from the list."""
        self.ensure_one()

        # if self.state != 'draft':
        #     raise ValueError("You can only add lines to a draft invoice.")

        new_lines = []
        for top_line in self.customer_top_lines_ids:
            new_lines.append((0, 0, {
                'product_id': top_line.product_id.id,
                'name': top_line.name or top_line.product_id.display_name,
                'quantity': top_line.quantity,
                'price_unit': top_line.price_unit,
                'tax_ids': [(6, 0, top_line.tax_ids.ids)],
            }))

        self.write({'invoice_line_ids': new_lines})
        self._compute_customer_top_lines()

        return {'type': 'ir.actions.client', 'tag': 'reload'}
