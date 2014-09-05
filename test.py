#-*- coding: utf-8 -*-
import webapp2
import jinja2
import setting
import urllib
import logging

from google.appengine.ext import ndb

class Person(ndb.Model):
  nom = ndb.StringProperty()
  telephone = ndb.StringProperty()

  def set(self, nom, telephone):
    try:
      self.nom = nom
      self.telephone = telephone
      self.put()
      return True
    except:
      return False

class Membre(ndb.Model):
  nom = ndb.StringProperty()
  pernom = ndb.StringProperty()
  post = ndb.StringProperty()

  def set(self, nom, pernom, post):
    try:
      self.nom = nom
      self.pernom = pernom
      self.post = post
      self.put()
      return True
    except:
      return False

class PersonPage(webapp2.RequestHandler):
  def get(self):
    persons = Person.query().order(Person.nom)
    template_values = {
      'persons': persons,
    }
    template = setting.JINJA_ENVIRONMENT.get_template('template/test.html')
    self.response.write(template.render(template_values))

  def post(self):
    #to do: check the values
    if self.request.get('type') == "Add":
      new_person = Person()
      res = new_person.set(
        nom=self.request.get('nom'),
        telephone=self.request.get('telephone'),
      )
    persons = Person.query().order(Person.nom)
    template_values = {
          'persons': persons,
          'result': res,
      }
    template = setting.JINJA_ENVIRONMENT.get_template('template/test.html')
    self.response.write(template.render(template_values))

application = webapp2.WSGIApplication([
    ('/test', PersonPage),
], debug=True)