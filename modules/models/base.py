from gluon.dal import DAL
from gluon.tools import Auth


class BaseModel(object):

    def __init__(self, db=None, migrate=None, db_format=None):
        """

        :param db:
        :param migrate:
        :param db_format:
        """

        self.db = db
        assert isinstance(self.db, DAL)
        self.config = db.config

        if migrate:
            self.migrate = migrate
        elif not hasattr(self, 'migrate'):
            self.migrate = self.config.db.migrate

        if db_format or not hasattr(self, 'format'):
            self.format = db_format

        self.fields = []
        self.set_properties()
        self.define_table()

    def set_properties(self):
        pass

    def define_table(self):
        if self.table_name in self.db:
            self.entity = self.db[self.table_name]
            return

        self.entity = self.db.define_table(
            self.table_name,
            *self.fields,
            **dict(migrate=self.migrate, format=self.format)
        )


class BaseAuth(BaseModel):

    def __init__(self, auth, migrate=None):
        """


        :param auth:
        :param migrate:
        """
        self.auth = auth
        assert isinstance(self.auth, Auth)
        self.db = auth.db
        self.config = self.db.config
        self.migrate = migrate or self.config.db.migrate
        self.set_properties()
        self.define_extra_fields()
        self.auth.define_tables(migrate=self.migrate)
        self.entity = self.auth.settings.table_user

    def define_extra_fields(self):
        self.auth.settings.extra_fields['auth_user'] = self.fields