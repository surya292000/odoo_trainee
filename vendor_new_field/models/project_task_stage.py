from odoo import fields, models

class ProjectTaskStage(models.Model):
    _inherit = 'project.task.type'

    default_duration_days = fields.Integer(string='Default Duration (days)')
    is_complete = fields.Boolean(string="Completed")
