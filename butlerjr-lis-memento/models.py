from google.appengine.ext import ndb 


class MementoUser(ndb.Model):

    user_name = ndb.StringProperty()
    isVendor = ndb.BooleanProperty()
    user_data = ndb.KeyProperty()
    
    def get_type(self):
        return self.isVendor

class Memento(ndb.Model):
    
    memento_name = ndb.StringProperty()
    event = ndb.KeyProperty()
    vendor = ndb.KeyProperty()
    item = ndb.KeyProperty()
    
class Item(ndb.Model):
    item_name = ndb.StringProperty()
    item_description = ndb.StringProperty()
    item_price = ndb.FloatProperty()

class Event(ndb.Model):
    
    event_name = ndb.StringProperty()
    occurrences = ndb.StringProperty(repeated = True)
    
class Employee(ndb.Model):
    employee_name = ndb.StringProperty()
    employee_id = ndb.IntegerProperty()
    employee_birthday = ndb.DateProperty()
    employee_anniversary = ndb.DateProperty()
    employee_maternity_start = ndb.DateProperty()
    
    def get_meta(self):
        return self._meta.get_all_field_names()
    
class Vendor(ndb.Model):
    
    company_name = ndb.StringProperty()
    inventory = ndb.KeyProperty(repeated=True)

class HRUser(ndb.Model):
    
    company_name = ndb.StringProperty()
    mementos = ndb.KeyProperty(repeated=True)

class Order(ndb.Model):
    
    to_company = ndb.KeyProperty()
    memento = ndb.KeyProperty(repeated=True)
    
    
    