from odoo import http
from odoo.http import request


class WebFormController(http.Controller):
   @http.route('/webform', auth='public', website=True)
   def display_web_form(self, **kwargs):
       # property = request.env['property.rental.lease'].sudo().search([])
       # owner = request.env['res.partner'].sudo().search([])
       # datas = {
       #     'property': property,
       #     'owner': owner,
       # }
       return request.render('property_management.customer_form_template')

   @http.route(['/website/customer/create'], type='http', auth="public", methods=['POST'], website=True, csrf=True)
   def create_customer(self, **post):
       request.env['property.rental.lease'].sudo().create({
           'property_ids': post.get('property_ids'),
           'rental_type': post.get('rental_type'),
           'start_date': post.get('start_date'),
           'tenant_id': post.get('tenant_id')
           # 'customer_rank': 1,
       })
       return request.render('property_management.customer_success_template')

   @http.route('/webform/submit', type='http', auth='public', website=True, methods=['POST'])
   def handle_web_form_submission(self, **post):
       request.env['property.rental.lease'].sudo().create({
           'name': post.get('name'),
           # 'phone': post.get('phone'),
           # 'email': post.get('email'),
       })
       return request.redirect('/thank-you-page')
