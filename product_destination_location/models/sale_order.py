from odoo import models, fields, api, Command, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    project_id = fields.Many2one('project.project', string='Project')
    is_empty_task = fields.Boolean(string='Is Empty Task', compute='_compute_partner_id', default=0)
    sub_task_count = fields.Integer(string="Sub Task Count")

    @api.depends('project_id')
    def _compute_partner_id(self):
        self.is_empty_task = len(self.project_id.task_ids) > 0

    def button_to_create_task(self):
        task = self.env['project.task'].create([{
            'display_name': self.name + ' - ' + self.partner_id.name,
            'user_ids': self.env.user,
            'project_id': self.project_id.id,
        }])
        self.sub_task_count = len(self.order_line)
        priority = self.order_line.sorted(lambda rec: rec.price_subtotal, reverse=True)
        for line in priority:
            title_name = line.product_id.name + ' - ' + str(line.product_uom_qty)
            task_name = len(task.child_ids.filtered(lambda tsk: tsk.name == title_name))
            if task_name > 0:
                raise ValidationError(_("This task have already created."))
            else:
                sub_task = task.write({
                        'child_ids': [Command.create({
                            'name': title_name,
                            'project_id': self.project_id.id,
                            'parent_id': task.id,
                        })]
                    })
            return sub_task
        return None

    def action_view_tasks(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Tasks',
            'res_model': 'project.task',
            'view_mode': 'kanban,form',
            'domain': [('project_id', '=', self.project_id.id)],
        }
