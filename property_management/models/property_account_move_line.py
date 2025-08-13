# -*- coding: utf-8 -*-
from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    property_lease_line_id = fields.Many2one("property.rental.lease.lines", string="Rent Lease Line")
