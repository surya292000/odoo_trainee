from odoo import models, fields
from odoo.exceptions import UserError

class ProductButtonWizard(models.TransientModel):
    _name = "product.button.wizard"
    _description = "Product Button Wizard"

    product_id = fields.Many2one('product.product', string="Product", required=True)
    quantity = fields.Float(string="Quantity", required=True)
    price = fields.Float(string="Unit Price", required=True)

    def action_confirm_po(self):
        self.ensure_one()
        product = self.product_id
        if not product.seller_ids:
            raise UserError("No vendors found for this product.")
        vendor = product.seller_ids[0].partner_id
        PurchaseOrder = self.env['purchase.order']
        PurchaseOrderLine = self.env['purchase.order.line']
        existing_po = PurchaseOrder.search([
            ('partner_id', '=', vendor.id),
            ('state', '=', 'draft')
        ], limit=1)

        if existing_po:
            po = existing_po
        else:
            po = PurchaseOrder.create([{
                'partner_id': vendor.id,
                'date_order': fields.Datetime.now(),
            }])
        line = po.order_line.filtered(lambda lin: lin.product_id == product)

        if line:
            line.write({
                'product_qty': line.product_qty + self.quantity,
                'price_unit': self.price,
            })
        else:
            PurchaseOrderLine.create({
                'order_id': po.id,
                'product_id': product.id,
                'name': product.display_name,
                'product_qty': self.quantity,
                'price_unit': self.price,  # ✅ Use wizard's price
                'product_uom': product.uom_po_id.id,
                'date_planned': fields.Datetime.now(),
            })
        if po.state == 'draft':
            po.button_confirm()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Purchase Order',
            'res_model': 'purchase.order',
            'res_id': po.id,
            'view_mode': 'form',
            'target': 'current',
        }