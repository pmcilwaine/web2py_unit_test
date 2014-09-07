import unittest
from gluon import current
from gluon.storage import Storage
from gluon.sqlhtml import SQLFORM
from gluon.http import HTTP
from controllers import default


class DefaultTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.application = current.app

    def setUp(self):
        """
        """

        self.request = current.request
        self.request.controller = 'default'
        self.request.application = 'web2py_unit_test'
        self.request.post_vars = Storage()
        self.request.get_vars = Storage()
        self.application.session.clear()

    def test_index(self):
        """
        """

        self.assertEqual(default.index(), 'Hello World')

    def test_edit_get(self):
        """
        """
        get_response = default.edit()
        self.assertIsInstance(get_response['form'], SQLFORM)

    def test_edit_empty_form(self):
        """
        """

        get_response = default.edit()

        self.request._post_vars = Storage({
            '_formkey': get_response['form'].formkey,
            '_formname': get_response['form'].formname
        })

        post_response = default.edit()
        errors = post_response['form'].errors
        self.assertEqual(errors.first_name, 'Please enter first name')
        self.assertEqual(errors.last_name, 'Please enter last name')

    def test_edit_valid_form(self):
        """
        """

        get_response = default.edit()

        self.request.function = 'edit'
        self.request._post_vars = Storage({
            'first_name': 'Test',
            'last_name': 'User',
            '_formkey': get_response['form'].formkey,
            '_formname': get_response['form'].formname
        })

        try:
            default.edit()
        except HTTP:
            pass
        except Exception:
            self.fail('Unexpected exception thrown')
        else:
            self.fail('No exception thrown')

    def test_contact_empty_form(self):
        get_response = default.contact()

        self.request._post_vars = Storage({
            '_formkey': get_response['form'].formkey,
            '_formname': get_response['form'].formname
        })

        post_response = default.contact()
        errors = post_response['form'].errors
        self.assertEqual(errors.first_name, 'Please enter a first name')
        self.assertEqual(errors.last_name, 'Please enter a last name')
        self.assertEqual(errors.email, 'Enter a valid email')

    def test_contact_valid_form(self):
        db = self.application.db()
        get_response = default.contact()

        self.request.function = 'edit'
        self.request._post_vars = Storage({
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@test.com',
            '_formkey': get_response['form'].formkey,
            '_formname': get_response['form'].formname
        })

        try:
            default.contact()
            db.commit()
        except HTTP:
            pass
        except Exception:
            self.fail('Unexpected exception thrown')
        else:
            self.fail('No exception thrown')

        # check to see if we have a single record
        self.assertEqual(db(db.Contact.id != 0).count(), 1)

    def test_different_view(self):
        try:
            default.different_view()
        except:
            self.fail('An exception was thrown')
