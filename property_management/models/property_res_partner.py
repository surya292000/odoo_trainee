# -*- coding: utf-8 -*-
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    owned_property_ids = fields.One2many('property.details', 'owner_id',string="Owned Properties")
