import os

from paste.deploy import loadapp
from paste import httpserver

application = loadapp('config:production.ini', relative_to='.')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    httpserver.serve(application, host='0.0.0.0', port=port)
