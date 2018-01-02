from db import db


class BranchModel(db.Model):
    __tablename__ = 'branches'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    country = db.Column(db.String(40))
    city = db.Column(db.String(40))
    postal_code = db.Column(db.String(16))
    street = db.Column(db.String(40))
    email = db.Column(db.String(320))
    phone = db.Column(db.String(40))

    # items = db.relationship('ItemModel', lazy='dynamic')  # list of items

    users = db.relationship('UserModel', lazy='dynamic')
    cars = db.relationship('CarModel', lazy='dynamic')
    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name, country, city, postal_code, street, email, phone):
        self.id

        self.name = name

        self.country = country
        self.city = city
        self.postal_code = postal_code
        self.street = street
        self.email = email
        self.phone = phone

    def json(self):
        # return {'name': self.name, 'items': [item.json() for item in self.items.all()]}
        return {
                'id': self.id, 'name': self.name, 'country': self.country, 'city': self.city,
                'postal_code': self.postal_code, 'street': self.street, 'email': self.email, 'phone': self.phone,
                'users': [user.json() for user in self.users.all()],
                'cars': [car.json() for car in self.cars.all()],
                'items': [item.json() for item in self.items.all()]
                }

    def short_json(self):
        return {
                'id': self.id, 'name': self.name, 'country': self.country, 'city': self.city, 'street': self.street,
                'users': [user.short_json() for user in self.users.all()],  # short_json fake_json
                'cars': [car.short_json() for car in self.cars.all()],
                'items': [item.short_json() for item in self.items.all()]
                }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()  # SELECT * FROM branches WHERE name=name LIMIT 1

    def save_to_db(self):
        db.session.add(self)  # We can add multiple objects to session and then commit once - more efficient
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
