# -*- coding: utf-8 -*-

from odoo import api, fields, models

class ExampleLine(models.Model):
    _name = "example.line"
    _description = "Example line"

    example_id = fields.Many2one(
        'example',
        string='Example')
    product_id = fields.Many2one(
        'product.product',
        string='Product')
    qty = fields.Integer(string='Quantity')
    price = fields.Float()
    sub_total = fields.Float(compute='_compute_sub_total')

    @api.depends('qty','price')
    def _compute_sub_total(self):
        for record in self:
            record.sub_total = record.qty*record.price

