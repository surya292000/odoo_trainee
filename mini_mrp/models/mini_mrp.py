from odoo import fields, models


class MiniMrp(models.Model):
    _name = "mini.mrp"

    product = fields.Many2one('product.product', string="Product", required=True)
    product_qty = fields.Integer(string="Quantity", required=True)
    date_start = fields.Datetime(string="Scheduled Date", default=fields.Datetime.now())
    date_end = fields.Datetime(string="Scheduled End")
    states = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed'), ('done', 'Done')], string="State", default = 'draft')
    user_id = fields.Many2one(
        'res.users', 'Responsible', default=lambda self: self.env.user,
        domain=lambda self: [('groups_id', 'in', self.env.ref('mrp.group_mrp_user').id)])
    mrp_lines_ids = fields.One2many('mini.mrp.line','mini_mrp_id', string="Mrp Lines")

    def action_to_confirm(self):
        self.states = 'confirmed'

    def action_produce(self):
        print('hai')
        self.states = 'done'
        pass


