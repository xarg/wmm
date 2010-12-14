import os
ROOT_PATH = os.path.abspath(os.path.dirname(__file__)) + '/'
DEBUG = True
PORT = 8080

DATABASES = {
    'default': {
        'TYPE': 'mongoengine',
        'HOST': '',
        'NAME': '',
        'USER': '',
        'PASS': ''
    }
}
TEMPLATES = (
    ROOT_PATH + 'templates/'
)

LOGS = ROOT_PATH + 'logs/'

MEDIA_URL = ''

ROUTES = (
    (r'/', 'example_app.views.index', ),
)
