from odoo import models, _, api, fields
from odoo.exceptions import ValidationError


class ProductProduct(models.Model):
    _inherit = 'product.product'

    is_approval_needed = fields.Boolean(String='Need Approval')

    @api.model
    def create(self, vals):
        if not self.env.user.has_group('base.group_erp_manager'):
            self.is_approval_needed = True
            raise ValidationError(_('Sorry, you are not allowed to create new products.'))
        else:
            return super(ProductProduct, self).create(vals)
