from google.appengine.ext import ndb



class Greeting(ndb.Model):
  author = ndb.UserProperty()
  content = ndb.StringProperty(indexed=False)
  date = ndb.DateTimeProperty(auto_now_add=True)