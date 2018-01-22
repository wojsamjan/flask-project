from db import db
import datetime


def _get_date():
    return datetime.datetime.now()


class LogModel(db.Model):
    __tablename__ = 'logs'

    id = db.Column(db.Integer, primary_key=True)
    action_name = db.Column(db.String(40))
    action_date = db.Column(db.Date, default=_get_date())
    action_creator = db.Column(db.String(40))
    creator_role = db.Column(db.String(60))

    def __init__(self, action_name, action_creator, creator_role):
        self.id
        self.action_name = action_name
        self.action_date
        self.action_creator = action_creator
        self.creator_role = creator_role

    def json(self):
        return {'id': self.id, 'action_name': self.action_name, 'action_date': self.action_date}

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    # datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    # datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
