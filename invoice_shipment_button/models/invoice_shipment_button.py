from odoo import models, fields

class AccountMove(models.Model):
    _inherit = "account.move"

    shipment_count = fields.Integer(
        string="Shipments",
        compute="_compute_shipment_count"
    )

    def _compute_shipment_count(self):
        for move in self:
            move.shipment_count = self.env['stock.picking'].search_count([
                ('origin', '=', move.invoice_origin)
            ])

    def action_view_shipments(self):
        self.ensure_one()
        return {
            'name': "Shipments",
            'type': 'ir.actions.act_window',
            'res_model': 'stock.picking',
            'view_mode': 'list,form',
            'domain': [('origin', '=', self.invoice_origin)],
        }
