from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList, ItemReserve
# from resources.store import Store, StoreList
from resources.car import Car, CarList, CarReserve
from resources.branch import Branch, BranchList
from resources.position import Position, PositionList

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
# api.add_resource(StoreList, '/stores')

api.add_resource(Item, '/<string:branch_name>/item/<string:name>')  # http://127.0.0.1:5000/branch_namr/item/item_name
api.add_resource(ItemList, '/<string:branch_name>/items',
                 '/<string:branch_name>/items/<string:param>/<string:value_p>')
api.add_resource(ItemReserve, '/<string:branch_name>/item/reserve/<string:name>')

api.add_resource(Car, '/<string:branch_name>/car/<string:name>')
api.add_resource(CarList, '/<string:branch_name>/cars',
                 '/<string:branch_name>/cars/<string:param>/<string:value_p>')
api.add_resource(CarReserve, '/<string:branch_name>/car/reserve/<string:name>')

api.add_resource(Branch, '/branch/<string:name>')
api.add_resource(BranchList, '/branches',
                 '/branches/<string:country>')

api.add_resource(Position, '/position/<string:name>')
api.add_resource(PositionList, '/positions',
                 '/<string:branch_name>/positions')

api.add_resource(UserRegister, '/register')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
