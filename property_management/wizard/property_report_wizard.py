from odoo import fields, models


class RentLeaseReportWizard(models.TransientModel):
    _name = 'rent.lease.report.wizard'
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
    tenant_id = fields.Many2one("res.partner", string="Tenant")
    owner_id = fields.Many2one("res.partner", string="Owner")
    rental_type = fields.Selection([
        ('rent', 'Rent'),
        ('lease', 'Lease')
    ], string="Type")
    property_id = fields.Many2one("property.details", string="Property")

    def action_print_report(self):
        query = """
            SELECT 
                pl.states AS state,
                tenant.name AS tenant,
                owner.name AS owner,
                pl.rental_type AS type,
                pd.name AS property
            FROM property_rental_lease_lines AS pll
            INNER JOIN property_rental_lease AS pl ON pl.id = pll.rental_id
            INNER JOIN res_partner AS tenant ON tenant.id = pl.tenant_id
            INNER JOIN property_details AS pd ON pd.id = pll.property_id
            INNER JOIN res_partner AS owner ON owner.id = pd.owner_id
        """

        conditions = []

        if self.from_date and self.to_date:
            conditions.append("pl.start_date >= '%s' AND pl.end_date <= '%s'" % (self.from_date, self.to_date))
        if self.state:
            conditions.append("pl.states = '%s'" % self.state)
        if self.tenant_id:
            conditions.append("pl.tenant_id = %s" % self.tenant_id.id)
        if self.owner_id:
            conditions.append("pd.owner_id = %s" % self.owner_id.id)
        if self.rental_type:
            conditions.append("pl.rental_type = '%s'" % self.rental_type)
        if self.property_id:
            conditions.append("pll.property_id = %s" % self.property_id.id)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()

        data = {'date': self.read()[0], 'report': report}
        return self.env.ref('your_module_name.action_property_rental_lease_report').report_action(None, data=data)

