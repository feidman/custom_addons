# -*- coding: utf-8 -*-
from odoo import http

# class TaskApplication(http.Controller):
#     @http.route('/task_application/task_application/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/task_application/task_application/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('task_application.listing', {
#             'root': '/task_application/task_application',
#             'objects': http.request.env['task_application.task_application'].search([]),
#         })

#     @http.route('/task_application/task_application/objects/<model("task_application.task_application"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('task_application.object', {
#             'object': obj
#         })