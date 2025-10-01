from odoo import models, fields


class SaleOrderlineWizard(models.TransientModel):
    _name = "sale.orderline.wizard"
    _description = "Sale Orderline Wizard"

    customer = fields.Many2one('res.partner', string="Customer")
    delivery_address = fields.Many2one