from odoo import fields, models
class PropertyReportWizard(models.TransientModel):


   _name = 'property.report.wizard'
   _description = "Property Report Wizard"

   from_date = fields.Datetime(string="From Date")
   to_date = fields.Datetime(string="To Date")
   states = fields.Selection([
       ('Draft', 'Draft'),
       ('To Approve', 'To Approve'),
       ('Confirmed', 'Confirmed'),
       ('Closed', 'Closed'),
       ('Returned', 'Returned'),
       ('Expired', 'Expired'),
   ], string="Status", default='Draft', tracking=True)
   rental_type = fields.Selection([('Rent', 'Rent'), ('Lease', 'Lease')], String="Type", required=True)
   owner_id = fields.Many2one("res.partner", string="Owner")
   tenant_id = fields.Many2one("res.partner", string="Tenant", required=True)
   property = fields.Char(string="Property", required=True)