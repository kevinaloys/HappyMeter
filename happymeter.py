__author__ = 'jasonchilders'

from google.appengine.api import users
import webapp2
from happy_meter.model.test import Person

class MainPage(webapp2.RequestHandler):

  def get(self):
    user = users.get_current_user()

    self.response.headers['Content-Type'] = 'text/plain'
    if user:
      self.response.write('Hello, ' + user.nickname() + '!\n')
      self.response.write('We measure happiness! :-)')
    else:
      self.redirect(users.create_login_url(self.request.uri))

class PersonPage(webapp2.RequestHandler):

  def get(self):
    person_key = Person.Create('Kevin', 372, 1)
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.write('person_key: %s' % person_key + '\n')

application = webapp2.WSGIApplication([
  ('/', MainPage), ('/person', PersonPage)
], debug=True)



