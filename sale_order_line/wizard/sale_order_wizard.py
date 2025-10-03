from odoo import models, fields

class SaleOrderFromLinesWizard(models.TransientModel):
    _name = 'sale.order.from.lines.wizard'
    _description = 'Create Sale Order from Lines Wizard'

    partner_id = fields.Many2one('res.partner', string="Customer", required=True)
    pricelist_id = fields.Many2one(
        'product.pricelist',
        string="Pricelist",
        related="partner_id.property_product_pricelist",
        readonly=True,
    )
    invoice_address_id = fields.Many2one(
        'res.partner', string="Invoice Address", readonly=True,
        compute="_compute_addresses"
    )
    delivery_address_id = fields.Many2one(
        'res.partner', string="Delivery Address", readonly=True,
        compute="_compute_addresses"
    )
    line_ids = fields.Many2many('sale.order.line', string="Selected Lines")

    def _compute_addresses(self):
        for wizard in self:
            if wizard.partner_id:
                wizard.invoice_address_id = wizard.partner_id.address_get(['invoice'])['invoice']
                wizard.delivery_address_id = wizard.partner_id.address_get(['delivery'])['delivery']
            else:
                wizard.invoice_address_id = False
                wizard.delivery_address_id = False

    def action_create_sale_order(self):
        SaleOrder = self.env['sale.order']
        SaleOrderLine = self.env['sale.order.line']

        order = SaleOrder.create({
            'partner_id': self.partner_id.id,
            'pricelist_id': self.pricelist_id.id,
            'partner_invoice_id': self.invoice_address_id.id,
            'partner_shipping_id': self.delivery_address_id.id,
        })

        for line in self.line_ids:
            SaleOrderLine.create({
                'order_id': order.id,
                'product_id': line.product_id.id,
                'product_uom_qty': line.product_uom_qty,
                'price_unit': line.price_unit,
                'name': line.name,
                'product_uom': line.product_uom.id,
            })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'view_mode': 'form',
            'res_id': order.id,
        }
