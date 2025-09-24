# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    """Extension of 'res.config.settings' for setting category discount limit."""
    _inherit = 'res.config.settings'

    enable_category_wise_discount = fields.Boolean(
        related='pos_config_id.is_enable_category_wise_discount',
        string='Category discount limit',
        readonly=False,
        help='This field is used to enable setting category wise'
             ' discount in POS Category.')

    @api.onchange('enable_category_wise_discount')
    def _set_is_enable_category_wise_discount(self):
        """Setting is_enable_category_wise_discount in selected categories in
        current POS."""
        for res_config in self:
            for categ in res_config.pos_iface_available_categ_ids:
                categ._origin.is_enable_category_wise_discount = res_config.enable_category_wise_discount

    @api.model
    def get_values(self):
        """Get the values from settings."""
        res = super(ResConfigSettings, self).get_values()
        icp_sudo = self.env['ir.config_parameter'].sudo()
        enable_category_wise_discount = icp_sudo.get_param(
            'res.config.settings.enable_category_wise_discount')
        res.update(
            enable_category_wise_discount=enable_category_wise_discount,
        )
        return res

    def set_values(self):
        """Set the values. The new values are stored in the configuration parameters."""
        res = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param(
            'res.config.settings.enable_category_wise_discount',
            self.enable_category_wise_discount)
        return res
