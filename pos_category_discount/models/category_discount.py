# -*- coding: utf-8 -*-
from odoo import fields, models


class ProductOwner(models.Model):
    _inherit = 'product.category'

    product_discount = fields.Float(string='Discount Percentage')
