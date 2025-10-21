from odoo import models, fields, api, _


class ProductLine(models.Model):
    _name = 'product.line'
    _description = 'Product Line'

    crm_commission_id = fields.Many2one(comodel_name='crm.commission', string='Custom Model Reference')
    product_id = fields.Many2one('product.product', string='Product')
    commission_type = fields.Selection([('straight', 'Straight'), ('graduated', 'Graduated')])
    product_commission = fields.Float(compute="_compute_product_commission", string="Product Commission")
    straight_commission = fields.Float(string="Straight Commission")

    @api.onchange('commission_type')
    def _onchange_commission_type(self):
        sale_person_id = self.crm_commission_id.sale_person.id
        sale_report = self.env['sale.report'].search([('user_id', '=', sale_person_id)])
        if self.commission_type == 'straight':
            self.straight_commission = sum(sale_report.mapped('price_subtotal'))*(10/100)
            print(self.straight_commission, 'straight commission')
        elif self.commission_type == 'graduated':
            print('haiiii')

    @api.depends('product_id')
    def _compute_product_commission(self):
        self.product_commission = (self.product_id.lst_price * 10)/100