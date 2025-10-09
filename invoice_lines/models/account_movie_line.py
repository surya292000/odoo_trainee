from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move.line'

    move_id = fields.Many2one('account.move', string='move')

    def action_add_invoice_line(self):
        print('hai')
        for line in self:
            print(line, 'line')
            move = line.move_id
            print(move, 'move')
            if move.move_type != 'out_invoice':
                continue
            for lin in self.move_id.customer_top_lines_ids:
                print(lin, 'linnn')
                move.write({
                    'invoice_line_ids': [{
                        lin
                    }]
                })
        return True