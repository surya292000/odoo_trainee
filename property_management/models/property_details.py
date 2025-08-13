# -*- coding: utf-8 -*-
from odoo import fields, models


class PropertyDetails(models.Model):
    _name = "property.details"
    _inherit = 'mail.thread'
    _description = "Property Details"

    name = fields.Char(string="Property", required=True)
    street = fields.Char(string="Street")
    city = fields.Char(string="City")
    state_id = fields.Many2one("res.country.state", string="State")
    country_id = fields.Many2one("res.country", string="Country")
    built_date = fields.Date(string="Build Date")
    legal_amount = fields.Float(string="Legal Amount")
    rent = fields.Integer(string="Rent")
    owner_id = fields.Many2one("res.partner", string="Owner")
    property_image = fields.Binary(store=True)
    description = fields.Text(string="Description")
    can_be_sold = fields.Boolean(string="Can be sold")
    facilities_ids = fields.Many2many("property.facility", string="Facilities")
    rent_count = fields.Integer(String="Rent count", compute="_compute_rent_count", default=0)
    states = fields.Selection([('Draft', 'Draft'), ('Rented', 'Rented'), ('Leased', 'Leased'),
                               ('Sold', 'Sold')],
                              string='State', required=True, default='Draft')
    property_rental_lease_id = fields.Many2one("property.rental.lease", string="state of rent or lease")

    def _compute_rent_count(self):
        for record in self:
            record.rent_count = self.env['property.rental.lease'].search_count(
                [('property_ids.property_id', '=', self.id)])

    def unlink(self):
        order_line = self.env['property.rental.lease.lines']
        for record in self:
            lease_lines = order_line.search([('property_id', '=', record.id)])
            parent_lease = lease_lines.mapped('rental_id')
            lease_lines.unlink()
            remaining_lines = order_line.search([('rental_id', '=', parent_lease.id)])
            if not remaining_lines:
                parent_lease.unlink()
        return super().unlink()

    def action_get_rent_count(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Rental Leases',
            'view_mode': 'list,form',
            'res_model': 'property.rental.lease',
            'domain': [('property_ids.property_id', '=', self.id)],
            'context': {'create': False}
        }
