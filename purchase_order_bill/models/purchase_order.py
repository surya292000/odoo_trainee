# -*- coding: utf-8 -*-
from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def button_confirm(self):
        res = super(PurchaseOrder, self).button_confirm()
        for order in self:
            if order.invoice_status == 'to invoice':
                bill = self.env['account.move'].create({
                    'move_type': 'in_invoice',  # Specifies that it is a vendor bill
                    'partner_id': order.partner_id.id,
                    'purchase_id': order.id,
                    'invoice_date': fields.Date.today(),
                    'invoice_line_ids': [
                        fields.Command.create({
                            'product_id': line.product_id.id,
                            'name': line.name,
                            'quantity': line.product_qty,
                            'price_unit': line.price_unit,
                        }) for line in order.order_line
                    ],
                })

                if bill:
                    bill.action_post()

        return res
