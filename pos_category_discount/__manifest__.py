# -*- coding: utf-8 -*-
{
    'name': "POS category discount",
    'version': '18.0.1.3.2',
    'description': 'Set a category wise limit to discount in POS.',
    'sequence': -1,
    'summary': 'Set a category wise limit to discount in POS',
    'category': 'sales',
    'depends': [
        'web',
        'base',
        'product',
        'point_of_sale',
    ],
    'data': [
        'views/pos_category_view.xml',
        'views/res_config_settings_views.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_category_discount/static/src/js/pos_category_discount.js',
        ],
    },

    'license': 'LGPL-3',
}