
from gluon import current
from gluon.dal import DAL
from gluon.storage import Storage
from gluon.tools import Auth, Mail
from models.user import User
import os


class Application(object):

    def __init__(self, config=None):
        """

        :param config:
        """

        self.request = current.request
        self.response = current.response
        self.session = current.session

        # store the application within the thread
        current.app = self

        # TODO we need to setup the configuration better so its flexible
        if not config:
            self.config = Storage(
                db=Storage(
                    uri='sqlite://storage.db',
                    migrate=False,
                    migrate_enabled=False
                ),
                mail=Storage(
                    server='localhost:25',
                    login=None,
                    sender='test@example.org',
                    tls=False
                ),
                upload_folder=os.path.join(self.request.folder, 'static/uploads')
            )
        else:
            self.config = config

    def db(self, models=None):
        """

        :param models:
        """
        if not models:
            models = []

        if not hasattr(self, '_db'):
            self._db = Database(self.config)

        if models:
            self._db.define_models(models)

        return self._db

    @property
    def auth(self):
        if not hasattr(self, '_auth'):
            self._auth = Account(self._db)

        return self._auth

    @property
    def mail(self):
        """


        :return: Mailer
        """
        if not hasattr(self, "_mail"):
            self._mail = Mailer(self.config)

        return self._mail


class Database(DAL):

    def __init__(self, config):
        """

        :param config:
        """

        self._tables = dict()
        self.config = config
        DAL.__init__(self, **config.db)

    def define_models(self, models):
        """

        :param models:
        """

        for model in models:

            # if we have loaded don't load again
            if model.__name__ in self:
                continue

            obj = model(self)
            self.__setattr__(model.__name__, obj.entity)
            if obj.__class__.__name__ == "Account":
                self.__setattr__("auth", obj)


class Account(Auth):

    def __init__(self, db):
        self.db = db
        Auth.__init__(self, self.db)
        user = User(self)
        self.entity = user.entity


class Mailer(Mail):

    def __init__(self, config):
        Mail.__init__(self)
        self.settings.server = config.mail.server
        self.settings.sender = config.mail.sender
        self.settings.login = config.mail.login

if __name__ == '__main__':
    import doctest
    doctest.testmod(extraglobs={'app':App()})