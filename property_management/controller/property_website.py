# -*- coding: utf-8 -*-
from odoo import http, Command
from odoo.http import request, route


class WebFormController(http.Controller):
    @http.route('/web/list', type='http', auth='user', website=True)
    def display_web_list(self, search=None, search_in='All', **kwargs):
        searchbar_inputs = {
            'All': {'label': 'All', 'input': 'All', 'domain': []},
            'Property': {
                'label': 'Property',
                'input': 'Property',
                'domain': [('property_ids.property_id.name', 'ilike', search)] if search else []
            },
            'Rental Type': {
                'label': 'Rental Type',
                'input': 'Rental Type',
                'domain': [('rental_type', 'ilike', search)] if search else []
            },
        }

        search_domain = searchbar_inputs.get(search_in, searchbar_inputs['All'])['domain']
        domain = [('tenant_id', '=', request.env.user.partner_id.id)] + search_domain

        properties = request.env['property.rental.lease'].search(domain)
        print(properties,'properties')

        return request.render('property_management.property_record_list_view', {
            'property': properties,
            'page_name': 'property',
            'search': search,
            'search_in': search_in,
            'searchbar_inputs': searchbar_inputs,
        })

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

    @http.route('/website/customer/create', type='http', auth='public',
                website=True, csrf=False)
    def create_customer(self, **post):
        partner = request.env.user.partner_id
        property_val = post.get('property_id')
        rental_type = post.get('rental_type')
        start_date = post.get('start_date')
        end_date = post.get('end_date')

        if not property_val:
            return request.redirect('/webform?error=Please select a property')
        if not rental_type:
            return request.redirect('/webform?error=Please select a rental type')
        if start_date and end_date and start_date > end_date:
            return request.redirect('/webform?error=End date cannot be before start date')

        property_id = int(property_val)
        lease = request.env['property.rental.lease'].sudo().create({
            'tenant_id': partner.id,
            'start_date': start_date,
            'end_date': end_date,
            'property_ids': [Command.create({'property_id': property_id})],
        })
        return request.redirect('/customer/success?lease_id=%s' % lease.id)

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
        return property_data

    @http.route('/material/submit', type='json', auth='public', website=True, csrf=False)
    def request_submit(self, start=None, end=None, type=None, data=None, **post):
        partner = request.env.user.partner_id

        if not start:
            start = post.get('start')
        if not end:
            end = post.get('end')
        if not type:
            type = post.get('type')
        if not data:
            data = post.get('data')
        property_id = [val.get('property_id') for val in data if 'property_id' in val]
        if not property_id:
            return {"status": "error", "message": "No property selected"}

        lease = request.env['property.rental.lease'].sudo().create({
            'tenant_id': partner.id,
            'rental_type': type,
            'start_date': start,
            'end_date': end,
            'property_ids': [Command.create({'property_id': int(pid)}) for pid in property_id],
        })
        return {"status": "success", "lease_id": lease.id}

    @http.route('/customer/success', type='http', auth='user', website=True)
    def customer_success(self, lease_id=None, **kwargs):
        lease = None
        if lease_id:
            lease = request.env['property.rental.lease'].sudo().browse(int(lease_id))
        return request.render('property_management.customer_success_template', {
            'lease': lease,
        })