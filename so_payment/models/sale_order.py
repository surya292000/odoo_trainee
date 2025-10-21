from odoo import models, fields
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_register_payment(self):
        invoices = self.invoice_ids.filtered(lambda inv: inv.state == 'posted' and inv.amount_residual > 0)

        if not invoices:
            raise UserError('No outstanding invoice for this sale order')
        ctx = {
            'active_model': 'account.move',
            'active_ids': invoices.ids,
        }
        return {
            'name': 'Register Payment',
            'type': 'ir.actions.act_window',
            'res_model': 'account.payment.register',
            'view_mode': 'form',
            'context': ctx,
            'target': 'new',
        }
