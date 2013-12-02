__author__ = 'jasonchilders'


import os

import jinja2
import logging as logger
import webapp2

from google.appengine.api import users
from happy_meter.model.test import Person
import happy_meter.model.user as user_model


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class MainPage(webapp2.RequestHandler):

  def get(self):
    user = users.get_current_user()

    #self.response.headers['Content-Type'] = 'text/plain'
    if user:
      #self.response.write('Hello, ' + user.nickname() + '!\n')
      #self.response.write('We measure happiness! :-)')
      #template_values = {}
      #template = JINJA_ENVIRONMENT.get_template('static/index.html')
      #self.response.write(template.render(template_values))
      self.redirect('/login')
    else:
      #self.redirect(users.create_login_url(self.request.uri))
      template_values = {}
      template = JINJA_ENVIRONMENT.get_template('static/index.html')
      self.response.write(template.render(template_values))



class PersonPage(webapp2.RequestHandler):

  def get(self):
    person_key = Person.Create('Kevin', 372, 1)
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.write('person_key: %s' % person_key + '\n')

class LoginPage(webapp2.RequestHandler):

  def get(self):
    user = users.get_current_user()
    if user:
      template_values = {
        'user_email': user.email(),
        'group_name': LoginPage.GetFirstGroupName(user.email())
      }
      template = JINJA_ENVIRONMENT.get_template('static/dashboard.html')
      self.response.write(template.render(template_values))
    else:
      self.redirect(users.create_login_url(self.request.uri))

  @staticmethod
  def GetFirstGroupName(user_name):
    """This is really a simplified method to get the user's first group_name.  Modify this to be in line with the
        future needs of the login page.
    """
    user_do = user_model.User.GetUser(user_name)
    group_names = user_do.GroupNames()
    logger.info('group_names: %s' % group_names)

    return group_names[0]

application = webapp2.WSGIApplication([
  ('/', MainPage), ('/person', PersonPage), ('/login', LoginPage)
], debug=True)



