from db import db


# class ItemModel(db.Model):
class CarModel(db.Model):
    # __tablename__ = 'items'
    __tablename__ = 'cars'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    available = db.Column(db.Integer)

    year = db.Column(db.Integer)
    car_type = db.Column(db.String(20))
    vendor = db.Column(db.String(30))
    model = db.Column(db.String(20))
    colour = db.Column(db.String(20))
    seats = db.Column(db.Integer)
    transmission = db.Column(db.String(20))
    drive = db.Column(db.String(20))
    fuel = db.Column(db.String(20))
    engine_power = db.Column(db.Integer)

    # store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    # store = db.relationship('StoreModel')

    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'))
    branch = db.relationship('BranchModel')

    # def __init__(self, name, price, store_id):
    def __init__(self, name, price, year, car_type, vendor, model, colour, seats,
                 transmission, drive, fuel, engine_power, branch_id):
        self.id
        self.name = name  # CarType-Vendor-Model-Number(first available from 1) ex: hatch-vw-golf3-1994-1
        self.price = price
        # self.store_id = store_id

        self.available = 1

        self.year = year
        # self.mileage
        # self.registration_date
        # self.service_expiry
        # self.oc_expiry
        # self.ac_expiry
        self.car_type = car_type
        self.vendor = vendor
        self.model = model
        self.colour = colour
        self.seats = seats
        self.transmission = transmission
        self.drive = drive
        self.fuel = fuel
        # self.engine_size = engine_size
        self.engine_power = engine_power

        self.branch_id = branch_id

        #
        # self.name = vendor + "-" + model + "-" + str(year) + "-"
        #
        # self.number = 1
        #
        # while True:
        #     if CarModel.query.filter_by(name=(self.name + str(self.number))).first():
        #         self.number += 1
        #     else:
        #         self.name += str(self.number)
        #         break

    def json(self):
        return {
                'id': self.id, 'name': self.name, 'price': self.price, 'available': self.available, 'year': self.year,
                'car_type': self.car_type, 'vendor': self.vendor, 'model': self.model, 'colour': self.colour,
                'seats': self.seats, 'transmission': self.transmission, 'drive': self.drive, 'fuel': self.fuel,
                'engine_power': self.engine_power, 'branch_id': self.branch_id
                }

    def short_json(self):
        return {
                'id': self.id, 'name': self.name, 'price': self.price, 'available': self.available,
                'car_type': self.car_type, 'transmission': self.transmission, 'drive': self.drive,
                'branch_id': self.branch_id
                }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()  # SELECT * FROM cars WHERE name=name LIMIT 1

    @classmethod
    def find_by_name_in_branch(cls, branch_id, name):
        return cls.query.filter_by(branch_id=branch_id, name=name).first()

    @staticmethod
    def is_car_type(car_type):
        # return car_type in ["delivery", "van", "sedan", "estate", "hatch", "coupe"]
        return car_type in ["car", "van"]

    def save_to_db(self):  # updating or upserting data
        db.session.add(self)  # We can add multiple objects to session and then commit once - more efficient
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
