#!/usr/bin/env python
import sys
from wsgiref.simple_server import make_server
from utils import Router
from config import ROUTES, PORT

if __name__ == '__main__':
    router = Router()
    for route in ROUTES:
        router.add(*route)
    server = make_server('', PORT, router)
    try:
        print "Serving on :%s" % (PORT)
        server.serve_forever()
    except KeyboardInterrupt:
        print "Shutting down"
        sys.exit(1)
