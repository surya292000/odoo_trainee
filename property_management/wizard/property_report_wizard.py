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
        return self.env.ref(
            'property_management.action_property_rental_lease_report'
        ).report_action(self)
