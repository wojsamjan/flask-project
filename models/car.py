from db import db
from models.branch import BranchModel


class CarModel(db.Model):
    __tablename__ = 'cars'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    available = db.Column(db.Integer)
    reserved_by = db.Column(db.String(40))

    year = db.Column(db.Integer)
    car_type = db.Column(db.String(20))
    vendor = db.Column(db.String(30))
    model = db.Column(db.String(40))
    colour = db.Column(db.String(20))
    seats = db.Column(db.Integer)
    transmission = db.Column(db.String(20))
    drive = db.Column(db.String(20))
    fuel = db.Column(db.String(20))
    engine_power = db.Column(db.Integer)

    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'))
    branch = db.relationship('BranchModel')

    def __init__(self, name, price, year, car_type, vendor, model, colour, seats,
                 transmission, drive, fuel, engine_power, branch_id):
        self.id
        # CarType-Vendor-Model-Number(first available from 1) ex: hatch-vw-golf3-1994-1, car-vw-golf-vi-2012-1
        self.name = name
        self.price = price

        self.available = 1
        self.reserved_by = None

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

    def json(self):
        return {
                'id': self.id, 'name': self.name, 'price': self.price, 'available': self.available,
                'reserved_by': self.reserved_by, 'year': self.year, 'car_type': self.car_type, 'vendor': self.vendor,
                'model': self.model, 'colour': self.colour, 'seats': self.seats, 'transmission': self.transmission,
                'drive': self.drive, 'fuel': self.fuel, 'engine_power': self.engine_power, 'branch_id': self.branch_id
                }

    def short_json(self):
        return {
                'name': self.name, 'price': self.price, 'available': self.available,  # 'reserved_by': self.reserved_by,
                'year': self.year, 'car_type': self.car_type, 'vendor': self.vendor, 'model': self.model,
                'seats': self.seats, 'transmission': self.transmission, 'drive': self.drive, 'fuel': self.fuel,
                'branch': (BranchModel.find_by_id(self.branch_id)).name
                }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_name_in_branch(cls, branch_id, name):
        return cls.query.filter_by(branch_id=branch_id, name=name).first()

    @staticmethod
    def is_car_type(car_type):
        # return car_type in ["delivery", "van", "sedan", "estate", "hatch", "coupe"]
        return car_type in ["car", "van"]

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
