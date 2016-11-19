from odoo import http




class Mymodule(http.Controller):
    @http.route('/mymodule/mymodule/', auth='public')
    def index(self, **kw):
        return "Hello, world"

"""
class Mymodule(http.Controller):
    @http.route('/mymodule/mymodule/', auth='public')
    def index(self, **kw):
        return http.request.render("mymodule.index",{'fruits':['apple','banana','pear']})


"""