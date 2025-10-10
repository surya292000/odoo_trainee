from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_create_purchase_order(self):
        self.ensure_one()
        vendor = self.partner_id
        bill_lines = self.invoice_line_ids

        purchase_order = self.env['purchase.order'].create({
            'partner_id': vendor.id,
            'order_line': [fields.Command.create({
                'product_id': line.product_id.id,
                'name': line.name,
                'product_qty': line.quantity,
                'price_unit': line.price_unit,
                'product_uom': line.product_uom_id.id,
            }) for line in bill_lines if line.product_id],
        })
        if purchase_order:
            print(purchase_order, 'hhhhhhh')
            print(purchase_order.invoice_ids, 'jjjjjjjjj')
        return {
            'type': 'ir.actions.act_window',
            'name': 'Purchase Order',
            'res_model': 'purchase.order',
            'res_id': purchase_order.id,
            'view_mode': 'form',
            'target': 'current',
        }
