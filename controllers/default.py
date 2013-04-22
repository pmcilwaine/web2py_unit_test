
from gluon.sqlhtml import SQLFORM
from gluon.dal import Field
from gluon.validators import IS_NOT_EMPTY
from gluon.html import URL
from gluon.http import redirect
from gluon import current
from app import Application

try:
    application = current.app
except:
    application = Application()


def index():
    return 'Hello World'


def edit():
    form = SQLFORM.factory(
        Field('first_name', 'string',
              requires=IS_NOT_EMPTY(error_message='Please enter first name')),
        Field('last_name', 'string',
              requires=IS_NOT_EMPTY(error_message='Please enter last name')),
        _action=URL('experiments', 'default', 'edit')
    )

    if form.process().accepted:
        redirect(URL())

    return {'form': form}


def contact():
    from models.contact import Contact

    db = application.db(models=[Contact])
    form = SQLFORM(db.Contact, _action=URL('experiments', 'default', 'contact'))

    if form.process().accepted:
        redirect(URL())

    return {'form': form}


def different_view():
    response = current.response
    response.view = 'default/myview.html'

    return {'test': 'testing for view'}