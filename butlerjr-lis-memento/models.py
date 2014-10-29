from google.appengine.ext import ndb 

class MementoUser(ndb.Model):

    user_name = ndb.StringProperty()
    isVendor = ndb.BooleanProperty()
    
    def get_type(self):
        return self.isVendor

class Memento(ndb.Model):
    
    memento_name = ndb.StringProperty()
    event = ndb.StringProperty()
    item = ndb.StringProperty()