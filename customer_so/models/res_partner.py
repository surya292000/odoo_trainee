from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    threshold = fields.Float(string='Product Threshold', default=0.0)
    product_ids = fields.Many2many('product.product', string='Products')

    def action_recalculate_products(self):
        partner = self.id
        print(partner, 'partner')
        sale_order = self.env['sale.order'].search(['partner_id.id'])
        print()

        # sale_order = self.env['sale.order'].search(['partner_id.id'])
        # print(sale_order, 'sale order')
        # for order in sale_order:
        #     print(order, 'order')
        #     if order.partner_id == partner:
        #         print(order.order_line, 'order lines')

        # for partner in self:
        #     if partner.threshold <= 0:
        #         continue
        #     sale_orders = self.env['sale.order'].search([
        #         ('partner_id', '=', partner.id),
        #         ('state', 'in', ['sale', 'done'])
        #     ])
        #
        #     # Gather products whose ordered quantity ≥ threshold
        #     product_ids = set()
        #     for order in sale_orders:
        #         for line in order.order_line:
        #             if line.product_id and line.product_uom_qty >= partner.threshold:
        #                 product_ids.add(line.product_id.id)
        #
        #     # Update the many2many field with those products
        #     partner.product_ids = [(6, 0, list(product_ids))]

    def action_create_so(self):
        SaleOrder = self.env['sale.order']
        SaleOrderLine = self.env['sale.order.line']

        for partner in self:
            if not partner.product_ids:
                continue
            order = SaleOrder.create({
                'partner_id': partner.id,
            })
            for product in partner.product_ids:
                SaleOrderLine.create({
                    'order_id': order.id,
                    'product_id': product.id,
                    'product_uom_qty': partner.threshold or 1.0,
                    'price_unit': product.lst_price,
                })
        return True
