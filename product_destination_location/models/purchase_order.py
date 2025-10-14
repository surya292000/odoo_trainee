from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def button_confirm(self):
        super().button_confirm()
        for product in self.order_line:
            if product.product_id.weight > 20:
                self.picking_ids.location_dest_id = self.env.ref('product_destination_location.location_1')
