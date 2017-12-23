from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList, ItemReserve
# from resources.store import Store, StoreList
from resources.car import Car, CarList, CarReserve
from resources.branch import Branch, BranchList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # It turns off Flask SQLAlchemy Tracker, no SQLAlchemy Tracker
app.secret_key = 'stan'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity)  # /auth

# api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')  # http://127.0.0.1:5000/item/item_name
api.add_resource(ItemList, '/items',
                 '/items/<string:param>/<string:value_p>')
api.add_resource(ItemReserve, '/item/reserve/<string:name>')
# api.add_resource(StoreList, '/stores')

api.add_resource(Car, '/car/<string:name>')
api.add_resource(CarList, '/cars',
                 '/cars/<string:param>/<string:value_p>')
api.add_resource(CarReserve, '/car/reserve/<string:name>')

api.add_resource(Branch, '/branch/<string:name>')
api.add_resource(BranchList, '/branches',
                 '/branches/<string:country>')

api.add_resource(UserRegister, '/register')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
