from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move.line'

    def button_to_add_invoice_lines(self):
        print('hai')