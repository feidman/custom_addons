# -*- coding: utf-8 -*-
from odoo import http

# class MultiuserTodoApp(http.Controller):
#     @http.route('/multiuser_todo_app/multiuser_todo_app/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/multiuser_todo_app/multiuser_todo_app/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('multiuser_todo_app.listing', {
#             'root': '/multiuser_todo_app/multiuser_todo_app',
#             'objects': http.request.env['multiuser_todo_app.multiuser_todo_app'].search([]),
#         })

#     @http.route('/multiuser_todo_app/multiuser_todo_app/objects/<model("multiuser_todo_app.multiuser_todo_app"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('multiuser_todo_app.object', {
#             'object': obj
#         })