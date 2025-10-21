from odoo import models, fields, api


class RentLeaseReportWizard(models.TransientModel):
    _name = "product.button.wizard"
    _description = "Product Button Wizard"

    product_id = fields.Many2one('product.product',string="product")
    quantity = fields.Integer(string="Quantity")
    price = fields.Float(string="Price")


    def action_confirm_po(self):
        self.ensure_one()
        product = self.product_id
        previous_pos = self.env['purchase.order'].search([])
        vendor = previous_pos[0].partner_id

        existing_po = previous_pos.mapped('')

        purchase_order = self.env['purchase.order'].create({
            'partner_id': vendor.id,
            'order_line': [fields.Command.create({
                'product_id': product.id,
                'name': product.name,
                'product_qty': self.quantity,
                'price_unit': self.price,
            })]
        })
        return {
            'type': 'ir.actions.act_window',
            'name': 'Purchase Order',
            'res_model': 'purchase.order',
            'res_id': purchase_order.id,
            'view_mode': 'form',
            'target': 'current',
        }
