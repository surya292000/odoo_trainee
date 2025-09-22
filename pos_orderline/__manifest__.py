# -*- coding: utf-8 -*-
{
    'name': "POS",
    'depends': ['base', 'point_of_sale', 'product'],
    'data': ["views/product_owner_views.xml",
    ],
'assets': {
    "point_of_sale._assets_pos": [
        "pos_orderline/static/src/js/order_lines.js",
        "pos_orderline/static/src/js/product_owner.js",
        "pos_orderline/static/src/xml/order_line.xml",
    ],},
    'application': True, "sequence": 1
}