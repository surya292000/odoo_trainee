from odoo import models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _is_website_order(self):
        return bool(self.website_id)

    def _get_applicable_programs(self):
        print('hai')
        programs = super()._get_applicable_programs()
        if not self._is_website_order():
            website_promo = self.env.ref('ecommerce_discount.promo_5_percent_website', raise_if_not_found=False)
            if website_promo:
                programs = programs - website_promo
        return programs
