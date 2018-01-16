from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from flask import g
from models.position import PositionModel


class Continue(Resource):
    admin = 'admin'
    manager = 'manager'
    user = 'user'
    customer = 'customer'

    @staticmethod
    def is_user():
        try:
            if g.user:
                return True
        except:
            return False

    @staticmethod
    def is_manager():
        is_user = Continue.is_user()
        if not is_user:
            return False

        user = g.user
        user_position = PositionModel.find_by_id(user.position_id)

        if user_position.name != Continue.manager:
            return False
        return True

    @staticmethod
    def is_admin():
        is_user = Continue.is_user()
        if not is_user:
            return False

        user = g.user
        user_position = PositionModel.find_by_id(user.position_id)

        if user_position.name != Continue.admin:
            return False
        return True

    @jwt_required()
    def get(self):
        if not Continue.is_user():
            return {'role': Continue.customer}
        elif Continue.is_admin():
            return {'role': Continue.admin}
        elif Continue.is_manager():
            return {'role': Continue.manager}
        return {'role': Continue.user}


class Dashboard(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('role',
        type=str,
        required=True,
        help="You need a role to continue!"
    )

    admin = 'admin'
    manager = 'manager'
    user = 'user'
    it_specialist = 'it specialist'
    customer_service = 'customer service'
    customer = 'customer'

    @staticmethod
    def is_user():
        try:
            if g.user:
                return True
        except:
            return False

    @staticmethod
    def is_manager():
        is_user = Dashboard.is_user()
        if not is_user:
            return False

        user = g.user
        user_position = PositionModel.find_by_id(user.position_id)

        if user_position.name != Dashboard.manager:
            return False
        return True

    @staticmethod
    def is_admin():
        is_user = Dashboard.is_user()
        if not is_user:
            return False

        user = g.user
        user_position = PositionModel.find_by_id(user.position_id)

        if user_position.name != Dashboard.admin:
            return False
        return True

    @jwt_required()
    def post(self):
        data = Dashboard.parser.parse_args()

        users = [Dashboard.it_specialist, Dashboard.customer_service]

        print(data['role'])

        if not Dashboard.is_user() and data['role'] == Dashboard.customer:
            print('CUSTOMER DASHBOARD')
            return {'message': 'passed'}

        position = PositionModel.find_by_id(g.user.position_id)
        role = position.name

        if Dashboard.is_admin() and role == data['role']:
            return {'message': 'passed'}
        elif Dashboard.is_manager() and role == data['role']:
            return {'message': 'passed'}
        elif Dashboard.is_user() and data['role'] == Dashboard.user and role in users:
            return {'message': 'passed'}

        return {'message': 'failed'}
