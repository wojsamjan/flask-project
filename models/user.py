from passlib.apps import custom_app_context as pwd_context
from db import db


class UserModel(db.Model):  # db.Model -> tells SQLAlchemy about relation
    __tablename__ = 'users'  # where to save our UserModel in database using SQLAlchemy

    id = db.Column(db.Integer, primary_key=True)  # specifies columns in database for our UserModel
    username = db.Column(db.String(40))
    password_hash = db.Column(db.String(128))

    first_name = db.Column(db.String(40))
    last_name = db.Column(db.String(40))

    country = db.Column(db.String(40))
    city = db.Column(db.String(40))
    postal_code = db.Column(db.String(16))
    street = db.Column(db.String(40))
    email = db.Column(db.String(320))
    phone = db.Column(db.String(40))

    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'))
    branch = db.relationship('BranchModel')

    position_id = db.Column(db.Integer, db.ForeignKey('positions.id'))
    position = db.relationship('PositionModel')

    salary = db.Column(db.Integer)

    def __init__(self, username, password, first_name, last_name,
                 country, city, postal_code, street, email, phone, branch_id, position_id, salary):
        self.id

        self.username = username
        self.password_hash = self.hash_password(password)

        self.first_name = first_name
        self.last_name = last_name

        self.country = country
        self.city = city
        self.postal_code = postal_code
        self.street = street
        self.email = email
        self.phone = phone

        self.branch_id = branch_id
        self.position_id = position_id

        self.salary = salary

    def hash_password(self, password):
        return pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    # def fake_json(self):
    #     return {'username': self.username, 'password_hash': self.password_hash, 'branch_id': self.branch_id,
    #             'position_id': self.position_id, 'salary': self.salary}

    def json(self):
        return {'id': self.id, 'username': self.username, 'first_name': self.first_name, 'last_name': self.last_name,
                'country': self.country, 'city': self.city, 'postal_code': self.postal_code, 'street': self.street,
                'email': self.email, 'phone': self.phone, 'branch_id': self.branch_id, 'position_id': self.position_id,
                'salary': self.salary}

    def short_json(self):
        return {'first_name': self.first_name, 'last_name': self.last_name, 'city': self.city,
                'postal_code': self.postal_code, 'street': self.street, 'email': self.email, 'phone': self.phone}

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
    def find_by_branch_id(cls, branch_id):
        return cls.query.filter_by(branch_id=branch_id)

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
