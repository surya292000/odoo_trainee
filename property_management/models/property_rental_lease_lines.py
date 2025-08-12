# -*- coding: utf-8 -*-
from odoo import fields, models, api


class PropertyRentalLeaseLines(models.Model):
    _name = "property.rental.lease.lines"
    _rec_name = "property_id"
    _description = "Rented/Lease lines"

    property_id = fields.Many2one("property.details", string="Property")
    amount = fields.Float(string='Amount', compute='_compute_amount')
    rental_id = fields.Many2one("property.rental.lease", string="Property ID")
    quantity = fields.Integer(string="Quantity", related="rental_id.total_days")
    order_line_ids = fields.Many2many('account.move.line', string="order_lines")
    invoiced_quantity = fields.Integer(string="Invoiced quantity", compute="_compute_invoiced_quantity")

    @api.depends('rental_id.rental_type')
    def _compute_amount(self):
        for rec in self:
            if rec.rental_id.rental_type == 'Rent':
                rec.amount = rec.property_id.rent
            else:
                rec.amount = rec.property_id.legal_amount

    @api.depends('order_line_ids.move_id.state')
    def _compute_invoiced_quantity(self):
        for line in self:
            related_invoice_lines = line.order_line_ids.filtered(
                lambda lin: lin.move_id.move_type == 'out_invoice'
                            and lin.move_id.state in ['posted'])
            line.invoiced_quantity = sum(related_invoice_lines.mapped('quantity'))

    @api.onchange('self.rental_id.rental_type')
    def _onchange_rental_type(self):
        if self.rental_id.rental_type == 'Rent':
            self.property_id.states = 'Rented'
        elif self.rental_id.rental_type == 'Lease':
            self.property_id.states = 'Leased'
        else:
            self.property_id.states = 'Draft'

    @api.onchange('amount')
    def _amount_change(self):
        self.property_id.legal_amount = self.amount
