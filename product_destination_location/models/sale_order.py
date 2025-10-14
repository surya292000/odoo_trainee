from dateutil.relativedelta import relativedelta

from odoo import models, fields, api, Command
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    project_id = fields.Many2one('project.project',string='Project')

    is_empty_task = fields.Boolean(string='Is Empty Task', compute='_compute_partner_id', default=0)

    @api.depends('project_id')
    def _compute_partner_id(self):
        if len(self.project_id.task_ids) > 0:
            self.is_empty_task = True
        else:
            self.is_empty_task = False

    def button_to_create_task(self):
        print(self.project_id.task_ids)
        Task = self.env['project.task']

        lines = self.order_line
        for lin in lines:
            title_name = lin.product_id.name
            print(title_name, 'title_name')
        print(lines, 'lines')

        task = Task.create({
            'display_name' : self.name + ' - ' + self.partner_id.name,
            'user_ids' : self.env.user,
            # 'child_ids' : [Command.create({
            #     'name' : title_name,
            # })],
        })

        self.project_id.task_ids = task
        print(task, 'task')
        return task

