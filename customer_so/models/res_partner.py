from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    threshold = fields.Float(string='Product Threshold', default=0.0)
    product_ids = fields.Many2many('product.product', string='Products')

    def action_recalculate_products(self):
        partner = self.id
        threshold_qty = self.threshold
        print(partner, 'partner')
        sale_orders = self.env['sale.order'].search([('partner_id', '=', partner)])
        print(sale_orders, 'sale order')

        products = []
        for line in sale_orders.mapped('order_line'):
            if line.product_uom_qty >= threshold_qty:
                products.append(line.product_id.id)

        print(products, 'eligible product ids')
        self.product_ids = products


        # product_id = sale_orders.order_line.mapped('product_template_id')
        # print(product_id, 'product id')
        # for pro in product_id:
        #     qty_ordered = sale_orders.order_line.mapped('product_template_id')
        #     # qty_ordered = sale_orders.order_line.mapped('product_uom_qty')
        #     print(qty_ordered, 'qty_ordered')
        #     for order in qty_ordered:
        #         if order >= threshold_qty:
        #
        #             print('greater')

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
