import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from flask_cors import CORS

from security import authenticate, identity
from resources.user import UserRegister, UserChangePassword, UserDelete, UserList, UserDetails
from resources.item import Item, ItemList, ItemReserve, ItemCancelReservation, ItemListAdmin, ItemReservedByList, \
    ItemReservedListForAdmin
from resources.car import Car, CarList, CarReserve, CarCancelReservation, CarListAdmin, CarReservedByList, \
    CarReservedListForAdmin
from resources.branch import Branch, BranchList
from resources.position import Position, PositionList
from resources.customer import CustomerRegister, CustomerChangePassword, CustomerDelete, CustomerList, CustomerDetails
from resources.auth import Continue, Dashboard
from resources.dev_testing import Devel
from resources.log import Log, LogList


app = Flask(__name__)
CORS(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # It turns off Flask SQLAlchemy Tracker, no SQLAlchemy Tracker
app.secret_key = 'stan'
api = Api(app)

# start global comment
# development:
@app.before_first_request
def create_tables():
    db.create_all()
# end global comment

jwt = JWT(app, authenticate, identity)  # /auth

api.add_resource(Item, '/<string:branch_name>/item/<string:name>')  # http://127.0.0.1:5000/branch_namr/item/item_name
api.add_resource(ItemList, '/<string:branch_name>/items',
                 '/<string:branch_name>/items/<string:param>/<string:value_p>')
api.add_resource(ItemListAdmin, '/items',
                 '/items/<string:param>/<string:value_p>')

api.add_resource(ItemReserve, '/<string:branch_name>/item/reserve/<string:name>')
api.add_resource(ItemCancelReservation, '/<string:branch_name>/item/cancel-reservation/<string:name>')
api.add_resource(ItemReservedByList, '/item-reserved-by-list')
api.add_resource(ItemReservedListForAdmin, '/item-reserved-list-for-admin/<string:username>')

api.add_resource(Car, '/<string:branch_name>/car/<string:name>')
api.add_resource(CarList, '/<string:branch_name>/cars',
                 '/<string:branch_name>/cars/<string:param>/<string:value_p>')
api.add_resource(CarListAdmin, '/cars',
                 '/cars/<string:param>/<string:value_p>')

api.add_resource(CarReserve, '/<string:branch_name>/car/reserve/<string:name>')
api.add_resource(CarCancelReservation, '/<string:branch_name>/car/cancel-reservation/<string:name>')
api.add_resource(CarReservedByList, '/car-reserved-by-list')
api.add_resource(CarReservedListForAdmin, '/car-reserved-list-for-admin/<string:username>')

api.add_resource(Branch, '/branch/<string:name>')
api.add_resource(BranchList, '/branches',
                 '/branches/<string:country>')

api.add_resource(Position, '/position/<string:name>')
api.add_resource(PositionList, '/positions',
                 '/<string:branch_name>/positions')

api.add_resource(UserRegister, '/register-user')
api.add_resource(UserChangePassword, '/change-password-user')
api.add_resource(UserDelete, '/delete-user')
api.add_resource(UserDetails, '/user-details/<string:user_name>')
api.add_resource(UserList, '/users')

api.add_resource(CustomerRegister, '/register')
api.add_resource(CustomerChangePassword, '/change-password')
api.add_resource(CustomerDelete, '/delete')
api.add_resource(CustomerDetails, '/customer-details/<string:customer_name>')
api.add_resource(CustomerList, '/customers')

api.add_resource(Continue, '/continue')
api.add_resource(Dashboard, '/dashboard')

api.add_resource(Devel, '/dev-testing/<string:fk_id>')
api.add_resource(Log, '/log/<string:_id>')
api.add_resource(LogList, '/logs')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
