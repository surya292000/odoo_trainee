# -*- coding: utf-8 -*-
from odoo import fields, models
class ResConfigSettings(models.TransientModel):
   _inherit = 'res.config.settings'

   is_max_amount = fields.Boolean(string='Discount limit',
         config_parameter='sale_order_configuration.is_discount_limit',
         help='Check this field for enabling discount limit')
   max_amount = fields.Float(string='Limit amount',
         config_parameter='sale_order_configuration.max_amount',
         help='The Max amount ')

