# -*- coding: utf-8 -*-
from odoo import fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    owned_property_ids = fields.One2many('property.details', 'owner_id',string="Owned Properties")

    def action_view_property(self):
        print('button action')
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Property',
            'res_model': 'property.details',
            'view_mode': 'list',
            'context': {'create': False},
        }
