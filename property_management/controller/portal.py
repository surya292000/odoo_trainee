from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal


class PropertyPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'portal_property' in counters:
            values['portal_property'] = request.env['property.rental.lease'].sudo().search_count([])
        return values

    @http.route(['/property', '/property/page/<int:page>'], type='http', auth="user", website=True)
    def portal_property(self, search=None, search_in='All'):
        searchbar_inputs = {
            'All': {'label': 'All', 'input': 'All', 'domain': []},
            'Property': {'label': 'Property', 'input': 'Property', 'domain': [('property_ids.property_id.name', 'ilike', search)]},
            'Rental Type': {'label': 'Rental Type', 'input': 'Rental Type', 'domain': [('rental_type', 'ilike', search)]},
        }

        search_domain = searchbar_inputs.get(search_in, searchbar_inputs['All'])['domain']
        domain = [('tenant_id', '=', request.env.user.partner_id.id)] + search_domain

        properties = request.env['property.rental.lease'].sudo().search(domain)

        return request.render('property_management.portal_my_home_property_views', {
            'property': properties,
            'page_name': 'property',
            'search': search,
            'search_in': search_in,
            'searchbar_inputs': searchbar_inputs,
        })
