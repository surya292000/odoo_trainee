from odoo import models, fields, api


class ProjectProject(models.Model):
    _inherit = 'project.project'

    progress = fields.Float(string="Progress %")

    @api.depends('task_ids')
    def _compute_field_progress(self):
        for project in self:
            total_tasks = len(project.task_ids)
            if total_tasks > 0:
                completed_tasks = sum()
                project.progress_percentage = (completed_tasks / total_tasks) * 100
        pass

