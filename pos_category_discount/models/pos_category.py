# -*- coding: utf-8 -*-
from email.policy import default

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class PosCategory(models.Model):
    """Inheriting pos category for adding discount limit feature"""
    _inherit = "pos.category"

    is_enable_category_wise_discount = fields.Boolean(default=False)
    discount_limit = fields.Float(string='Maximum Discount Limit')

    @api.constrains('discount_limit')
    def _check_discount_limit(self):
        """Checking discount is not less than 0."""
        if not 0 <= self.discount_limit:
            raise ValidationError(
                'Error! You cannot set discount limit below 0.')

    @api.model
    def _load_pos_data_fields(self, config_id):
        """Load custom fields to POS frontend."""
        result = super()._load_pos_data_fields(config_id)
        result += ['discount_limit', 'is_enable_category_wise_discount']
        return result