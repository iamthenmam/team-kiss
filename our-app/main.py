import webapp2

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
    ('/', MainHandler)
], debug=True)
