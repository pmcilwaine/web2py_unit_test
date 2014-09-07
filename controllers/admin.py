
"""
This file is an attempt to demonstrate how to unit test
with authentication
"""

from app import Application, Account
from gluon import current
from gluon.sqlhtml import SQLFORM
from gluon.dal import Field
from gluon.validators import IS_IMAGE
from gluon.html import URL
from gluon.http import redirect

try:
    application = current.app
except:
    application = Application()

application.db(models=[Account])


@application.auth.requires_membership('admin')
def check_logged():
    return 'I am logged in'


def has_session():
    session = current.session
    if 'my_session' in session:
        return 'The session exists'
    else:
        return 'The session does not exist'


def file_upload():
    form = SQLFORM.factory(
        Field('file', 'upload', uploadfolder=application.config.upload_folder,
              requires=IS_IMAGE(extensions=('jpg', 'jpeg'))),
        _action=URL()
    )

    if form.process().accepted:
        redirect(URL())

    return {'form': form}


def send_email():
    application.mail.send('user1@example.org', 'Example subject', 'My plain text body')
    return {}


def send_email_html():
    application.mail.send('user1@example.org', 'Another subject',
                          (None, '<html><p>My HTML email</p></html>'))
    return {}


def myform():
    form = SQLFORM.factory(
        Field('first_name', 'string'),
        Field('last_name', 'string')
    )

    def onvalidation(form):
        pass

    if form.process(session=application.session, onvaliidation=onvalidation).accepted:
        redirect(URL())

    return dict(form=form)
