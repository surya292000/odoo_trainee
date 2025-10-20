from odoo import models, fields, api, _


class ResPartner(models.Model):
    _inherit = 'purchase.order'

    @api.model
    def create_activity_for_delayed_po(self):
        delayed_po = self.env['purchase.order'].search([
            ('state', 'in', ('purchase', 'done')),
            ('date_planned', '<', fields.Datetime.now()),
        ])
        activity_type_todo_id = self.env.ref('mail.mail_activity_data_todo').id
        for po in delayed_po:
            existing_activity = self.env['mail.activity'].search([
                ('res_id', '=', po.id),
                ('res_model', '=', 'purchase.order'),
                ('activity_type_id', '=', activity_type_todo_id)
            ])
            if not existing_activity:
                activity_type = self.env.ref('mail.mail_activity_data_todo')
                summary = 'Delayed Purchase Order'
                note = f'The purchase order for vendor {po.partner_id.name} is delayed. Check with the supplier.'

                po.activity_schedule(
                    activity_type_id=activity_type.id,
                    summary=summary,
                    note=note,
                    user_id=po.user_id.id or self.env.user.id,
                )
                manager_group = self.env.ref('purchase.group_purchase_manager', raise_if_not_found=False)
                if manager_group and manager_group.users:
                    po.message_post(
                        body=_(
                            "Purchase Order <b>%s</b> for vendor <b>%s</b> is delayed.<br/>"
                            "Expected delivery date was <b>%s</b>."
                        ) % (po.name, po.partner_id.name, po.date_planned.strftime('%Y-%m-%d')),
                        partner_ids=manager_group.users.mapped('partner_id').ids,
                        subtype_xmlid='mail.mt_comment',
                    )
        return True
