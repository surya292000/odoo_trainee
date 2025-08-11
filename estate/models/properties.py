from odoo import fields, api, models
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = 'Description'

    def action_do_sold(self):
        for record in self:
            if record.status == "Cancelled":
                raise UserError("A sold property cannot be cancelled")
            record.status = "sold"

    def action_do_cancelled(self):
        for record in self:
            if record.status == "sold":
                raise UserError("A cancelled property cannot be sold")
            record.status = "Cancelled"

    total = fields.Float(compute="_compute_total")

    @api.depends("garden_area", "living_area")
    def _compute_total(self):
        for record in self:
            record.total = 2.0 * record.living_area * record.garden_area

    best_offer = fields.Float(string="Best Offer", compute="_compute_best_offer")

    @api.depends("offers_line_ids")
    def _compute_best_offer(self):
        for record in self:
            prices = record.offers_line_ids.mapped('price')
            if prices:
                record.best_offer = max(prices)
            else:
                record.best_offer = 0.0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'North'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price_margin(self):
        for record in self:
            if record.selling_price > 0 and record.selling_price < 0.9 * record.expected_price:
                raise ValidationError("The selling price cannot be lower than 90% of the expected price.")

    name = fields.Char(string='Name', required=True)
    status = fields.Selection([('new', 'New'),('offer_received', 'Offer Received'),('offer_accepted', 'Offer Accepted'),('sold', 'Sold'),
    ], string="Status", required=True, default='new')
    description = fields.Text()
    postcode = fields.Char()
    data_availability = fields.Date(default=fields.Datetime.now())
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(read_only=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Float()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Float()
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('North', 'North'), ('Riverside', 'Riverside'), ('Hilltop', 'Hilltop'), ('Roadside', 'Roadside')],
    )

    buyer_id = fields.Many2one("res.partner", string="Buyer")
    seller_id = fields.Many2one("res.partner", string="Seller")
    property_type_id = fields.Many2one("estate.property.type", string="Type")
    property_tags_ids = fields.Many2many("estate.property.tags", string="Tag")
    offers_line_ids = fields.One2many("estate.property.offers", "property_id", string="Offers")

    _sql_constraints = [
        # ('check_selling_price', 'CHECK(selling_price >= 0)','The selling price must be positive or zero.'),
        ('check_expected_price', 'CHECK(expected_price > 0)', 'The expected price must be strictly positive.')
    ]

