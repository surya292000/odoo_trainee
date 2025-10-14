from odoo import models, fields, api


class ProjectProject(models.Model):
    _inherit = 'project.project'

    progress = fields.Float(string="Progress %", compute='_compute_field_progress')

    @api.depends('task_ids.stage_id')
    def _compute_field_progress(self):
        for project in self:
            total_tasks = len(project.task_ids)
            if total_tasks > 0:
                completed_tasks = len(project.task_ids.filtered(lambda rec: rec.stage_id.is_complete))
                project.progress = (completed_tasks / total_tasks)
