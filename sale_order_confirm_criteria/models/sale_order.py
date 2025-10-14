from dateutil.relativedelta import relativedelta

from odoo import models, fields
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'


    def action_confirm(self):
        confirmed_sales = self.env['sale.order'].search([("partner_id", "=", self.partner_id.id), ("state", "=", "sale")])
        confirmed_sales_count = len(confirmed_sales)
        confirmed_sales_amount = sum(confirmed_sales.mapped('amount_total'))
        sale_order_dates = confirmed_sales.sorted(lambda rec: rec.date_order)
        if sale_order_dates:
            diff = relativedelta(fields.Datetime.now(), sale_order_dates[0].date_order)
            if not (confirmed_sales_count >= 2 or confirmed_sales_amount > 10000 or diff.months >= 6):
                raise ValidationError('This sale order does not meets minimum criteria')
        else:
            raise ValidationError('This sale order does not meets minimum criteria')
        super(SaleOrder, self).action_confirm()
