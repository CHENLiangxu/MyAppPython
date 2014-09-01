# -*- coding: utf-8 -*-
import logging
import webapp2
import jinja2
import setting

from google.appengine.ext import ndb
from google.appengine.api import users

class Account(ndb.Model):
  username = ndb.StringProperty()
  power = ndb.StringProperty()

class IndexPage(webapp2.RequestHandler):
    def get(self):
      user = users.get_current_user()
      is_editor = False
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
        welcome_word = ''
        url = users.create_login_url(self.request.uri)
        url_linktext = 'Login'
      template_values = {
          'welcome_word': welcome_word,
          'url': url,
          'url_linktext': url_linktext,
          'is_editor': is_editor,
      }
      template = setting.JINJA_ENVIRONMENT.get_template('template/index.html')
      self.response.write(template.render(template_values))

application = webapp2.WSGIApplication([
    ('/', IndexPage),
], debug=True)