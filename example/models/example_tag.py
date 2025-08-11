# -*- coding: utf-8 -*-

from odoo import fields,models

class ExampleTag(models.Model):
    """Tag creation model"""
    _name = 'example.tag'
    _description = 'Example Tags'
    _order = 'id desc'

    name = fields.Char('Tag name', help='Tag name creation')
    color = fields.Integer('Color', help='Color code of the specific tag')

    """This is the sql constraints for the unique tag name creation"""
    _sql_constraints = [
        ('name_unique', 'unique(name)', "The property tag must be unique"),
    ]



