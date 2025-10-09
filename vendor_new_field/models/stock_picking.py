from odoo import models, fields, _
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = 'stock.picking'


    def button_validate(self):
        print('haii')
        for picking in self:
            for move_line in picking.move_line_ids:
                print('hyyy')
                print(move_line.lot_id, 'hiiiii')
                print(move_line.product_id.expiration_date,'alooiiii')
                print(move_line.lot_id.expiration_date, 'allllo')

                if move_line.lot_id and move_line.lot_id.expiration_date:
                    if move_line.lot_id.expiration_date < fields.Date.today():
                        raise ValidationError(_("Validation Error: The product '%s' from lot/serial number has expired."))
        return super(StockPicking, self).button_validate()