from models.base import BaseAuth


class User(BaseAuth):

    def set_properties(self):
        self.fields = []
