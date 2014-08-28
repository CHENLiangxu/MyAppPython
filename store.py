#-*- coding: utf-8 -*-
import logging
import webapp2
import jinja2
import time
import setting

from google.appengine.ext import ndb
from google.appengine.api import users
from main import Account

class Item(ndb.Model):
  code_id = ndb.StringProperty()
  price = ndb.FloatProperty()
  name = ndb.StringProperty()
  type_item = ndb.StringProperty(choices=setting.TYPE_ITEM)

class ItemPage(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    is_editor = False
    if user:
      account = Account.query(Account.username == user.nickname()).get()
      if account:
        if account.power == 'editor':
          url = users.create_logout_url(self.request.uri)
          url_linktext = 'Logout'
          is_editor = True
          items = Item.query()
          template_values = {
              'items': items,
              'url': url,
              'url_linktext': url_linktext,
          }
          template = setting.JINJA_ENVIRONMENT.get_template('template/item.html')
          self.response.write(template.render(template_values))
    if not is_editor:
      self.redirect(users.create_login_url(self.request.uri))

  def post(self):
    #to do: price reglex
    new_item = Item(
      code_id=self.request.get('code_id'),
      price=float(self.request.get('price')),
      name=self.request.get('name'),
      type_item=self.request.get('type_item'))
    new_item.put()
    #input xml for add many items at one time
    self.redirect('/item')

application = webapp2.WSGIApplication([
    ('/item', ItemPage),
], debug=True)