from google.appengine.ext import ndb 

class MementoUser(ndb.Model):

    user_name = ndb.StringProperty()
    isVendor = ndb.BooleanProperty()
    
    def get_type(self):
        return self.isVendor
