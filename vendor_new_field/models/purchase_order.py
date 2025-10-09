from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    po_reference_date = fields.Datetime(related='partner_id.reference_date',string="Last Reference Date",store=True)

    def button_confirm(self):
        print('dfghjm,')
        super(PurchaseOrder, self).button_confirm()
        for order in self:
            order.partner_id.reference_date = order.date_approve
