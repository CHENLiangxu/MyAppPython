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
    template = setting.JINJA_ENVIRONMENT.get_template('template/test_1.html')
    self.response.write(template.render(template_values))

  def post(self):
    #to do: check the values
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
    template = setting.JINJA_ENVIRONMENT.get_template('template/test_1.html')
    self.response.write(template.render(template_values))

class MembrePage(webapp2.RequestHandler):
  def get(self):
    membres = Membre.query().order(Membre.nom)
    template_values = {
      'membres': membres,
      'result': True,
    }
    template = setting.JINJA_ENVIRONMENT.get_template('template/test_2.html')
    self.response.write(template.render(template_values))

  def post(self):
    membres = Membre.query(Membre.nom == self.request.get('nom')).order(Membre.nom)
    if membres.count() == 0:
      result = False
    else:
      result = True
    template_values = {
      'membres': membres,
      'result': result,
    }
    template = setting.JINJA_ENVIRONMENT.get_template('template/test_2.html')
    self.response.write(template.render(template_values))

application = webapp2.WSGIApplication([
    ('/test_1', PersonPage),
    ('/test_2', MembrePage),
], debug=True)