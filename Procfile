web: python setup.py develop && gunicorn -k gevent --bind=$HOST:$PORT --workers=3 --max-requests=250 wsgi
