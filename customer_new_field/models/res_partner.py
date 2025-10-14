from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    restricted = fields.Boolean(string='Restricted')
    count = fields.Integer(string='Count')