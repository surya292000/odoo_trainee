# -*- coding: utf-8 -*-
from odoo import fields, models


class ProductionProductLines(models.Model):
    _name = "material.request.lines"
    _description = "Material Request Lines"

    component_id = fields.Many2one('product.product', string='Component')
    quantity = fields.Float(string="Quantity", default=1)
    request_id = fields.Many2one("material.request", string="Production")
    vendor_ids = fields.Many2many("res.partner", string="Vendors")
    src_location_id = fields.Many2one("stock.location", string="SRC Location")
    dest_location_id = fields.Many2one("stock.location", string="Destination Location")
    request_type = fields.Selection([
        ('purchase_order', 'Purchase Order'),
        ('internal_transfer', 'Internal Transfer')],
        default="purchase_order", required=True)
