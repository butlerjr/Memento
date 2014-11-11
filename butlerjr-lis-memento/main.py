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
import datetime
import logging
import os

from google.appengine.api import users
from google.appengine.ext import ndb
import jinja2
import webapp2

from models import MementoUser, Memento, Vendor, HRUser, Event, Item


jinja_env = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
  autoescape=True)

MEMENTO_USER_KEY = ndb.Key("Entity", "memento_user_root")
MEMENTO_KEY = ndb.Key("Entity", "memento_root")
EVENT_KEY = ndb.Key("Entity", "event_root")
ITEM_KEY = ndb.Key("Entity", "item_root")

FAKE_ITEM_PRICE = 3.00

item_cupcake = Item(parent=ITEM_KEY, item_name="Flying Cupcake", item_price=3.40);
item_cupcake.put()
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
        
        memento_user_query = ndb.gql("SELECT * from MementoUser WHERE user_name = :1", user.nickname())
        curr_memento_user = memento_user_query.get()
        curr_memento_user_key = curr_memento_user.key
        
        curr_vendor_items = Item.query(ancestor=curr_memento_user_key)
        greeting = ('Welcome to Vendor Page, %s! (<a href="%s">sign out</a>)' %
                    (user.nickname(), users.create_logout_url('/')))
        logout_url = users.create_logout_url('/')
        template = jinja_env.get_template("templates/vendorhub.html")
        
        
        self.response.write(template.render({"logout_url": logout_url, "curr_vendor_items": curr_vendor_items}))
        self.response.out.write(greeting)
        
class HRHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        
        memento_user_query = ndb.gql("SELECT * from MementoUser WHERE user_name = :1", user.nickname())
        curr_memento_user = memento_user_query.get()
        curr_memento_user_key = curr_memento_user.key
        
        greeting = ('Welcome to HR Page, %s! (<a href="%s">sign out</a>)' %
                    (user.nickname(), users.create_logout_url('/')))
        logout_url = users.create_logout_url('/')
        template = jinja_env.get_template("templates/hrhub.html")
        all_mementos = Memento.query(ancestor=curr_memento_user_key)
        all_vendors = Vendor.query(ancestor=MEMENTO_USER_KEY)
        self.response.write(template.render({"logout_url": logout_url, "all_mementos": all_mementos, "all_vendors":all_vendors}))
        self.response.out.write(greeting)

class CreateMementoHandler(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        memento_name = self.request.get("name")
        memento_user_query = ndb.gql("SELECT * from MementoUser WHERE user_name = :1", user.nickname())
        curr_memento_user = memento_user_query.get()
        curr_memento_user_key = curr_memento_user.key
        existing_mementos = Memento.query(ancestor=curr_memento_user_key)
        alreadyExists = existing_mementos.filter(ndb.GenericProperty("memento_name") == memento_name)
        if (alreadyExists.count(limit=1000) == 0):
            new_memento = Memento(parent = curr_memento_user_key, memento_name = memento_name, event = event_birthday.key, item = item_cupcake.key)
            new_memento.put()
        self.redirect("/HRHub")

class CreateEventHandler(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        

class DeleteMementoHandler(webapp2.RequestHandler):
    def post(self):
        memento_key = ndb.Key(urlsafe=self.request.get("entity_key"))
        memento_key.delete()
#       memento_name = self.request.get("memento_to_delete_name")
#       memento_to_delete = ndb.gql("SELECT * FROM Memento WHERE memento_name = :1", memento_name)
#       for m in memento_to_delete:
#            m.key.delete()
        self.redirect("/HRHub")

class AddItemHandler(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        item_name = self.request.get("item_name")
        item_price = float(self.request.get("item_price"))
        memento_user_query = ndb.gql("SELECT * from MementoUser WHERE user_name = :1", user.nickname())
        curr_memento_user = memento_user_query.get()
        curr_memento_user_key = curr_memento_user.key
        existing_items = Item.query(ancestor=curr_memento_user_key)
        alreadyExists = existing_items.filter(ndb.GenericProperty("item_name") == item_name)
        if (alreadyExists.count(limit=1000) == 0):
            new_item = Item(parent = curr_memento_user_key, item_name = item_name, item_price = item_price)
            new_item.put()
            curr_memento_user.user_data.get().inventory.append(new_item.key)
            curr_memento_user.user_data.get().put()
        self.redirect("/VendorHub")


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
                                        isVendor = isVendor,
                                        user_data = None)
            new_memento_user.put()
            if new_memento_user.isVendor:
                new_Vendor = Vendor(parent = new_memento_user.key, company_name=self.request.get("company"), inventory=[])
                new_Vendor.put()
                new_memento_user.user_data = new_Vendor.key
                new_memento_user.put()
                self.redirect('/VendorHub')
            else:
                new_HR = HRUser(parent = new_memento_user.key, company_name="test_company", mementos=[])
                new_HR.put()
                new_memento_user.user_data = new_HR.key
                new_memento_user.put()
                self.redirect('/HRHub')

app = webapp2.WSGIApplication([
    ('/', MyHandler),
    ('/VendorHub', VendorHandler),
    ('/HRHub', HRHandler),
    ('/SignInOrRegister', SignInOrRegisterHandler),
    ('/RegisterUser', RegisterUserHandler),
    ('/addmemento', CreateMementoHandler),
    ('/DeleteMemento', DeleteMementoHandler),
    ('/AddItem', AddItemHandler)
], debug=True)
