# -*- coding: utf-8 -*-
{
    'name': "Property Management",
    'depends': ['base', 'mail', 'sale'],
    'data': ["security/ir.model.access.csv",
             "data/ir_sequence_data.xml",
             "data/property_facilities_data.xml",
             "data/property_details_datas.xml",
             "views/property_facility_views.xml",
             "views/property_details_views.xml",
             "views/property_rental_lease_views.xml",
             "views/property_rental_lease_lines_views.xml",
             "views/res_partner_views.xml",
             "views/menu.xml"
             ],
    'application': True,
    "sequence": 1
}
