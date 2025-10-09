from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    reference_date = fields.Datetime(string='Last Reference Date')
