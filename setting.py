#-*- coding: utf-8 -*-
import os
import jinja2

TYPE_ITEM = [u'针', u'铊', u'钉', u'片', 'None']

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'