from odoo import models, Command

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    def button_to_add_invoice_lines(self):
        """Add this top line into the current draft invoice."""
        self.ensure_one()

        active_id = self.env.context.get('active_id')
        if not active_id:
            raise ValueError("No active_id found in context. Make sure the context includes 'active_id'.")

        move = self.env['account.move'].browse(active_id)
        if not move.exists():
            raise ValueError(f"Invoice with ID {active_id} not found.")
        if move.state != 'draft':
            raise ValueError("You can only add lines to a draft invoice.")

        # Create a new invoice line in the current move
        self.env['account.move.line'].create({
            'move_id': move.id,
            'product_id': self.product_id.id,
            'name': self.name or self.product_id.display_name,
            'quantity': self.quantity,
            'price_unit': self.price_unit,
            'tax_ids': [Command.set(self.tax_ids.ids)],
        })

        # No need to manually recompute in Odoo 18 — it's automatic
        move.invalidate_recordset()  # Ensures UI refresh

        return {'type': 'ir.actions.client', 'tag': 'reload'}

    # def action_add_all_top_lines(self):
    #     """Add all 20 top lines to the current draft invoice."""
    #     self.ensure_one()
    #
    #     if self.state != 'draft':
    #         raise ValueError("You can only add lines to a draft invoice.")
    #
    #     # Loop through each top line and add it
    #     new_lines = []
    #     for top_line in self.customer_top_lines_ids:
    #         new_lines.append(Command.create({
    #             'product_id': top_line.product_id.id,
    #             'name': top_line.name or top_line.product_id.display_name,
    #             'quantity': top_line.quantity,
    #             'price_unit': top_line.price_unit,
    #             'tax_ids': [Command.set(top_line.tax_ids.ids)],
    #         }))
    #
    #     # Add them all at once
    #     self.write({'invoice_line_ids': new_lines})
    #
    #     return {'type': 'ir.actions.client', 'tag': 'reload'}