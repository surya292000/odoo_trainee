# -*- coding: utf-8 -*-
import io
import json
import xlsxwriter
from odoo.tools import json_default
from odoo import models, fields
from odoo.exceptions import ValidationError


class RentLeaseReportWizard(models.TransientModel):
    _name = "rent.lease.report.wizard"
    _description = "Rent/Lease Report Wizard"

    from_date = fields.Date(string="From Date")
    to_date = fields.Date(string="To Date")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('to_approve', 'To Approve'),
        ('confirmed', 'Confirmed'),
        ('closed', 'Closed'),
        ('returned', 'Returned'),
        ('expired', 'Expired'),
    ], string="State")
    tenant_ids = fields.Many2many("res.partner", string="Tenant")
    owner_id = fields.Many2one("res.partner", string="Owner")
    rental_type = fields.Selection([
        ('rent', 'Rent'),
        ('lease', 'Lease')
    ], string="Type")
    property_ids = fields.Many2many("property.details", string="Property")

    def data_fetch(self):
        """Fetch data using SQL query based on the wizard filters"""
        conditions = [f"p.company_id = {self.env.company.id}"]
        if self.rental_type:
            conditions.append(f"p.rental_type = '{self.rental_type}'")
        if len(self.tenant_ids) == 1:
            conditions.append(f"p.tenant_id = {self.tenant_ids.id}")
        elif len(self.tenant_ids) > 1:
            conditions.append(f"p.tenant_id IN {tuple(self.tenant_ids.ids)}")
        if len(self.property_ids) == 1:
            conditions.append(f"pl.property_id = {self.property_ids.id}")
        elif len(self.property_ids) > 1:
            conditions.append(f"pl.property_id IN {tuple(self.property_ids.ids)}")
        if self.owner_id:
            conditions.append(f"pr.owner_id = {self.owner_id.id}")
        if self.state:
            conditions.append(f"p.state = '{self.state}'")
        if self.from_date and self.to_date and self.from_date > self.to_date:
            raise ValidationError("From Date cannot be after To Date.")
        if self.from_date:
            conditions.append(f"p.start_date >= '{self.from_date}'")
        if self.to_date:
            conditions.append(f"p.end_date <= '{self.to_date}'")
        where_clause = " AND ".join(conditions)
        query = f""" SELECT p.name AS rental_lease_id, pr.name AS property, pr.owner_id AS owner_id, r.name AS owner_name,
                p.price AS amount, p.rental_type AS rental_type, CASE WHEN p.rental_type = 'rent' THEN 'Rent' 
                WHEN p.rental_type = 'lease' THEN 'Lease' ELSE 'None' END AS type, 
                p.tenant_id AS tenant_id, rs.name AS tenant_name, 
                p.states AS state, p.start_date AS start_date, p.end_date AS end_date
                FROM property_rental_lease_lines pl
                INNER JOIN property_rental_lease p ON p.id = pl.rental_id
                INNER JOIN property_details pr ON pr.id = pl.property_id
                INNER JOIN res_partner r ON r.id = pr.owner_id
                INNER JOIN res_partner rs ON rs.id = p.tenant_id
                WHERE {where_clause}"""

        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        return {"records": report}

    def action_print_report(self):
        """Button action to generate PDF report"""
        data = self.data_fetch()
        if not data['records']:
            raise ValidationError("No records matches your condition")
        return self.env.ref("property_management.action_property_rental_lease_report").report_action(None, data=data)

    def action_print_xlsx(self):
        data = self.data_fetch()
        if not data['records']:
            raise ValidationError("No records matches your condition")
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'rent.lease.report.wizard',
                     'options': json.dumps(data,
                                           default=json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Property Excel Report',
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response):
        output = io.BytesIO()
        report = data['records']
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        cell_format = workbook.add_format(
            {'font_size': '12px', 'align': 'center'})
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '20px'})
        txt = workbook.add_format({'font_size': '10px', 'align': 'center'})
        sheet.merge_range('B4:S5', 'EXCEL REPORT', head)
        sheet.write('H11', 'Property', cell_format)
        sheet.write('I11', 'Owner', cell_format)
        sheet.write('J11', 'Property Type', cell_format)
        sheet.write('K11', 'Tenant', cell_format)
        sheet.write('L11', 'Start Date', cell_format)
        sheet.write('M11', 'End Date', cell_format)
        sheet.write('N11', 'Amount', cell_format)
        sheet.write('O11', 'State', cell_format)
        for i, row in enumerate(report,start=12):
            sheet.write(f'H{i}:', str(row['property']), txt)
            sheet.write(f'I{i}', str(row['owner_name']), txt)
            sheet.write(f'J{i}', str(row['type']), txt)
            sheet.write(f'K{i}', str(row['tenant_name']), txt)
            sheet.write(f'L{i}', str(row['start_date']), txt)
            sheet.write(f'M{i}', str(row['end_date']), txt)
            sheet.write(f'N{i}', str(row['amount']), txt)
            sheet.write(f'O{i}', str(row['state']), txt)
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
