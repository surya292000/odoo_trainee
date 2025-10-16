from odoo import models, fields, api

class ProductApproval(models.Model):
    _name = 'product.approval'
    _description = 'Product Approval'

    product_id = fields.Many2one('product.product', string='Product', required=True)

    @api.model
    def create(self, vals):
        if vals.get('product_id'):
            product = self.env['product.product'].search(['is_new_product'])
        return super(ProductApproval, self).create(vals)
