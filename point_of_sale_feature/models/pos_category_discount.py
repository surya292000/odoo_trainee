
# -*- coding: utf-8 -*-
"""model to add category in pos config"""

from odoo import models, fields


class PosCategoryDiscount(models.Model):
    """for select category and discount amount"""
    _name = "pos.category.discount"
    _description = "Pos Category Discount"
    _inherit = ['pos.load.mixin']

    section_id = fields.Many2one('pos.config', string='Section')
    category_id = fields.Many2one('pos.category', string='Category')
    pos_category_discount = fields.Float(string='Discount')
    allowed_categories_ids = fields.Many2many('pos.category', 'name',related='section_id.iface_available_categ_ids')


