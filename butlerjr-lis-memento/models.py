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
    item_price = ndb.FloatProperty()

class Event(ndb.Model):
    
    event_name = ndb.StringProperty()
    occurrences = ndb.KeyProperty(repeated = True)
    
class Employee(ndb.Model):
    employee_name = ndb.StringProperty()
    employee_birthday = ndb.DateProperty()
    employee_anniversary = ndb.DateProperty()
    employee_maternity_start = ndb.DateProperty()
    
class Vendor(ndb.Model):
    
    company_name = ndb.StringProperty()
    inventory = ndb.KeyProperty(repeated=True)

class HRUser(ndb.Model):
    
    company_name = ndb.StringProperty()
    mementos = ndb.KeyProperty(repeated=True)

class Order(ndb.Model):
    
    item = ndb.KeyProperty(repeated=True)
    to_company = ndb.KeyProperty()
    from_company = ndb.KeyProperty()
    delivery_date = ndb.DateTimeProperty()
    
    
    