from odoo import models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def action_button_to_open_wizard(self):
        return {
            'name': 'Create PO',
            'view_mode': 'form',
            'res_model': 'product.button.wizard',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'context': {'default_product_id': self.id}
        }
