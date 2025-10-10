from odoo import models, fields, _
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        for picking in self:
            for move_line in picking.move_line_ids:
                if move_line.lot_id and move_line.lot_id.expiration_date:
                    if move_line.lot_id.expiration_date < fields.Datetime.now():
                        raise ValidationError(_("Validation Error: The product '%s' from lot/serial number has expired."))
        return super(StockPicking, self).button_validate()
