# -*- coding: utf-8 -*-
from odoo import fields, models


class ProductionProductLines(models.Model):
    _name = "production.product.lines"
    _description = "Product Lines"

    component_id = fields.Many2one('product.product', string='Component')
    quantity = fields.Float(string="Quantity", default=1)
    production_id = fields.Many2one("production.production", string="Production")
    vendor_ids = fields.Many2many("res.partner", string="Vendors")
    request_type = fields.Selection([
        ('purchase_order', 'Purchase Order'),
        ('internal_transfer', 'Internal Transfer')],
        default="purchase_order", required=True)
