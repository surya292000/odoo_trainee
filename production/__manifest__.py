# -*- coding: utf-8 -*-
{
    'name': "Production",
    'depends': ['base', 'product'],
    'data': ["security/production_groups.xml",
             "security/ir.model.access.csv",
             "views/production_product_lines_views.xml",
             "views/production_product_views.xml",
             "views/menu.xml"
             ],
    'application': True,
    "sequence": 1
}
