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
import json
import logging
import os


from google.appengine.api import users
from google.appengine.ext import ndb
import jinja2
import webapp2
from collections import Counter

from models import MementoUser, Memento, Vendor, HRUser, Event, Item, Employee, Order
import models



jinja_env = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),extensions=["jinja2.ext.do",],
  autoescape=True)

MEMENTO_USER_KEY = ndb.Key("Entity", "memento_user_root")
MEMENTO_KEY = ndb.Key("Entity", "memento_root")
EVENT_KEY = ndb.Key("Entity", "event_root")
ITEM_KEY = ndb.Key("Entity", "item_root")


class MyHandler(webapp2.RequestHandler):
    def get(self):
        """
        all_employees = ndb.gql("SELECT * FROM Employee")
        for employee in all_employees:
            employee.key.delete()
        
        Sarah = Employee(parent = MEMENTO_USER_KEY,
                   employee_name = "Sarah Keyes",
                   employee_id = 12345679, 
                   employee_birthday = datetime.date(1960, 10, 3), 
                   employee_anniversary = datetime.date(1987, 02, 3), 
                   employee_maternity_start= datetime.date(1987, 1, 3))
        Sarah.put()
        
        Bob = Employee(parent = MEMENTO_USER_KEY,
                   employee_name = "Bob Martin",
                   employee_id = 12345678, 
                   employee_birthday = datetime.date(1957, 10, 5), 
                   employee_anniversary = datetime.date(1980, 02, 2), 
                   employee_maternity_start= datetime.date(1981, 1, 9))
        Bob.put()
        
        Lars = Employee(parent = MEMENTO_USER_KEY,
                   employee_name = "Lars Von Trier",
                   employee_id = 12345672, 
                   employee_birthday = datetime.date(1930, 11, 9), 
                   employee_anniversary = datetime.date(1950, 02, 2), 
                   employee_maternity_start= datetime.date(1981, 1, 9))
        Lars.put()
        """
        
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
        
        curr_vendor_orders = Order.query(ancestor=curr_memento_user_key)
        

        self.response.write(template.render({"user":user, "logout_url": logout_url, "curr_vendor_items": curr_vendor_items}))
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
        all_events = Event.query(ancestor=curr_memento_user_key)
        sample_employee = ndb.gql("SELECT * FROM Employee").get()
        model_fields = sample_employee.to_dict()
        jsonStr = json.dumps({"foo":"bar"})
        print(jsonStr)
        jsonDic = json.loads(jsonStr)
        print(jsonDic["foo"])
        self.response.write(template.render({"user":user, "logout_url": logout_url, "all_mementos": all_mementos, "all_events":all_events, "all_vendors":all_vendors, "model_fields":model_fields}))
        self.response.out.write(greeting)
  

class CreateMementoHandler(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        memento_name = self.request.get("name")
        event_name = self.request.get("event_input")
        item_name = self.request.get("item_input")
        memento_user_query = ndb.gql("SELECT * from MementoUser WHERE user_name = :1", user.nickname())
        
        curr_memento_user = memento_user_query.get()
        curr_memento_user_key = curr_memento_user.key
        
        event = Event.query(ancestor=curr_memento_user_key).filter(ndb.GenericProperty("event_name") == event_name).get()
        item = Item.query(ancestor=MEMENTO_USER_KEY).filter(ndb.GenericProperty("item_name") == item_name).get()
        existing_mementos = Memento.query(ancestor=curr_memento_user_key)
        alreadyExists = existing_mementos.filter(ndb.GenericProperty("memento_name") == memento_name)
        if not self.request.get("entity_key"):
            new_memento = Memento(parent = curr_memento_user_key, memento_name = memento_name, event = event.key, item = item.key)
            new_memento.put()
            
            existing_orders = Order.query(ancestor=MEMENTO_USER_KEY)
            orderAlreadyExists = existing_orders.filter(ndb.GenericProperty("to_company") == curr_memento_user_key)
            hasOrders = False
            existing_order = None
            for order in orderAlreadyExists:
                if (order.key.parent() == item.key.parent()):
                    existing_order = order
                    hasOrders = True
                    break
            if hasOrders:
                existing_order.memento.append(new_memento.key)
                existing_order.put()
                print "Memento Keys:" + str(existing_order.memento)
            else:
                new_order = Order(parent = item.key.parent(), to_company = curr_memento_user_key, memento=[new_memento.key])
                print "SHOULD BE PUTTING NEW ORDER"
                new_order.put()
        else:
            memento_key = ndb.Key(urlsafe=self.request.get("entity_key"))
            memento = memento_key.get()
            memento.memento_name = memento_name
            memento.event = event.key
            memento.item = item.key
            memento.put()
        self.redirect("/HRHub")
        
        
        

class DeleteMementoHandler(webapp2.RequestHandler):
    def post(self):
        memento_key = ndb.Key(urlsafe=self.request.get("entity_key"))
        memento_key.delete()
#       memento_name = self.request.get("memento_to_delete_name")
#       memento_to_delete = ndb.gql("SELECT * FROM Memento WHERE memento_name = :1", memento_name)
#       for m in memento_to_delete:
#            m.key.delete()
        self.redirect("/HRHub")

class DeleteItemHandler(webapp2.RequestHandler):
    def post(self):
        item_key = ndb.Key(urlsafe=self.request.get("entity_key"))
        item_key.delete()
        self.redirect("/VendorHub")

class AddItemHandler(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        item_name = self.request.get("item_name")
        item_description = self.request.get("item_description")
        item_price = float(self.request.get("item_price"))
        memento_user_query = ndb.gql("SELECT * from MementoUser WHERE user_name = :1", user.nickname())
        curr_memento_user = memento_user_query.get()
        curr_memento_user_key = curr_memento_user.key
        existing_items = Item.query(ancestor=curr_memento_user_key)
        alreadyExists = existing_items.filter(ndb.GenericProperty("item_name") == item_name)
        if (alreadyExists.count(limit=1000) == 0):
            new_item = Item(parent = curr_memento_user_key, item_name = item_name, item_price = item_price, item_description = item_description)
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
                new_HR = HRUser(parent = new_memento_user.key, company_name=self.request.get("company"), mementos=[])
                new_HR.put()
                new_memento_user.user_data = new_HR.key
                new_memento_user.put()
                self.redirect('/HRHub')

class DefineEventHandler(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        memento_user_query = ndb.gql("SELECT * from MementoUser WHERE user_name = :1", user.nickname())
        curr_memento_user = memento_user_query.get()
        curr_memento_user_key = curr_memento_user.key
        
        selected_field = self.request.get("event_source")
        
        occurrences = ndb.gql("SELECT * FROM Employee")
        name_and_date = []
        
        
        for occurrence in occurrences:
            employee_dict = {"employee_name" : occurrence.employee_name, "employee_maternity_start": occurrence.employee_maternity_start, "employee_birthday": occurrence.employee_birthday, "employee_anniversary":occurrence.employee_anniversary, "employee_id":occurrence.employee_id}
            str_to_add = "For " + str(employee_dict["employee_name"]) + " on " + str(employee_dict[selected_field])
            name_and_date.append(str_to_add)
            
        
        new_event = Event(parent=curr_memento_user_key, event_name=self.request.get("event_name"), occurrences=name_and_date)
        new_event.put()
        self.redirect('HRHub')

class ViewOrderHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        logout_url = users.create_logout_url('/')
        template = jinja_env.get_template("templates/order.html")
        
        memento_user_query = ndb.gql("SELECT * from MementoUser WHERE user_name = :1", user.nickname())
        curr_memento_user = memento_user_query.get()
        curr_memento_user_key = curr_memento_user.key
        curr_vendor_orders = Order.query(ancestor=curr_memento_user_key)
        all_companies = []
        all_special_order_dict = []
        for order in curr_vendor_orders:
            print "Order" + str(order)
            all_items_in_order = []
            all_special_order_dict = []
            for memento_key in order.memento:
                item_name = memento_key.get().item.get().item_name
                all_items_in_order.append(item_name)
            
            for memento_key in order.memento:
                item_company = order.to_company.get().user_data.get().company_name
                if item_company not in all_companies:
                    all_companies.append(item_company)
                item_name = memento_key.get().item.get().item_name
                item_price = memento_key.get().item.get().item_price
                item_frequency = all_items_in_order.count(item_name)
                special_order_dict = {"company_name": item_company, "item_name":item_name, "item_price":item_price, "item_frequency":item_frequency, "all_companies":all_companies}
                print special_order_dict
                if special_order_dict not in all_special_order_dict:
                    all_special_order_dict.append(special_order_dict)
        print all_special_order_dict
        self.response.write(template.render({"user":user, "logout_url": logout_url, "orders": all_special_order_dict, "all_companies":all_companies}))


app = webapp2.WSGIApplication([
    ('/', MyHandler),
    ('/VendorHub', VendorHandler),
    ('/HRHub', HRHandler),
    ('/SignInOrRegister', SignInOrRegisterHandler),
    ('/RegisterUser', RegisterUserHandler),
    ('/addmemento', CreateMementoHandler),
    ('/DeleteMemento', DeleteMementoHandler),
    ('/DeleteItem', DeleteItemHandler),
    ('/AddItem', AddItemHandler),
    ('/DefineEvent', DefineEventHandler),
    ('/vieworder', ViewOrderHandler)
], debug=True)
