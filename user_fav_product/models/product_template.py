from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    favourite_user_ids = fields.Many2many('res.users','product_favourite_rel',
        'product_id','user_id',string='Favourited by Users',)

    is_favourite = fields.Boolean(string='Favourite',compute='_compute_is_favourite',inverse='_inverse_is_favourite',
        store=False,)

    @api.depends('favourite_user_ids')
    def _compute_is_favourite(self):
        """Compute if the current user has this product as favourite."""
        user = self.env.user
        for product in self:
            product.is_favourite = user in product.favourite_user_ids

    def _inverse_is_favourite(self):
        """Add/remove the current user when toggling favourite."""
        user = self.env.user
        for product in self:
            if product.is_favourite:
                product.favourite_user_ids = [(4, user.id)]
            else:
                product.favourite_user_ids = [(3, user.id)]
