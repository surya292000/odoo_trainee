from odoo import models, fields, api


class ProductProduct(models.Model):
    _inherit = 'product.product'

    is_new_product = fields.Boolean(string="New Product")

    @api.model_create_multi
    def create(self, vals_list):
        record = super().create(vals_list)
        if not self.env.user.has_group('product_creation.group_erp_manager'):
            record.active = False
            record.is_new_product = True
        return record

    def action_to_approve(self):
        self.active = True
        self.is_new_product = False
