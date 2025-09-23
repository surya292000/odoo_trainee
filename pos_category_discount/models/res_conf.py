# -- coding: utf-8 --
from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    enable_discount_control = fields.Boolean(string="Enable Discount Control",
                                             help="Enable/Disable discount control for POS sessions.")

    @api.model
    def get_values(self):
        res = super().get_values()
        icp = self.env['ir.config_parameter'].sudo()
        enable_discount = icp.get_param('pos_discount_limit.enable_discount_control', default='False') == 'True'
        res.update({'enable_discount_control': enable_discount})
        return res

    def set_values(self):
        super().set_values()
        icp = self.env['ir.config_parameter'].sudo()
        icp.set_param('pos_discount_limit.enable_discount_control', self.enable_discount_control)
