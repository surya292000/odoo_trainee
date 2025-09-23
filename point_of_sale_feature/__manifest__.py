# -*- coding: utf-8 -*-

{
    'name': "Point of sale features new",
    'version': '1.0',
    'depends': ['base','point_of_sale'],
    'author': "STARLIN",
    'category': 'All',
    'description': """
    Point Of Sale Discount Features
    """,
    'data': [
        'security/ir.model.access.csv',
        'views/pos_config_views.xml',

    ],
    'application': True,
    'installable': True,
    'license': 'LGPL-3',
    'assets': {
        'point_of_sale._assets_pos': [
            'point_of_sale_feature/static/src/js/category_wise_discount.js',
        ],
    },
}
