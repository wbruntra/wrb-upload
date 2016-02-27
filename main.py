import os
import urllib

import cgi
import re

import jinja2
import webapp2
import json

from google.appengine.ext import ndb
from google.appengine.api import images

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

def render_str(template, **params):
  t = jinja_env.get_template(template)
  return t.render(params)

class Photo(ndb.Model):
    content = ndb.BlobProperty()
    caption = ndb.StringProperty()

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render(self, template, **kw):
        self.response.out.write(render_str(template, **kw))

class MainHandler(Handler):
  def get(self):
    self.render('index.html')

class UploadHandler(Handler):
    def post(self):
        file = self.request.POST['text']
        self.response.headers['Content-Type'] = "text/plain"
        self.response.write(file.value)

class PhotoUploader(Handler):
    def get(self):
        self.render('photos.html')
    def post(self):
        content = self.request.get('img')
        # content = images.resize(content,64,64)
        photo = Photo(content=content)
        photo_key = photo.put()
        url_string = photo_key.urlsafe()
        msg = {'status':'OK',
                    'url':url_string}
        self.response.headers['Content-Type'] = 'application/json'
        self.write(json.dumps(msg))


class ImageHandler(Handler):
    def get(self):
        photo_key = ndb.Key(urlsafe=self.request.get('img_id'))
        photo = photo_key.get()
        if photo:
            self.response.headers['Content-Type'] = 'image/png'
            self.response.out.write(photo.content)
        else:
            self.response.out.write('No image')

class ClearDB(Handler):
    def get(self):
        photos = Photo.query()
        for photo in photos:
            photo.key.delete()
        self.write('Deleted the photos')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/upload',UploadHandler),
    ('/photo',PhotoUploader),
    ('/getphoto',ImageHandler)
], debug=True)
