# -*- coding: utf-8 -*-
"""To inherit and add new field into pos config model"""

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class PosConfig(models.Model):
    """Add new field and function into pos.config"""
    _inherit = 'pos.config'

    pos_category_discount_enable = fields.Boolean("Category discount enable")
    pos_categories_discount_ids = fields.One2many('pos.category.discount', 'section_id',
                                                  string='Pos Categories')

    @api.onchange('pos_categories_discount_ids')
    def _onchange_pos_categories_discount_ids_exist(self):
        """Check existing category or not"""
        exist_category_list = []
        for line in self.pos_categories_discount_ids:
            if line.category_id.id in exist_category_list:
                raise ValidationError(_('The category should be different'))
            exist_category_list.append(line.category_id.id)

