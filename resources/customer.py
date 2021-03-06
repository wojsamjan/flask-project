from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from flask import g
from models.customer import CustomerModel
from models.user import UserModel
from models.position import PositionModel
from models.log import LogModel
import helpers.resource_validators as validators
import helpers.authorizators as auth


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
    parser.add_argument('first_name',
        type=str,
        required=True,
        help="Every user needs a first_name!"
    )
    parser.add_argument('last_name',
        type=str,
        required=True,
        help="Every user needs a last_name!"
    )
    parser.add_argument('email',
        type=str,
        required=True,
        help="Every user needs a email!"
    )
    parser.add_argument('phone',
        type=str,
        required=True,
        help="Every user needs a phone!"
    )

    def post(self):
        data = CustomerRegister.parser.parse_args()
        error_validation = validators.customer_register_validator(**data)
        if error_validation['error validation']:
            return error_validation

        if CustomerModel.find_by_username(data['username']) or UserModel.find_by_username(data['username']):
            return {"message": "An account with that username already exists"}, 400

        customer = CustomerModel(**data)  # CustomerModel(data['username'], data['password'] ...)
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
                return {'message': 'You are not privileged to continue!'}, 400
        except:
            pass

        data = CustomerChangePassword.parser.parse_args()
        error_validation = validators.change_password_validator(**data)
        if error_validation['error validation']:
            return error_validation

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
    parser.add_argument('password',  # [ADMIN]user.password or customer.password
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
        error_validation = validators.delete_validator(**data)
        if error_validation['error validation']:
            return error_validation

        if is_user:
            user = g.user
            position = PositionModel.find_by_id(user.position_id)

            if position.name != 'admin' or not user.verify_password(data['password']):
                return {'message': "You are not privileged to delete customer's account!"}, 400

            customer = CustomerModel.find_by_username(data['username'])
            if customer:
                log = LogModel("remove customer '{}'".format(data['username']), g.user.username, auth.admin)
                customer.delete_from_db()
                log.save_to_db()

                return {'message': "Customer's account deleted."}

            return {'message': "Customer '{}' account does not exist.".format(data['username'])}
        else:
            customer = g.customer

            if customer.username != data['username']:
                return {'message': 'You can not delete your account because you have typed wrong username!'}, 400

            if not customer.verify_password(data['password']):
                return {'message': 'You can not delete your account because you have typed wrong password!'}, 400

        log = LogModel("remove customer '{}'".format(data['username']), g.customer.username, auth.customer)
        customer.delete_from_db()
        log.save_to_db()

        return {'message': 'Your account is deleted.'}


class CustomerDetails(Resource):
    @jwt_required()
    def get(self, customer_name):
        try:
            if g.customer:
                return {'message': 'You are not privileged to continue!'}, 400
        except:
            pass

        # position = PositionModel.find_by_id(g.user.position_id)
        # if position.name != 'admin':
        #     return {'message': "You are not privileged to check user details!"}, 400

        customer = CustomerModel.find_by_username(customer_name)
        if customer:
            return customer.json()

        return {'message': "Customer '{}' not found.".format(customer_name)}, 404


class CustomerList(Resource):
    @jwt_required()
    def get(self):
        is_user = False
        try:
            if g.user:
                is_user = True
        except:
            pass

        if not is_user:
            return {'message': 'You are not privileged to continue!'}, 400
        else:
            # user = g.user
            # position = PositionModel.find_by_id(user.position_id)
            #
            # if position.name != 'admin':
            #     return {'message': "You are not privileged to list customers accounts!"}, 400

            return {'customers': [customer.json() for customer in CustomerModel.query.all()]}
