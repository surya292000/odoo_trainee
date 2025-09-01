from odoo import models, fields
from odoo.exceptions import ValidationError


class RentLeaseReportWizard(models.TransientModel):
    _name = "rent.lease.report.wizard"
    _description = "Rent/Lease Report Wizard"

    from_date = fields.Date(string="From Date", required=True)
    to_date = fields.Date(string="To Date", required=True)
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
        """Fetch data using SQL query based on wizard filters"""
        query = f"""
            SELECT p.id AS rental_lease_id, pr.name AS property,pr.owner_id AS owner_id, p.price AS amount, 
            r.name AS owner_name, p.rental_type AS type, p.tenant_id AS tenant_id, p.states AS state,
            rs.name AS tenant_name,p.start_date AS start_date,p.end_date AS end_date
            FROM property_rental_lease_lines pl
            INNER JOIN property_rental_lease p ON p.id = pl.rental_id
            INNER JOIN property_details pr ON pr.id = pl.property_id
            INNER JOIN res_partner r ON r.id = pr.owner_id
            INNER JOIN res_partner rs ON rs.id = p.tenant_id
            where {self.env.company.id} = p.company_id """

        if self.rental_type:
            query += f"""and p.rental_type = '{self.rental_type}'"""
        if len(self.tenant_ids)==1:
            query += f"""and p.tenant_id = '{self.tenant_ids.id}'"""
        elif len(self.tenant_ids)>1:
            query += f""" and p.tenant_id in {tuple(self.tenant_ids.ids)} """
        if len(self.property_ids)==1:
            query += f"""and pl.property_id = '{self.property_ids.id}'"""
        elif len(self.property_ids)>1:
            query += f"""and pl.property_id in {tuple(self.property_ids.ids)} """
        if self.owner_id:
            query += f"""and pr.owner_id = '{self.owner_id.id}'"""
        if self.from_date and self.to_date:
            if self.from_date > self.to_date:
                raise ValidationError("Date not appropriate")
            # else:
            #     query += f"""and p.start_date >= '{self.from_date}' and p.end_date >= '{self.to_date}'"""
        if self.from_date:
            query += f"""and p.start_date >= '{self.from_date}'"""
        if self.to_date:
            query += f"""and p.end_date <= '{self.to_date}'"""
        print('query', query)

        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        # print(report, 'report')
        data ={"report": report}
        # print(data, 'data')
        return data

    def action_print_report(self):
        """Button action to generate PDF report"""
        data = self.data_fetch()
        # print(data,'data')
        # if not data['report']:
        #     raise ValidationError("No data matches your condition")
        return self.env.ref("property_management.action_property_rental_lease_report").report_action(None, data=data)