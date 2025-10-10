from datetime import date, timedelta

from odoo import models, api

class ProjectTaskStage(models.Model):
    _inherit = 'project.task'

    
    def set_deadline(self):
        print('haiii')
        for task in self:
            print(task, 'task')
            print(task.stage_id.default_duration_days, 'task.stage_id.default_duration_days')
            if task.stage_id and task.stage_id.default_duration_days:
                print(task.stage_id, 'task.stage_id')

                task.date_deadline = date.today() + timedelta(days=task.stage_id.default_duration_days)
            else:
                task.date_deadline = False
