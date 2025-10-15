from odoo import models, fields, _, api
from odoo.exceptions import UserError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    approval_request_id = fields.Many2one('product.approval', string="Approval Request", readonly=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending Approval'),
        ('approved', 'Approved')
    ], string='Status', default='draft', copy=False)

    @api.model
    def create(self, vals):
        # Create the product first
        product = super(ProductTemplate, self).create(vals)

        # Define the manager to notify (e.g., from settings or a specific user)
        # For simplicity, let's hardcode the manager for this example.
        # In a real-world scenario, you might find this dynamically.
        manager_user = self.env.ref('base.user_admin')  # The admin user

        if product and self.env.user.id != manager_user.id:
            # Create a product approval request
            approval_request = self.env['product.approval'].create({
                'name': _('Approval Request for Product: %s', product.name),
                'product_id': product.id,
                'requester_id': self.env.user.id,
                'manager_id': manager_user.id,
                'state': 'pending',
            })

            # Link the approval request to the product and change its state
            product.write({
                'approval_request_id': approval_request.id,
                'state': 'pending',
            })

            # Notify the manager using the Chatter system
            product.message_post_with_view(
                'my_product_approval.mail_template_product_approval',
                subtype_id=self.env.ref('mail.mt_note').id,
                partner_ids=[manager_user.partner_id.id],
                values={'product': product, 'approval_request': approval_request}
            )

        return product
