# -*- coding: utf-8 -*-
from odoo import http, Command
from odoo.http import request, route


class WebFormController(http.Controller):
    @http.route('/webform', type='http', auth='user', website=True)
    def display_web_form(self, **kwargs):
        properties = request.env['property.details'].sudo().search([])
        rental_type_field = request.env['property.rental.lease']._fields['rental_type']
        quantity = request.env['property.rental.lease']._fields['total_days']
        rental_types = rental_type_field.selection
        return request.render('property_management.customer_form_template', {
            'properties': properties,
            'rental_types': rental_types,
            'quantity': quantity,
        })

    # @http.route('/website/customer/create', type='http', auth='public',
    #             website=True, csrf=False)
    # def create_customer(self, **post):
    #     partner = request.env.user.partner_id
    #     property_val = post.get('property_id')
    #     rental_type = post.get('rental_type')
    #     start_date = post.get('start_date')
    #     end_date = post.get('end_date')
    #
    #     if not property_val:
    #         return request.redirect('/webform?error=Please select a property')
    #     if not rental_type:
    #         return request.redirect('/webform?error=Please select a rental type')
    #     if start_date and end_date and start_date > end_date:
    #         return request.redirect('/webform?error=End date cannot be before start date')
    #
    #     property_id = int(property_val)
    #     lease = request.env['property.rental.lease'].sudo().create({
    #         'tenant_id': partner.id,
    #         # 'rental_type': rental_type,
    #         'start_date': start_date,
    #         'end_date': end_date,
    #         'property_ids': [Command.create({'property_id': property_id})],
    #     })
    #     return request.render('property_management.customer_success_template', {
    #         'lease': lease,
    #     })

    @route('/property-property', type='json', auth='public', website=True)
    def get_property_data(self, **post):
        """
        Returns property data for calculations (rent, lease prices, owner info)
        """
        properties = request.env['property.details'].sudo().search([])
        property_data = {}

        for prop in properties:
            property_data[str(prop.id)] = {
                'owner': prop.owner_id.name if prop.owner_id else 'N/A',
                'rent': prop.rent or 0,
                'lease': prop.legal_amount or 0,
                'name': prop.name or '',
            }

        # print('Property data:', property_data)
        return property_data

    @route('/material/submit', type='json', auth='public', website=True)
    def request_submit(self, abc, data, **post):
        print('sdfghjknbvcxcvbnmbgvfcdsdfghj')
        """create a record on backend"""
        order = []
        print('ggggg', abc)
        # for rec in data:
        print('ggggg2',data)
        #     dicts = {
        #         'property_id': rec['property_id'],
        #         'rental_type': rec['rental_type']
        #     }
        #     order.append(dicts)
        # print(data, 'data')
        # print(user_data, 'user')
        # print(post, 'post')
        # print('post', post)

        partner = request.env.user.partner_id.id
        print(partner,'partner')
        print(data[0]['rental_type'], 'data type')

        # property_val = post.get('property_id')
        # print('property_val',property_val)
        # rental_type = post.get('rental_type')
        # print(rental_type,'rental_type')
        # start_date = post.get('start_date')
        # print('start_date',start_date)
        # end_date = post.get('end_date')
        record = request.env['property.rental.lease'].sudo().create({
            'tenant_id': partner,
            'rental_type': data[0]['rental_type'],
            # 'start_date': start_date,
            # 'end_date': end_date,
            'property_ids': [Command.create(data)]
        })
        print(record,'record')
        return record
        # return True
