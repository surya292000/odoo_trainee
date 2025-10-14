from datetime import date, timedelta

from odoo import models, api, fields

class ProjectTask(models.Model):
    _inherit = 'project.task'

    @api.model
    def date_deadline(self):
        print('hai')
        for task in self:
            if task.stage_id and task.stage_id.default_duration_days:
                task.date_deadline = task.stage_id.default_duration_days
            else:
                task.date_deadline = False

    # @api.onchange('stage_id')
    # def _onchange_stage_id(self):
    #     if self.stage_id and self.stage_id.default_duration_days:
    #         self.date_deadline = self.stage_id.default_duration_days
    #     else:
    #         self.date_deadline = False  # Or a default valu



    # def set_deadline(self):
    #     print('haiii')
    #     for task in self:
    #         print(task, 'task')
    #         print(task.stage_id.default_duration_days, 'task.stage_id.default_duration_days')
    #         if task.stage_id and task.stage_id.default_duration_days:
    #             print(task.stage_id, 'task.stage_id')
    #             task.date_deadline = date.today() + timedelta(days=task.stage_id.default_duration_days)
    #         else:
    #             task.date_deadline = False
