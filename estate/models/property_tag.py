from odoo import fields,api,models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tags"
    _description = 'Property Tags'

    name = fields.Text()
    # property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    # color = fields.Integer(string="Color Index")
    # sequence = fields.Integer(default=10)

    _sql_constraints = [
        ('unique_type_name', 'UNIQUE(name)', 'Property type name must be unique.')
    ]