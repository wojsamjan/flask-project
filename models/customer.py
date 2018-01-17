from passlib.apps import custom_app_context as pwd_context
# from sqlalchemy.sql.expression import func
# import itertools
from db import db


class CustomerModel(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.String(40), primary_key=True)
    username = db.Column(db.String(40))
    password_hash = db.Column(db.String(128))

    first_name = db.Column(db.String(40))
    last_name = db.Column(db.String(40))
    email = db.Column(db.String(320))
    phone = db.Column(db.String(40))

    def __init__(self, username, password, first_name, last_name, email, phone):
        self.id = username
        self.username = username
        self.password_hash = self.hash_password(password)

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone

    def hash_password(self, password):
        return pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    # def fake_json(self):
    #     return {'username': self.username, 'password_hash': self.password_hash}

    # def json(self):
    #     return {'id': self.id, 'username': self.username}

    # def short_json(self):
    #     return {'username': self.username}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
