from dateutil.relativedelta import relativedelta

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    project_id = fields.Many2one('project.project',compute='_compute_project', string='Project')

    @api.depends('partner_id')
    def _compute_project(self):
        print('haiiii')
        print(self.partner_id, 'partner')
        for pro in self:
            print(pro, 'pro')
            pro.project = self.env['project.project'].search(['partner_id', '=', self.partner_id])
            self.project_id = pro.project


    # def action_confirm(self):
    #     print('hii')
    #     confirmed_sales = self.env['sale.order'].search(
    #         ["&", ("partner_id", "=", self.partner_id.id), ("state", "=", "sale")]
    #     )
    #     print(confirmed_sales, 'confirmed_sales')
    #
    #     confirmed_sales_count = len(confirmed_sales)
    #     print(confirmed_sales_count, 'confirmed_sales_count')
    #
    #     confirmed_sales_amount = sum(confirmed_sales.mapped('amount_total'))
    #     print(confirmed_sales_amount)
    #
    #     sale_order_dates = confirmed_sales.sorted(lambda rec: rec.date_order)
    #     print(sale_order_dates, 'first sale order')
    #
    #     if sale_order_dates:
    #         first_sale_order = sale_order_dates[0]
    #         print(first_sale_order, 'first_sale_order')
    #
    #         today = fields.Datetime.now()
    #         print(type(today), 'today')
    #         print(type(first_sale_order.date_order), 'lllll')
    #
    #         difference = first_sale_order.date_order - today
    #         print(difference, 'jjjjjjjjjjjjj')
    #
    #         diff = relativedelta(today, first_sale_order.date_order)
    #         diff.months
    #         print(diff.months, 'diff')
    #
    #         if not (confirmed_sales_count >= 2 or confirmed_sales_amount > 10000 or diff.months >= 6):
    #             raise ValidationError('dfghj')
    #     else:
    #         raise ValidationError('dfghj')
    #
    #     super(SaleOrder, self).action_confirm()




    # def action_confirm(self):
    #     print('hii')
    #     for lines in self.order_line:
    #         cost_price = lines.product_id.standard_price
    #         if lines.price_unit < cost_price + ((15/100)*cost_price):
    #             raise ValidationError(f'Cannot confirm order. Some items are sold below allowed margin."')
    #     super(SaleOrder,self).action_confirm()