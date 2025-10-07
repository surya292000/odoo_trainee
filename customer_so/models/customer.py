from odoo import fields, models, api

class ResPartner(models.Model):
    _inherit = "res.partner"

    ordered_lines_ids = fields.Many2many(
        comodel_name='sale.order.line',
        string='Product',
        compute='_compute_ordered_lines_ids',
        store=True)
    prt_threshold = fields.Float(string="Threshold Quantity")

    @api.depends('sale_order_ids.order_line')
    def _compute_ordered_lines_ids(self):
        for partner in self:
            partner.ordered_lines_ids = partner.sale_order_ids.mapped('order_line')

    def button_to_create_so(self):
        print('so')
        self.ensure_one()
        print(self.id, 'id')
        order_lines = self.ordered_lines_ids
        sale_order = self.env['sale.order'].create({
            'partner_id': self.name,
            'order_line': [fields.Command.create({
                'name': self.id,
                'product_id': line.name,
                'product_uom_qty': self.prt_threshold,
                'price_unit': line.price_unit,
                # 'product_uom': line.product_uom_id.id,
            }) for line in order_lines if self.name],
        })

        return {
            'type': 'ir.actions.act_window',
            'name': 'Sale Order',
            'res_model': 'sale.order',
            'res_id': sale_order.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def button_to_check_threshold(self):
        pass
