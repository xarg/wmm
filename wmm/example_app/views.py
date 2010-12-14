from .utils import view

@view
def index(request):
    return 'Hello world'
