# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class to-do_application(models.Model):
#     _name = 'to-do_application.to-do_application'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100
#--------------
#---------------------------
class TodoTask(models.Model):
	_name = 'todo.task'
	name = fields.Char('Description', required=True)
	is_done = fields.Boolean('Done?')
	active = fields.Boolean('Active?', default=True)
	