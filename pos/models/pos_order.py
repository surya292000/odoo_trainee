# -*- coding: utf-8 -*-
from odoo import models


class PosOrder(models.Model):
    _inherit = 'pos.order'

    def _order_fields(self, ui_order):
        res = super()._order_fields(ui_order)
        res['product_owner_id'] = ui_order.get('product_owner_id')
        return res
