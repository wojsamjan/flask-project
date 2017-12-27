from db import db


class PositionModel(db.Model):
    __tablename__ = 'positions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    # salary = db.Column(db.Integer)

    users = db.relationship('UserModel', lazy='dynamic')

    def __init__(self, name):
        self.id
        self.name = name
        # self.salary = salary

    def json(self):
        # return {'name': self.name, 'salary': self.salary, 'users': [user.json() for user in self.users.all()]}
        return {'id': self.id, 'name': self.name, 'users': [user.json() for user in self.users.all()]}

    # def short_json(self):
    #     return {'id': self.id, 'name': self.name, 'users': [user.short_json() for user in self.users.all()]}

    def branch_json(self, branch_id):
        return {'id': self.id, 'name': self.name, 'users': [user.json() for user in self.users.filter_by(branch_id=branch_id)]}

    # def branch_short_json(self, branch_id):
    #     return {'id': self.id, 'name': self.name, 'users': [user.short_json() for user in self.users.filter_by(branch_id=branch_id)]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()  # SELECT * FROM positions WHERE name=name LIMIT 1

    def save_to_db(self):
        db.session.add(self)  # We can add multiple objects to session and then commit once - more efficient
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
