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
    occurrences = ndb.DateProperty(repeated = True);
    
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
    
    
    