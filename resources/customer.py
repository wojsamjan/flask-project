from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from flask import g
from models.customer import CustomerModel
from models.user import UserModel
from models.position import PositionModel


class CustomerRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help="Every account needs a username!"
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="Every account needs a password!"
    )

    def post(self):
        data = CustomerRegister.parser.parse_args()

        if CustomerModel.find_by_username(data['username']) or UserModel.find_by_username(data['username']):
            return {"message": "An account with that username already exists"}, 400

        customer = CustomerModel(**data)  # CustomerModel(data['username'], data['password'])
        customer.save_to_db()

        # return {'customer': customer.fake_json()}, 201
        # return {'customers': [customer.short_json() for customer in CustomerModel.query.all()]}, 201
        return {"message": "Account created successfully."}, 201


class CustomerChangePassword(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('old_password',
        type=str,
        required=True,
        help="To change your password you need to type the current one!"
    )
    parser.add_argument('new_password',
        type=str,
        required=True,
        help="To change your password you need to type the new one!"
    )

    @jwt_required()
    def put(self):
        try:
            if g.user:
                return {'message': 'You are not privileged to continue!'}
        except:
            pass

        data = CustomerChangePassword.parser.parse_args()
        customer = g.customer

        if not customer.verify_password(data['old_password']):
            return {'message': 'You can not change your password because you have typed wrong current one!'}, 400

        customer.password_hash = customer.hash_password(data['new_password'])
        customer.save_to_db()

        return {'message': 'Your password has been changed successfully!'}


class CustomerDelete(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',  # customer.username
        type=str,
        required=True,
        help="To delete an account you need to type the username!"
    )
    parser.add_argument('password',  # user.password or customer.password
        type=str,
        required=True,
        help="To delete an account you need to type the password!"
    )

    @jwt_required()
    def delete(self):
        is_user = False
        try:
            if g.user:
                is_user = True
        except:
            pass

        data = CustomerDelete.parser.parse_args()

        if is_user:
            user = g.user
            position = PositionModel.find_by_id(user.position_id)

            if position.name != 'admin' or not user.verify_password(data['password']):
                return {'message': "You are not privileged to delete customer's account!"}, 400

            customer = CustomerModel.find_by_username(data['username'])
            if customer:
                customer.delete_from_db()
                return {'message': "Customer's account deleted."}

            return {'message': "Customer '{}' account does not exist.".format(data['username'])}
        else:
            customer = g.customer

            if customer.username != data['username']:
                return {'message': 'You can not delete your account because you have typed wrong username!'}, 400

            if not customer.verify_password(data['password']):
                return {'message': 'You can not delete your account because you have typed wrong password!'}, 400

        customer.delete_from_db()

        return {'message': 'Your account is deleted.'}
