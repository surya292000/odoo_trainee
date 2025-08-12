# -*- coding: utf-8 -*-
from odoo import api, Command, fields, models, _
from odoo.exceptions import UserError


class PropertyRentalLease(models.Model):
    _name = "property.rental.lease"
    _description = "Rented/Lease"
    _inherit = 'mail.thread'

    name = fields.Char(string='reference', readonly="1", default=lambda self: _('New'))
    property_ids = fields.One2many("property.rental.lease.lines",
                                   "rental_id", string="Property")
    rental_type = fields.Selection([('Rent', 'Rent'), ('Lease', 'Lease')], String="Type", required=True)
    tenant_id = fields.Many2one("res.partner", string="Tenant", required=True)
    amount = fields.Float('amount', related="property_ids.amount")
    price = fields.Float(string="Amount", compute="_compute_total", store=True)
    start_date = fields.Datetime(string="Start Date")
    end_date = fields.Datetime(string="End Date")
    states = fields.Selection([
        ('Draft', 'Draft'),
        ('Confirmed', 'Confirmed'),
        ('Closed', 'Closed'),
        ('Returned', 'Returned'),
        ('Expired', 'Expired'),
    ], string="Status",default='Draft', tracking=True)
    company_id = fields.Many2one("res.company", string="Company", default=1)
    total_days = fields.Integer(string="Total Days", compute="_compute_total_days", store=True)
    total_amount = fields.Float(string="Total Amount", compute="_compute_total_amount", store=True)
    attachment_ids = fields.Many2many('ir.attachment', compute='_compute_attachments')
    sale_order_id = fields.Many2one('sale.order', string="Related sale order")
    invoice_count = fields.Integer(string="Invoice count", compute="_compute_invoice_count")
    invoice_ids = fields.Many2many("account.move", string="Invoice IDs", copy=False)
    invoice_line_vals = fields.Char(string="Invoice line values")
    invoice_status = fields.Selection(
        selection=[('invoiced', 'Fully Invoiced'), ('partially_invoiced', 'Partially Invoiced'),
                   ('to_invoice', 'To Invoice'), ('paid', 'Paid'), ('partially_paid', 'Partially Paid')],
        string="Invoice Status",
        compute='_compute_invoice_status',
        store=True)
    sum_qty_remaining = fields.Integer(string="quantity remaining",default = 0)
    hide_invoice = fields.Boolean(string="Hide Invoice")
    active = fields.Boolean(string="Active", default = True)

    @api.depends("start_date", "end_date")
    def _compute_total_days(self):
        for record in self:
            """calculate total days"""
        if record.start_date and record.end_date:
            record.total_days = (record.end_date - record.start_date).days
        else:
             record.total_days = 0

    @api.depends("total_days", "price")
    def _compute_total_amount(self):
        for record in self:
             if record.rental_type == 'rent':
                record.total_amount = record.total_days * record.price

    @api.depends('property_ids.amount')
    def _compute_total(self):
        """calculate price"""
        for record in self:
            record.price = sum(line.amount for line in record.property_ids)

    @api.depends('invoice_ids.payment_state', 'invoice_ids.state', 'property_ids.order_line_ids',
                 'property_ids.invoiced_quantity')
    def _compute_invoice_status(self):
        qty_ordered_sum = sum(self.property_ids.mapped('quantity'))
        qty_invoiced_sum = sum(self.property_ids.mapped('invoiced_quantity'))
        self.sum_qty_remaining = qty_ordered_sum - qty_invoiced_sum
        if self.sum_qty_remaining == 0:
            self.hide_invoice = True
        else:
            self.hide_invoice = False
        if not self.invoice_ids:
            self.invoice_status = 'to_invoice'
        else:
            if qty_ordered_sum > qty_invoiced_sum:
                self.invoice_status = 'partially_paid' if self.invoice_ids.filtered(
                    lambda rec: rec.payment_state in ['partial', 'paid']) else 'partially_invoiced'
            else:
                if self.invoice_ids.filtered(lambda rec: rec.payment_state in ['partial', 'paid']):
                    self.invoice_status = 'paid' if all(
                        rec.payment_state == 'paid' for rec in self.invoice_ids.filtered(
                            lambda rec: rec.state == 'posted')) else 'partially_paid'
                elif not self.invoice_ids.filtered(lambda rec: rec.state == 'draft'):
                    self.invoice_status = 'invoiced'

    def _compute_invoice_count(self):
        """calculating the invoice count"""
        for record in self:
            record.invoice_count = self.env['account.move'].search_count([('id', '=', record.invoice_ids.ids)])

    @api.constrains('end_date')
    def _state_change(self):
        today = fields.Datetime.now()
        for rec in self:
            if today > rec.end_date:
                rec.states = 'Expired'

       # sequence creation
    @api.model
    def create(self, vals):
        """generating unique sequence number"""
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('property.rental') or _('New')
        return super(PropertyRentalLease, self).create(vals)

    # noinspection PyNoneFunctionAssignment
    def action_do_confirm(self):
        """action for confirm"""
        for record in self:
            """checking the required attachments"""
            attachments = self.env['ir.attachment'].search([
                ('res_model', '=', 'property.rental.lease'),
                ('res_id', '=', self.id)
            ])
            if not attachments:
                raise UserError("Please attach required attachments")
            record.states = 'Confirmed'
            for line in record.property_ids:
                if record.rental_type == 'Rent':
                    line.property_id.states = 'Rented'
                elif record.rental_type == 'Lease':
                    line.property_id.states = 'Leased'
                else:
                    line.property_id.states = 'Draft'

    def action_do_draft(self):
        """action for draft button"""
        self.states = "Draft"

    def action_do_close(self):
        """action for close button"""
        self.states = "Closed"

    def action_do_return(self):
        """action for return button"""
        self.states = "Returned"

    def action_do_expire(self):
        """action for expire button"""
        self.states = "Expired"

# function to create invoice
    def action_create_invoice(self):
        """action for invoice button"""
        ordered_quantity = self.total_days
        lines_to_invoice = []
        invoice = self.env['account.move']
        for line in self.property_ids:
            qty_invoiced = line.invoiced_quantity
            qty_remaining = ordered_quantity - qty_invoiced
            if qty_remaining > 0:
                draft_lines = line.order_line_ids.filtered(lambda inv: inv.move_id.state == 'draft')
                if draft_lines:
                    draft_lines.write({'quantity': qty_remaining})
                    invoice = draft_lines.mapped('move_id')
                else:
                    lines_to_invoice.append(Command.create({
                        'name': line.property_id.name,
                        'quantity': qty_remaining,
                        'price_unit': line.amount,
                        'property_lease_line_id': line.id,
                    }))
        if lines_to_invoice:
            """checking draft invoice"""
            invoice = self.invoice_ids.filtered(lambda d: d.state == 'draft' and d.move_type == 'out_invoice')
            if invoice:
                invoice.write({'invoice_line_ids': lines_to_invoice})
            else:
                """creating new invoice"""
                invoice = self.env['account.move'].create({
                    'partner_id': self.tenant_id.id,
                    'move_type': 'out_invoice',
                    'invoice_date': fields.Date.today(),
                    'invoice_line_ids': lines_to_invoice   #updating invoice lines in invoice lines
                })
                """linking property lines and invoice lines"""
                for lines in invoice.invoice_line_ids:
                    lines.property_lease_line_id.order_line_ids = [Command.link(lines.id)]
                self.write({'invoice_ids': [Command.link(invoice.id)]})
                body = _('The %s Invoice is created', self.name)
                self.message_post(body=body)
        if invoice:
            return {
                'name': 'Customer Invoice',
                'view_mode': 'form',
                'res_model': 'account.move',
                'res_id': invoice.id,
                'type': 'ir.actions.act_window',
            }

    def action_view_invoices(self):
        """action view for invoices"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoices',
            'res_model': 'account.move',
            'view_mode': 'list,form',
            'domain': [('id', 'in', self.invoice_ids.ids)],
            'context': {'create': False},
        }
