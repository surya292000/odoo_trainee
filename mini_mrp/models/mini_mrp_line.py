from odoo import fields, models, api


class MiniMrpLine(models.Model):
    _name = "mini.mrp.line"

    product = fields.Many2one('product.product',string="Product")
    mini_mrp_id = fields.Many2one('mini.mrp',string="Mrp ID")
    qty_product = fields.Integer(string="Quantity")
    location_id = fields.Many2one('stock.move', string="Location")

    # @api.depends('product')
    # def _compute_product_location(self):
    #     print('hai')
    #     print(self.product, 'product')
    #     if self.product:
    #         print(self.product.warehouse_id.lot_stock_id, 'location')
    #         self.location_id = self.product.warehouse_id.lot_stock_id

