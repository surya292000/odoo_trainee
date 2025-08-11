from odoo import fields, api, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = 'Property Type'

    name = fields.Text('Property Type', required=True)
    sequence = fields.Integer('Sequence', default=1,help="Used to order stages. Lower is better")
    property_ids = fields.One2many(
        comodel_name="estate.property",
        inverse_name="property_type_id",
        string="Properties"
    )

    _sql_constraints = [
        ('type_name_unique', 'unique(name)', 'Property type name must be unique.'),
    ]
