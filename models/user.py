from db import db
from passlib.apps import custom_app_context as pwd_context


class UserModel(db.Model):  # db.Model -> tells SQLAlchemy about relation
    __tablename__ = 'users'  # where to save our UserModel in database using SQLAlchemy

    id = db.Column(db.Integer, primary_key=True)  # specifies columns in database for our UserModel
    username = db.Column(db.String(80))
    password_hash = db.Column(db.String(128))

    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'))
    branch = db.relationship('BranchModel')

    position_id = db.Column(db.Integer, db.ForeignKey('positions.id'))
    position = db.relationship('PositionModel')

    salary = db.Column(db.Integer)

    def __init__(self, username, password, branch_id, position_id, salary):
        self.username = username
        # self.password = password

        self.password_hash = self.hash_password(password)

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
        return {'username': self.username, 'branch_id': self.branch_id, 'position_id': self.position_id,
                'salary': self.salary}

    def short_json(self):
        return {'username': self.username, 'branch_id': self.branch_id, 'position_id': self.position_id,
                'salary': self.salary}

    def save_to_db(self):
        db.session.add(self)
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
