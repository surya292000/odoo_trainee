# -*- coding: utf-8 -*-
from odoo import fields, models, api


class ProductionProductLines(models.Model):
    _name = "production.product.lines"
    _description = "Product Lines"

    product_id = fields.Many2one("product.product", string="Product")
    product_uom = fields.Many2one(related="product_id.uom_id",string="Unit")
    quantity = fields.Integer(string="Quantity")
    production_product_id = fields.Many2one("production.production", string="production product")
    vendors_ids = fields.Many2many("res.partner", string="vendors")
    order_type = fields.Selection([('purchase_order', 'Purchase Order'), ('internal_transfer', 'Internal Transfer')])


    # @api.depends('quantity','price_unit')
    # def _compute_total_amount(self):
    #     for record in self:
    #         record.total_amount = record.quantity * record.price_unit