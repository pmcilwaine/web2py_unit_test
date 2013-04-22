import unittest
from gluon import current
from gluon.http import HTTP
from gluon.storage import Storage
from app import Account
from helpers.tools import upload
from applications.experiments.controllers import admin
import os
import logging


class AdminTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.application = current.app

    def setUp(self):
        """
        """

        self.request = current.request
        self.session = current.session

        self.request.controller = 'admin'
        self.request.application = 'web2py_unit_test'
        self.request.post_vars = Storage()
        self.request.get_vars = Storage()
        self.application.auth.user = None
        self.session.clear()

        # remove the handler, delete the log file then reattach
        logger = logging.getLogger('web2py')
        logger.removeHandler(logger.handlers[0])
        os.remove('logs/web2py.log')
        logger.addHandler(logging.FileHandler("logs/web2py.log", "w"))

    def test_check_logged_not_logged(self):
        try:
            admin.check_logged()
        except HTTP:
            pass
        except Exception:
            self.fail('Unexpected exception thrown')
        else:
            self.fail('No exception thrown')

    def test_check_logged_in_wrong_group(self):
        db = self.application.db(models=[Account])
        auth = self.application.auth

        # create group
        group_id = db.auth_group.insert(**{
            'role': 'wrong role'
        })

        # create user
        user = auth.get_or_create_user({
            'email': 'test@example.org',
            'password': '12345678'
        })

        auth.add_membership(group_id=group_id, user_id=user.id)

        try:
            admin.check_logged()
        except HTTP:
            pass
        except Exception:
            self.fail('Unexpected exception thrown')
        else:
            self.fail('No exception thrown')

    def test_check_logged_in(self):
        db = self.application.db(models=[Account])
        auth = self.application.auth

        # create group
        group_id = db.auth_group.insert(**{
            'role': 'admin'
        })

        # create user
        user = auth.get_or_create_user({
            'email': 'test@example.org',
            'password': '12345678'
        })

        auth.add_membership(group_id=group_id, user_id=user.id)

        try:
            self.assertEqual('I am logged in', admin.check_logged())
        except:
            self.fail('An exception has been thrown')

    def test_has_session_empty(self):
        self.assertEqual('The session does not exist', admin.has_session())

    def test_has_session_exists(self):
        self.session.my_session = 'exists'
        self.assertEqual('The session exists', admin.has_session())

    def test_file_upload_invalid(self):
        get_response = admin.file_upload()

        self.request.function = 'edit'
        self.request.post_vars = Storage({
            'file': None,
            '_formkey': get_response['form'].formkey,
            '_formname': get_response['form'].formname
        })

        try:
            errors = admin.file_upload()['form'].errors
            self.assertEqual(errors.file, 'invalid image')
        except Exception as e:
            self.fail(('Unexpected exception thrown', e))

    def test_file_upload(self):
        get_response = admin.file_upload()

        self.request.function = 'edit'
        self.request.post_vars = Storage({
            'file': upload('file', 'icon_world.jpg'),
            '_formkey': get_response['form'].formkey,
            '_formname': get_response['form'].formname
        })

        try:
            admin.file_upload()
        except HTTP:
            pass
        except Exception:
            self.fail('Unexpected exception thrown')
        else:
            self.fail('No exception thrown')

    def test_send_email(self):
        admin.send_email()

        with open('logs/web2py.log', 'r') as f:
            contents = f.read()

        self.assertEqual('''email not sent
----------------------------------------
From: test@example.org
To: user1@example.org
Subject: Example subject

My plain text body
----------------------------------------

''', contents)

    def test_send_email_html(self):
        admin.send_email_html()

        with open('logs/web2py.log', 'r') as f:
            contents = f.read()

        self.assertEqual('''email not sent
----------------------------------------
From: test@example.org
To: user1@example.org
Subject: Another subject

<html><p>My HTML email</p></html>
----------------------------------------

''', contents)

    def test_myform(self):
        """
        This test is to demonstrate how you can test a form without
        doing a simulated get request to start off with.
        """

        self.session['_formkey[no_table/create]'] = 'abc'
        self.request.function = 'edit'
        self.request.post_vars = Storage({
            'first_name': 'Test',
            'last_name': 'User',
            '_formkey': 'abc',
            '_formname': 'no_table/create'
        })

        try:
            admin.myform()
        except HTTP:
            pass
        except Exception:
            self.fail('Unexpected exception thrown')
        else:
            self.fail('No exception thrown')

