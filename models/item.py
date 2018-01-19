from db import db
from models.branch import BranchModel


class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    price = db.Column(db.Float(precision=2))

    available = db.Column(db.Integer)
    reserved_by = db.Column(db.String(40))

    year = db.Column(db.Integer)
    item_type = db.Column(db.String(30))
    vendor = db.Column(db.String(30))
    model = db.Column(db.String(40))

    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'))
    branch = db.relationship('BranchModel')

    def __init__(self, name, price, year, item_type, vendor, model, branch_id):
        self.id
        self.name = name  # ItemType-Vendor-Model-Number(first available from 1) ex: narty-atomic-extra-1
        self.price = price

        self.available = 1
        self.reserved_by = None

        self.year = year
        self.item_type = item_type
        self.vendor = vendor
        self.model = model

        self.branch_id = branch_id

    def json(self):
        return {'id': self.id, 'name': self.name, 'price': self.price, 'available': self.available,
                'reserved_by': self.reserved_by, 'year': self.year, 'item_type': self.item_type, 'vendor': self.vendor,
                'model': self.model, 'branch_id': self.branch_id}

    def short_json(self):
        return {'name': self.name, 'price': self.price, 'available': self.available,  # 'reserved_by': self.reserved_by,
                'year': self.year, 'item_type': self.item_type, 'vendor': self.vendor, 'model': self.model,
                'branch_id': (BranchModel.find_by_id(self.branch_id)).name}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()  # SELECT * FROM items WHERE name=name LIMIT 1

    @classmethod
    def find_by_name_in_branch(cls, branch_id, name):
        return cls.query.filter_by(branch_id=branch_id, name=name).first()

    @staticmethod
    def is_item_type(item_type):
        return item_type in ["ski", "snowboard", "surfing-board", "bike", "rollerblades", "longboard",
                             "tent", "sleeping-bag", "gps", "caravan", "cool-box", "rucksack"]  # "pedalo",

    def save_to_db(self):  # updating or upserting data
        db.session.add(self)  # We can add multiple objects to session and then commit once - more efficient
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
