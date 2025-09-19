# -*- coding: utf-8 -*-
{
    'name': "POS",
    'depends': ['base', 'point_of_sale', 'product'],
    'data': ["views/product_owner_views.xml",
             "views/pos_menu.xml",
    ],
'assets': {
    'web.assets_frontend': [
        "pos/static/src/js/order_lines.js",
        "pos/static/src/js/product_owner.js",
        "pos/static/src/xml/order_line.xml",
    ],},
    'application': True, "sequence": 1
}