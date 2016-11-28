# -*- coding: utf-8 -*-
from odoo import http

# class To-doApplication(http.Controller):
#     @http.route('/to-do_application/to-do_application/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/to-do_application/to-do_application/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('to-do_application.listing', {
#             'root': '/to-do_application/to-do_application',
#             'objects': http.request.env['to-do_application.to-do_application'].search([]),
#         })

#     @http.route('/to-do_application/to-do_application/objects/<model("to-do_application.to-do_application"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('to-do_application.object', {
#             'object': obj
#         })