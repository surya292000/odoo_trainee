# -*- coding: utf-8 -*-
from odoo import fields, models


class PropertyFacility(models.Model):
    _name = "property.facility"
    _description = "Property Facility"

    name = fields.Text(string="Facility")
