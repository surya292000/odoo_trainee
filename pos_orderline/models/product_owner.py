# -*- coding: utf-8 -*-
from odoo import fields, models


class ProductOwner(models.Model):
    _inherit = 'product.template'

    product_owner_id = fields.Many2one('res.partner')

class ProductOwnerPos(models.Model):
    _inherit = 'product.product'

    def _load_pos_data_fields(self, config_id):
        result = super()._load_pos_data_fields(config_id)
        result += ['product_owner_id']
        return result