import re
import sys
from webob import Request, Response, exc
var_regex = re.compile(r'''
    \{          # The exact character "{"
    (\w+)       # The variable name (restricted to a-z, 0-9, _)
    (?::([^}]+))? # The optional :regex part
    \}          # The exact character "}"
    ''', re.VERBOSE)

def template_to_regex(template):
    regex = ''
    last_pos = 0
    for match in var_regex.finditer(template):
        regex += re.escape(template[last_pos:match.start()])
        var_name = match.group(1)
        expr = match.group(2) or '[^/]+'
        expr = '(?P<%s>%s)' % (var_name, expr)
        regex += expr
        last_pos = match.end()
    regex += re.escape(template[last_pos:])
    regex = '^%s$' % regex
    return regex

def view(func):
    """Decorate views with this

    """
    def replacement(environ, start_response):
        req = Request(environ)
        try:
            resp = func(req, **req.urlvars)
        except exc.HTTPException, e:
            resp = e
        resp = Response(body=resp)
        return resp(environ, start_response)
    return replacement

def load_view(view):
    """ Import and return callable """
    smodule, sview = view.rsplit('.', 1)
    __import__(smodule)
    cmodule = sys.modules[smodule]
    return getattr(cmodule, sview)

class Router(object):
    def __init__(self):
        self.routes = []

    def add(self, template, view, *vars):
        if callable(view):
            cview = view
        elif isinstance(view, basestring):
            cview = load_view(view)
        else:
            raise ValueError("Only string or callable are allowed for route "
                             "views")
        self.routes.append((re.compile(template_to_regex(template)), cview,
                            vars, ))

    def __call__(self, environ, start_response):
        req = Request(environ)
        for regex, cview, vars in self.routes:
            match = regex.match(req.path_info)
            if match:
                req.urlvars = match.groupdict()
                req.urlvars.update(vars)
                return cview(environ, start_response)
        return exc.HTTPNotFound()(environ, start_response)
