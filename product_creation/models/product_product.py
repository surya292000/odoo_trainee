from odoo import models, fields, api


class ProductProduct(models.Model):
    _inherit = 'product.product'

    is_new_product = fields.Boolean(string="New Product")

    @api.model_create_multi
    def create(self, vals_list):
        if not self.env.user.has_group('product_creation.group_erp_manager'):
            for vals in vals_list:
                vals['active'] = False
                vals['is_new_product'] = True
        return super().create(vals_list)

    def action_to_approve(self):
        self.write({'active': 1, 'is_new_product': 0})

