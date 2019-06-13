#!/home/posdoc/.pyenv/versions/anaconda3-5.3.1/bin/python
from wsgiref.handlers import CGIHandler
from index import app
CGIHandler().run(app)

