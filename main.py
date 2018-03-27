"""
Server entry point to use gunicorn
"""
#!/usr/bin/env python

import os
from src.routes import APP as application

if __name__ == "__main__":
    debug = os.environ.get("MODE", True)

    if debug == "production":
        debug = False
    else:
        debug = True

    application.run(host='0.0.0.0',port=8888, debug=debug)
