
import webapp2
import jinja2
from google.appengine.ext import ndb
import datetime

env = jinja2.Environment(loader=jinja2.FileSystemLoader("templates"))

class Word(ndb.Model):
    location = ndb.StringProperty(required=True)
    word = ndb.StringProperty(required=True)
    definition = ndb.TextProperty(required=True)
    timestamp = ndb.DateTimeProperty(required=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template("home.html")
        self.response.write(template.render())

class AddWordHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template("submit.html")
        self.response.write(template.render())
    def post(self):
        location = self.request.get("location_box")
        word = self.request.get("word_box")
        definition = self.request.get("definition_box")
        added_word = Word(location=location,
                          word=word,
                          definition=definition,
                          timestamp=datetime.datetime.now())
        added_word.put()
        self.redirect("/")


app = webapp2.WSGIApplication([
    ("/", MainHandler),
    ("/add", AddWordHandler)
], debug=True)
