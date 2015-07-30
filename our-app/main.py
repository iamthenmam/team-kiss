import webapp2
import jinja2
from google.appengine.ext import ndb
from google.appengine.api import urlfetch
import datetime
import json
import logging

env = jinja2.Environment(loader=jinja2.FileSystemLoader("templates"))

class Word(ndb.Model):
    latitude = ndb.FloatProperty(required=True)
    longitude = ndb.FloatProperty(required=True)
    word = ndb.StringProperty(required=True)
    definition = ndb.TextProperty(required=True)
    timestamp = ndb.DateTimeProperty(required=True)

class Marker(ndb.Model):
    latitude = ndb.FloatProperty(required=True)
    longitude = ndb.FloatProperty(required=True)
    word = ndb.StringProperty(required=True)
    definition = ndb.StringProperty(required=True)
    timestamp = ndb.DateTimeProperty(required=True)

class Searched_Word(ndb.Model):
    word = ndb.StringProperty(required=True)
    count = ndb.IntegerProperty(required=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template("home.html")

        location_searched = self.request.get('location')

        safe_location = location_searched.replace(" ", "+")
        json_url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + safe_location + "&key=AIzaSyAQeIATzPIzimJIYBgyN-b2rDX79rylZwc"
        json_code = urlfetch.fetch(json_url)
        json_content = json_code.content
        result = json.loads(json_content)["results"]
        if location_searched is "" or len(result) is 0:
            loc_lat = 39.8282
            loc_lng = -98.5795
            loc_zoom = 5
        else:
            loc_lat = result[0]["geometry"]["location"]["lat"]
            loc_lng = result[0]["geometry"]["location"]["lng"]
            loc_zoom = 11

        word_searched = self.request.get('searched_word')

        todays_word_source = urlfetch.fetch("http://urban-word-of-the-day.herokuapp.com/")
        todays_word_content = todays_word_source.content
        todays_word_dictionary = json.loads(todays_word_content)
        todays_word = todays_word_dictionary['word']
        todays_def = todays_word_dictionary['meaning']

        urban_url = ""

        if len(word_searched) > 0: #checks if actual word is searched
            #first count searched word
            list_of_sw = Searched_Word.query(Searched_Word.word == word_searched).fetch()
            if len(list_of_sw) > 0:
                list_of_sw[0].count += 1
                list_of_sw[0].put()
            else:
                Searched_Word(word=word_searched, count=1).put()

            if " " in word_searched:
                word_searched = word_searched.replace(" ", "%20") #replaces spaces in word searched
            urban_data_source = urlfetch.fetch("http://api.urbandictionary.com/v0/define?term=%s" % word_searched)
            urban_json_content = urban_data_source.content
            urban_definition = json.loads(urban_json_content)
            if len(urban_definition['list']) > 0: #checks if word actually has definitions
                urban_url = urban_definition['list'][0]['definition'] #gets definition
                #logging.info('!!!!!!' + urban_url)

        trending_results = Searched_Word.query().fetch()
        #posts.sort(key=lambda x: x.timestamp, reverse=True)
        trending_results.sort(key=lambda x: x.count, reverse=True)
        trending = trending_results[:3]

        word_searched = word_searched.replace("%20", " ") #puts spaces back into word to print
        defs = Word.query(Word.word == word_searched).fetch() #gets list of definitions for the word searched from database

        markers = Marker.query().fetch()

        variables = {'word_searched': word_searched, 'defs': defs, 'search_def': urban_url,
                     'todays_word': todays_word, 'todays_def': todays_def, 'trending': trending, "markers": markers,
                     'loc_lat': loc_lat, 'loc_lng': loc_lng, 'location_searched': location_searched, "loc_zoom": loc_zoom}

        self.response.write(template.render(variables))

# class placeMarkerHandler(webapp2.RequestHandler):
#     def get(self):
#         template = env.get_template("home.html")
#         markers = Marker.query().fetch()
#         variables = {"markers": markers}
#         self.response.write(template.render(variables))

class AddWordHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template("submit.html")
        self.response.write(template.render())
    def post(self):
        location = self.request.get("location_box")
        safe_location = location.replace(" ", "+")
        json_url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + safe_location + "&key=AIzaSyAQeIATzPIzimJIYBgyN-b2rDX79rylZwc"
        json_code = urlfetch.fetch(json_url)
        json_content = json_code.content
        result = json.loads(json_content)["results"]
        lat = result[0]["geometry"]["location"]["lat"]
        lng = result[0]["geometry"]["location"]["lng"]
        word = self.request.get("word_box").lower()
        definition = self.request.get("definition_box")
        added_word = Word(latitude= lat,
                          longitude= lng,
                          word=word,
                          definition=definition,
                          timestamp=datetime.datetime.now())
        added_word.put()
    # Saving markers to the database
        added_marker = Marker(latitude= lat,
                              longitude= lng,
                              word=word,
                              definition=definition,
                              timestamp=datetime.datetime.now())
        added_marker.put()
        self.redirect("/")

class AboutHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template("about.html")
        self.response.write(template.render())

app = webapp2.WSGIApplication([
    ("/", MainHandler),
    # ("/", placeMarkerHandler),
    ("/add", AddWordHandler),
    ("/about", AboutHandler)
], debug=True)
