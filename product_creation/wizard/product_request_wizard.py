from odoo import models, fields


class RentLeaseReportWizard(models.TransientModel):
    _name = "product.request.wizard"
    _description = "Product Request Wizard"

    product = fields.Char(string="Product")
    selling_price = fields.Float(string="Selling Price")
    cost_price = fields.Float(string="Cost Price")

    def action_to_submit_request(self):
        print('hai')
        pass