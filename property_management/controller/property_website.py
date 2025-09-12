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
        # quantity = post.get('total_days')
        # print(quantity,'quantity')
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
            # 'total_days' : quantity,
            'property_ids': [Command.create({'property_id': property_id})],
        })
        return request.render('property_management.customer_success_template', {
            'lease': lease,
        })

    @route('/material/submit', type='json', auth='public', website=True)
    def request_submit(self, **post):
        """
        Handles the material request submission dynamically based on field types.
        """
        print('post', post)
        model_name = 'property.rental.lease'
        model_fields = request.env['ir.model.fields'].sudo().search([('model', '=', model_name)])
        values = {}
        for key, val in post.items():
            field = model_fields.filtered(lambda f: f.name == key)
            if not field:
                continue
            # Process data based on field type
            if field.ttype == 'many2one':
                val = int(val) if val else False
            elif field.ttype == 'one2many':
                relation_fields = request.env['ir.model.fields'].sudo().search([('model', '=', field.relation)])
                one2many_lines = []
                for line in val:
                    line_data = {}
                    for sub_key, sub_val in line.items():
                        sub_field = relation_fields.filtered(lambda f: f.name == sub_key)
                        if sub_field:
                            if sub_field.ttype == 'many2one':
                                sub_val = int(sub_val) if sub_val else False
                            elif sub_field.ttype in ['integer', 'float']:
                                sub_val = float(sub_val) if sub_val else 0
                            elif sub_field.ttype == 'boolean':
                                sub_val = str(sub_val).lower() in ['true', '1', 'yes']
                        line_data[sub_key] = sub_val
                    one2many_lines.append((0, 0, line_data))
                val = one2many_lines
            values[key] = val
        # Create record
        record = request.env[model_name].sudo().create(values)
        print('record', record)
        return {'success': True, 'record_id': record.id}

    # @route('/material/submit', type='json', auth='public', website=True, csrf=False)
    # def request_submit(self, **post):
    #     """
    #     Handles the material request submission dynamically based on field types.
    #     """
    #     print('post', post)
    #     values = {}
    #
    #     for key, val in post.items():
    #         if key == "property_ids":  # special handling for one2many
    #             one2many_lines = []
    #             for line in val:
    #                 line_data = {
    #                     'property_id': int(line.get('property')) if line.get('property') else False,
    #                     # 'total_days': int(line.get('quantity') or 0),
    #                     'rental_type': line.get('rental_type') or False,
    #                 }
    #                 one2many_lines.append((0, 0, line_data))
    #             values['property_ids'] = one2many_lines
    #         else:
    #             values[key] = val
    #     # Create record
    #     record = request.env['property.rental.lease'].sudo().create(values)
    #     print('record created:', record)
    #     return {'success': True, 'record_id': record.id}
        # return request.render('property_management.customer_success_template', {
        #     'values': values,
        # })

    # lease = request.env['property.rental.lease'].sudo().create({
    #     'tenant_id': partner.id,
    #     'rental_type': rental_type,
    #     'start_date': start_date,
    #     'end_date': end_date,
    #     # 'total_days' : quantity,
    #     'property_ids': [Command.create({'property_id': property_id})],
    # })
