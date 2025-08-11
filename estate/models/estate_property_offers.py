from email.policy import default

from odoo import fields, api, models
from datetime import date, timedelta
from odoo.exceptions import ValidationError

from odoo.exceptions import ValidationError


class EstatePropertyOffers(models.Model):
    _name = "estate.property.offers"
    _description = 'Property offers'

    @api.depends("validity")
    def _compute_date_from(self):
        for record in self:
            record.deadline = date.today() + timedelta(days=record.validity)

    def _inverse_date_from(self):
        for record in self:
            record.validity = (record.deadline - date.today()).days

    def action_accept(self):
        for record in self:
            if record.property_id.selling_price == 0:
                record.status = 'accepted'
                record.property_id.selling_price = record.price
                record.property_id.seller_id = record.partner_id
            else:
                raise ValidationError('error')
        return True

    def action_refuse(self):
        for record in self:
            record.status = 'refused'
            if record.status == 'refused':
                record.property_id.selling_price = 0
                record.property_id.seller_id = ''
        return True

    # approve = fields.Selection([('approved','Approved'),('refused','Refused')],string='Approve', copy=False)

    Title = fields.Char(String="Title")
    price = fields.Float(string="Price")
    status = fields.Selection([('approved', 'Approved'), ('accepted', 'Accepted'), ('refused', 'Refused')],
                              string='Status', copy=False)


    partner_id = fields.Many2one("res.partner", string="Partner")
    property_id = fields.Many2one("estate.property", string="Property", required=True)

    validity = fields.Integer(string="Validity(Days)", default=7)
    deadline = fields.Date(compute="_compute_date_from", inverse="_inverse_date_from")

    _sql_constraints = [
        ('check_offer_price_positive', 'CHECK(price > 0)', 'Offer price must be strictly positive.')
    ]
