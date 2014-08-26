# -*- coding: utf-8 -*-
import logging
import cgi
import os
import urllib
import datetime
import webapp2
import jinja2

from google.appengine.ext import ndb
from google.appengine.api import users
import utils

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

guestbook_key = ndb.Key('Guestbook', 'default_guestbook')

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'
TYPE_ITEM = [u'针', u'铊', u'钉', u'片']

def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
    """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
    return ndb.Key('Guestbook', guestbook_name)

class Greeting(ndb.Model):
  author = ndb.UserProperty()
  content = ndb.StringProperty(indexed=False)
  date = ndb.DateTimeProperty(auto_now_add=True)

class Account(ndb.Model):
  username = ndb.StringProperty()
  power = ndb.StringProperty()

class Itme(ndb.Model):
  code_id = ndb.StringProperty()
  price = ndb.FloatProperty()
  name = ndb.StringProperty()
  type_itme = ndb.StringProperty(choices=TYPE_ITEM)

class IndexPage(webapp2.RequestHandler):
    def get(self):
      user = users.get_current_user()
      if user:
        welcome_word = user.nickname() + ' back'
        url_linktext = 'Logout'
        url = users.create_logout_url(self.request.uri)
        account = Account.query(Account.username == user.nickname()).get()
        if account:
          if account.power == 'editor':
            is_editor = True
            welcome_word = 'Editor ' + user.nickname() + ' back'
        else:
          new_user = Account(username=user.nickname(), power='normal')
          new_user.put()
          welcome_word = user.nickname() + ' visit my site by first time'
      else:
        welcome_word = 'you'
        url = users.create_login_url(self.request.uri)
        url_linktext = 'Login'
      template_values = {
          'welcome_word': welcome_word,
          'url': url,
          'url_linktext': url_linktext,
      }
      template = JINJA_ENVIRONMENT.get_template('index.html')
      self.response.write(template.render(template_values))

class GuestbookPage(webapp2.RequestHandler):

    def get(self):
        guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)
        greetings_query = Greeting.query(
            ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
        greetings = greetings_query.fetch(10)
        user = users.get_current_user()
        if user:
          url = users.create_logout_url(self.request.uri)
          url_linktext = 'Logout'
        else:
          url = users.create_login_url(self.request.uri)
          url_linktext = 'Login'

        template_values = {
            'greetings': greetings,
            'guestbook_name': urllib.quote_plus(guestbook_name),
            'url': url,
            'url_linktext': url_linktext,
        }

        template = JINJA_ENVIRONMENT.get_template('guesbook.html')
        self.response.write(template.render(template_values))

class Guestbook(webapp2.RequestHandler):
    def post(self):
        guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)
        greeting = Greeting(parent=guestbook_key(guestbook_name))

        if users.get_current_user():
            greeting.author = users.get_current_user()

        greeting.content = self.request.get('content')
        greeting.put()

        query_params = {'guestbook_name': guestbook_name}
        self.redirect('/?' + urllib.urlencode(query_params))

application = webapp2.WSGIApplication([
    ('/', IndexPage),
    ('/guestbook', GuestbookPage),
    ('/sign', Guestbook),
], debug=True)

