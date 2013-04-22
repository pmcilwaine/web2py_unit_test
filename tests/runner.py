
import unittest
import sys
import os

import logging
import logging.config

# setup the application path
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))

# setup the application modules path
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..', 'modules')))

# web2py path, its assumed you are setup correctly that is web2py/applications/<application>/tests
web2py_path = os.path.abspath(os.path.join(os.getcwd(), '..', '..', '..'))
sys.path.append(web2py_path)

# setup a very basic environment
from gluon import current
from gluon.globals import Request, Session, Response
from gluon.storage import Storage

current.T = lambda t: t
current.request = Request()
current.session = Session()
current.response = Response()

# you will need to update this with your application name
current.request.application = 'web2py_unit_test'

# create our test database
from app import Application
application = Application(config=Storage(
    db=Storage(
        uri='sqlite://test_storage.db', migrate=True,  migrate_enabled=True, folder='databases'
    ),
    mail=Storage(
        server='logging',
        sender='test@example.org'
    ),
    upload_folder=os.path.join(os.getcwd(), 'uploads')
))

from controllers import default_test, admin_test

logging.config.fileConfig('logging.conf')

suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(default_test.DefaultTest))
suite.addTest(unittest.makeSuite(admin_test.AdminTest))
unittest.TextTestRunner(verbosity=1).run(suite)


# clean up
db = application.db()
for table in db.tables:
    db[table].drop()

for db_file in os.listdir('databases'):
    os.remove(os.path.abspath(os.path.join('databases', db_file)))

for test_file in os.listdir('uploads'):
    os.remove(os.path.abspath(os.path.join('uploads', test_file)))

os.remove(os.path.join('logs', 'web2py.log'))
