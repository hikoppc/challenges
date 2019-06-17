#!/home/posdoc/.pyenv/versions/anaconda3-5.3.1/bin/python

import cgitb
cgitb.enable()

from wsgiref.handlers import CGIHandler
from index import app
CGIHandler().run(app)
