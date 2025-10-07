from ast import literal_eval
from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    """Extension of 'res.config.settings' for configuring delivery settings."""
    _inherit = 'res.config.settings'

    pdt_threshold = fields.Float(string='Threshold of Product',
                                     help='This field is used to set threshold value for products')