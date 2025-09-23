# -*- coding: utf-8 -*-
from odoo import models, fields, api

class PosCategory(models.Model):
    _inherit = 'pos.category'

    maximum_discount = fields.Float(string='Maximum Discount', config_parameter='pos_category_discount.maximum_discount')

    show_maximum_discount = fields.Boolean(
        string='Show Maximum Discount', compute='_compute_show_maximum_discount'
    )

    @api.depends()
    def _compute_show_maximum_discount(self):
        param = self.env['ir.config_parameter'].sudo().get_param('pos_discount_limit.enable_discount_control', default='False')
        for rec in self:
            rec.show_maximum_discount = param == 'True'
