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
            'quantity' : quantity,
        })
    @http.route('/website/customer/create', type='http', auth='public',
                website=True, csrf=False)
    def create_customer(self, **post):
        partner = request.env.user.partner_id
        property_val = post.get('property_id')
        rental_type = post.get('rental_type')
        start_date = post.get('start_date')
        end_date = post.get('end_date')
        quantity = post.get('total_days')
        print(quantity,'quantity')
        if not property_val:
            return request.redirect('/webform?error=Please select a property')
        if not rental_type:
            return request.redirect('/webform?error=Please select a rental type')
        if start_date and end_date and start_date > end_date:
            return request.redirect('/webform?error=End date cannot be before start date')
        property_id = int(property_val)
        lease = request.env['property.rental.lease'].sudo().create({
            'tenant_id': partner.id,
            'rental_type': rental_type,
            'start_date': start_date,
            'end_date': end_date,
            'total_days' : quantity,
            'property_ids': [Command.create({'property_id': property_id})],
        })
        return request.render('property_management.customer_success_template', {
            'lease': lease,
        })




