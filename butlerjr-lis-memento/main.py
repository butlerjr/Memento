#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os

from google.appengine.api import users
from google.appengine.ext import ndb
import jinja2
import webapp2

from models import MementoUser


jinja_env = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
  autoescape=True)

MEMENTO_USER_KEY = ndb.Key("Entity", "movieQuote_root")
class MyHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            q = ndb.gql("SELECT * FROM MementoUser WHERE user_name = :1 AND isVendor = True", user.nickname())
            if (q.count(limit=1000) > 0):
                self.redirect('/VendorHub')
            else:
                qCurrUser = ndb.gql("SELECT * FROM MementoUser WHERE user_name = :1", user.nickname())
                if (qCurrUser.count(limit=1000) > 0):
                    self.redirect('/HRHub')
                else:
                    self.redirect('/SignInOrRegister')
        else:
            greeting = ('<a href="%s">Sign in or register</a>.' %
                        users.create_login_url('/'))

            self.response.out.write("<html><body>%s</body></html>" % greeting)
        
class VendorHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        greeting = ('Welcome to Vendor Page, %s! (<a href="%s">sign out</a>)' %
                    (user.nickname(), users.create_logout_url('/')))
        template = jinja_env.get_template("templates/vendorhub.html")
        self.response.write(template.render({}))
        self.response.out.write(greeting)
        
class HRHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        greeting = ('Welcome to HR Page, %s! (<a href="%s">sign out</a>)' %
                    (user.nickname(), users.create_logout_url('/')))
        template = jinja_env.get_template("templates/hrhub.html")
        self.response.write(template.render({}))
        self.response.out.write(greeting)

class SignInOrRegisterHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        template = jinja_env.get_template("templates/Registration.html")
        self.response.write(template.render({}))
        
class RegisterUserHandler(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        isVendor = False
        
        if self.request.get("entity_key"):
            memento_user_key = ndb.Key(urlsafe=self.request.get("entity_key"))
            memento_user = memento_user_key.get()
            memento_user.user_name = user.nickname()
            isVendor = False
            if 'isVendor' in self.request.POST:
                isVendor = True
            memento_user.isVendor = isVendor
            memento_user.put()
            if memento_user.isVendor:
                self.redirect('/VendorHub')
            else:
                self.redirect('/HRHub')
        else:
            if 'isVendor' in self.request.POST:
                isVendor = True
            new_memento_user = MementoUser(parent = MEMENTO_USER_KEY,
                                        user_name = user.nickname(), 
                                        isVendor = isVendor)
            new_memento_user.put()
            if new_memento_user.isVendor:
                self.redirect('/VendorHub')
            else:
                self.redirect('/HRHub')

app = webapp2.WSGIApplication([
    ('/', MyHandler),
    ('/VendorHub', VendorHandler),
    ('/HRHub', HRHandler),
    ('/SignInOrRegister', SignInOrRegisterHandler),
    ('/RegisterUser', RegisterUserHandler)
], debug=True)
