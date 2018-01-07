from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from flask import g
from models.user import UserModel
from models.customer import CustomerModel
from models.position import PositionModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help="Every user needs a username!"
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="Every user needs a password!"
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

    parser.add_argument('country',
        type=str,
        required=True,
        help="Every user needs a country!"
    )
    parser.add_argument('city',
        type=str,
        required=True,
        help="Every user needs a city!"
    )
    parser.add_argument('postal_code',
        type=str,
        required=True,
        help="Every user needs a postal code!"
    )
    parser.add_argument('street',
        type=str,
        required=True,
        help="Every user needs a street!"
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

    parser.add_argument('branch_id',
        type=int,
        required=True,
        help="Every user needs a branch_id!"
    )
    parser.add_argument('position_id',
        type=int,
        required=True,
        help="Every user needs a position_id!"
    )
    parser.add_argument('salary',
        type=int,
        required=True,
        help="Every user needs a salary!"
    )

    @jwt_required()
    def post(self):
        try:
            user = g.user
        except:
            return {'message': "You are not privileged to continue!"}, 400

        data = UserRegister.parser.parse_args()
        position = PositionModel.find_by_id(user.position_id)

        print(position)

        if position.name != 'admin':
            return {'message': "You are not privileged to create user's account!"}, 400

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists."}, 400

        if CustomerModel.find_by_username(data['username']):
            return {"message": "A customer with that username already exists."}, 400

        user = UserModel(**data)
        user.save_to_db()

        # return {'user': user.fake_json()}, 201
        # return {'users': [user.short_json() for user in UserModel.query.all()]}, 201
        return {"message": "User created successfully."}, 201

    # def post(self):
    #     data = UserRegister.parser.parse_args()
    #
    #     if UserModel.find_by_username(data['username']):
    #         return {"message": "A user with that username already exists."}, 400
    #
    #     if CustomerModel.find_by_username(data['username']):
    #         return {"message": "A customer with that username already exists."}, 400
    #
    #     user = UserModel(**data)
    #     user.save_to_db()
    #
    #     # return {'user': user.fake_json()}, 201
    #     # return {'users': [user.short_json() for user in UserModel.query.all()]}, 201
    #     return {"message": "User created successfully."}, 201


class UserChangePassword(Resource):
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
            if g.customer:
                return {'message': 'You are not privileged to continue!'}, 400
        except:
            pass

        data = UserChangePassword.parser.parse_args()
        user = g.user

        if not user.verify_password(data['old_password']):
            return {'message': 'You can not change your password because you have typed wrong current one!'}, 400

        user.password_hash = user.hash_password(data['new_password'])
        user.save_to_db()

        return {'message': 'Your password has been changed successfully!'}


class UserDelete(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',  # user.username
        type=str,
        required=True,
        help="To delete an account you need to type the username!"
    )
    parser.add_argument('password',  # user.password or [admin]user.password
        type=str,
        required=True,
        help="To delete an account you need to type the password!"
    )

    @jwt_required()
    def delete(self):
        try:
            if g.customer:
                return {'message': 'You are not privileged to continue!'}, 400
        except:
            pass

        data = UserDelete.parser.parse_args()

        user = g.user
        position = PositionModel.find_by_id(user.position_id)
        if position.name == 'admin':
            if not user.verify_password(data['password']):
                return {'message': "You are not privileged to delete user's account!"}, 400

            user_delete = UserModel.find_by_username(data['username'])
            if user_delete:
                user_delete.delete_from_db()
                return {'message': "User's account deleted."}

            return {'message': "User '{}' account does not exist.".format(data['username'])}
        else:

            if user.username != data['username']:
                return {'message': 'You can not delete your account because you have typed wrong username!'}, 400

            if not user.verify_password(data['password']):
                return {'message': 'You can not delete your account because you have typed wrong password!'}, 400

        user.delete_from_db()

        return {'message': 'Your account is deleted.'}
