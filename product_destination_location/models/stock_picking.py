from odoo import models, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.onchange('move_ids_without_package')
    def destination_location(self):
        for product in self.move_ids_without_package:
            if product.product_id.weight > 20:
                self.location_dest_id = self.env.ref('product_destination_location.location_1')
            elif (product.product_id.weight * product.product_uom_qty) > 20:
                self.location_dest_id = self.env.ref('product_destination_location.location_1')

