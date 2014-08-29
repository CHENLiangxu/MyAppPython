#-*- coding: utf-8 -*-
import logging
import webapp2
import jinja2
import time
import setting
import urllib

from google.appengine.ext import ndb
from google.appengine.api import users
from main import Account

def isEditor(user):
  if user:
    account = Account.query(Account.username == user.nickname()).get()
    if account:
      if account.power == 'editor':
        return True
  return False

def buildContent(bill_id, del_item_id, del_item_number):
  bill_tables = BillTable.query().order(-BillTable.date)
  if del_item_id:
    del_item = Bill.query(
      (Bill.bill_id==bill_id)and
      (Bill.item_id==del_item_id)and
      (Bill.number==del_item_number))
    del_item.get().put().delete()
  bill_items = Bill.query(Bill.bill_id==bill_id)
  total_price = 0
  i = 0
  content = {}
  for bill_item in bill_items:
    item = Item.query(Item.code_id==bill_item.item_id).get()
    content[i]={
      'id': bill_item.item_id,
      'name': item.name,
      'price': item.price,
      'number': bill_item.number,
      'total': item.price*bill_item.number,
    }
    total_price += content[i]['total']
    i = i + 1
  content['total_price'] = total_price
  logging.info(content)
  return content

class Item(ndb.Model):
  code_id = ndb.StringProperty()
  price = ndb.FloatProperty()
  name = ndb.StringProperty()
  type_item = ndb.StringProperty(choices=setting.TYPE_ITEM)

class Bill(ndb.Model):
  bill_id = ndb.StringProperty()
  item_id = ndb.StringProperty()
  number = ndb.IntegerProperty()

class BillTable(ndb.Model):
  bill_id = ndb.StringProperty()
  date = ndb.DateTimeProperty(auto_now_add=True)
  total_price = ndb.FloatProperty()

class ItemPage(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if isEditor(user):
      items = Item.query().order(Item.code_id)
      template_values = {
          'items': items,
      }
      template = setting.JINJA_ENVIRONMENT.get_template('template/store_item.html')
      self.response.write(template.render(template_values))
    else:
      self.redirect(users.create_login_url(self.request.uri))

  def post(self):
    #to do: price reglex
    #to do: check code_id unique
    new_item = Item(
      code_id=self.request.get('code_id'),
      price=float(self.request.get('price')),
      name=self.request.get('name'),
      type_item=self.request.get('type_item'))
    new_item.put()
    #input xml for add many items at one time
    self.redirect('/store_item')

class BillPage(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if isEditor(user):
      template_values = {
          'bill_tables': BillTable.query(),
      }
      template = setting.JINJA_ENVIRONMENT.get_template('template/store_bill_table.html')
      self.response.write(template.render(template_values))
    else:
      self.redirect(users.create_login_url(self.request.uri))

  def post(self):
    timetamp = str(int(time.time()))
    new_bill_table = BillTable(
      bill_id='B'+ timetamp,
      total_price=0, 
    )
    new_bill_table.put()
    self.redirect("/store_bill_table")

class EditeBill(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if isEditor(user):
      bill_id = self.request.get('bill_id')
      del_item_id = self.request.get('item_id')
      if del_item_id:
        del_item_number = int(self.request.get('number'))
      else:
        del_item_number = None
      content = buildContent(bill_id, del_item_id, del_item_number)
      bill_table = BillTable.query(BillTable.bill_id==bill_id).get()
      bill_table.total_price = content['total_price']
      bill_table.put()
      del content['total_price']
      items = Item.query()
      template_values = {
          'content': content,
          'bill_id': bill_id,
          'total_price': bill_table.total_price,
          'items': items,
      }
      template = setting.JINJA_ENVIRONMENT.get_template(
        'template/store_bill.html' )
      self.response.write(template.render(template_values))
    else:
      self.redirect(users.create_login_url(self.request.uri))

  def post(self):
    #to do item_id is unique
    operation = self.request.get('Operation')
    bill_id = self.request.get('bill_id')
    if operation == 'add':
      new_item_bill = Bill(
        bill_id=bill_id,
        number=int(self.request.get('number')),
        item_id=self.request.get('item_id'),
      )
    new_item_bill.put()
    query_params = {'bill_id': bill_id}
    self.redirect('/store_bill?' + urllib.urlencode(query_params))

application = webapp2.WSGIApplication([
    ('/store_item', ItemPage),
    ('/store_bill_table', BillPage),
    ('/store_bill?.*', EditeBill),
], debug=True)