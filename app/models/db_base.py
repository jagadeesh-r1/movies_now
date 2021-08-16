from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_mixins import ActiveRecordMixin, SerializeMixin, SmartQueryMixin

Base = declarative_base()


class MySqlBase(Base, SerializeMixin):
    __abstract__ = True
    
    def __repr__(self):
        name = self.name if hasattr(self, "name") else self.id
        return "{}('{}')".format(self.__class__.__name__, name)


# MySqlBase.set_session()