# -*- coding: utf-8 -*-
{
    'name': "POS Category",
    'depends': ['base', 'point_of_sale', 'product'],
    'data': ["views/category_discount.xml",
             "views/config_settings_bool_field.xml.xml",
    ],

'assets': {
    "point_of_sale._assets_pos": [
        "pos_category_discount/static/src/js/pos_category_discount.js"
    ],},
}