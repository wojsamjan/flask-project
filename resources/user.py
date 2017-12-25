import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


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

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        user = UserModel(**data)  # UserModel(data['username'], data['password'])
        user.save_to_db()

        return {"message": "User created successfully."}, 201
