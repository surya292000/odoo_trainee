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

        query = f"""SELECT p.id AS rental_lease_id, pr.name AS property, pr.owner_id AS owner_id, r.name AS owner_name,
                p.price AS amount, p.rental_type AS rental_type, CASE WHEN p.rental_type = 'rent' THEN 'Rent' 
                WHEN p.rental_type = 'lease' THEN 'Lease' ELSE 'None' END AS type, p.tenant_id AS tenant_id, 
                rs.name AS tenant_name, p.states AS state, p.start_date AS start_date, p.end_date AS end_date
                FROM property_rental_lease_lines pl
                INNER JOIN property_rental_lease p ON p.id = pl.rental_id
                INNER JOIN property_details pr ON pr.id = pl.property_id
                INNER JOIN res_partner r ON r.id = pr.owner_id
                INNER JOIN res_partner rs ON rs.id = p.tenant_id
                WHERE p.company_id = {self.env.company.id}"""

        if self.rental_type:
            query += f" AND p.rental_type = '{self.rental_type}'"
        if len(self.tenant_ids) == 1:
            query += f" AND p.tenant_id = {self.tenant_ids.id}"
        elif len(self.tenant_ids) > 1:
            query += f" AND p.tenant_id IN {tuple(self.tenant_ids.ids)}"
        if len(self.property_ids) == 1:
            query += f" AND pl.property_id = {self.property_ids.id}"
        elif len(self.property_ids) > 1:
            query += f" AND pl.property_id IN {tuple(self.property_ids.ids)}"
        if self.owner_id:
            query += f" AND pr.owner_id = {self.owner_id.id}"
        if self.state:
            query += f" AND p.state = '{self.state}'"
        if self.from_date and self.to_date and self.from_date > self.to_date:
            raise ValidationError("From Date cannot be after To Date.")
        if self.from_date:
            query += f" AND p.start_date >= '{self.from_date}'"
        if self.to_date:
            query += f" AND p.end_date <= '{self.to_date}'"
        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        return {"records": report}

    def action_print_report(self):
        """Button action to generate PDF report"""
        data = self.data_fetch()
        if not data['records']:
            raise ValidationError("No records matches your condition")
        return self.env.ref("property_management.action_property_rental_lease_report").report_action(None, data=data)
