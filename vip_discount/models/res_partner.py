from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_vip = fields.Boolean(string="Is VIP")
    vip_discount = fields.Float(string="VIP Discount")
