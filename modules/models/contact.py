from models.base import BaseModel
from gluon.dal import Field
from gluon.validators import IS_NOT_EMPTY, IS_EMAIL


class Contact(BaseModel):
    table_name = 'contact'

    def set_properties(self):
        """
        """

        self.fields = [
            Field('first_name', 'string', requires=IS_NOT_EMPTY('Please enter a first name')),
            Field('last_name', 'string', requires=IS_NOT_EMPTY('Please enter a last name')),
            Field('email', 'string', requires=IS_EMAIL(error_message='Enter a valid email'))
        ]
