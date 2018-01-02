from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from flask import g
from models.position import PositionModel
from models.branch import BranchModel
from models.user import UserModel


class Position(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('password',
        type=str,
        required=True,
        help="To work with positions you need to type your password!"
    )
    admin = 'admin'
    manager = 'manager'

    @staticmethod
    def is_user():
        try:
            if g.customer:
                return False
        except:
            return True

    @staticmethod
    def is_manager():
        is_user = Position.is_user()
        if not is_user:
            return False

        user = g.user
        user_position = PositionModel.find_by_id(user.position_id)

        if user_position.name != Position.manager:
            return False

        return True

    @staticmethod
    def is_admin():
        is_user = Position.is_user()
        if not is_user:
            return False

        user = g.user
        user_position = PositionModel.find_by_id(user.position_id)

        if user_position.name != Position.admin:
            return False

        return True

    @jwt_required()
    def get(self, name):
        # try:
        #     if g.customer:
        #         return {'message': 'You are not privileged to continue!'}, 400
        # except:
        #     pass
        #
        # user = g.user
        # user_position = PositionModel.find_by_id(user.position_id)
        #
        # if user_position.name != Position.admin:
        #     return {'message': 'You are not privileged user to continue!'}, 400

        is_admin = Position.is_admin()
        if not is_admin:
            return {'message': 'You are not privileged to continue!'}, 400

        data = Position.parser.parse_args()
        user = g.user

        if not user.verify_password(data['password']):
            return {'message': 'You can not check a position because you have typed a wrong password!'}, 400

        position = PositionModel.find_by_name(name)
        if position:
            return position.json()
        return {'message': 'Position not found'}, 404

    @jwt_required()
    def post(self, name):
        is_admin = Position.is_admin()
        if not is_admin:
            return {'message': 'You are not privileged to continue!'}, 400

        data = Position.parser.parse_args()
        user = g.user

        if not user.verify_password(data['password']):
            return {'message': 'You can not add a new position because you have typed a wrong password!'}, 400

        if PositionModel.find_by_name(name):
            return {'message': "A position with name '{}' already exists.".format(name)}, 400

        position = PositionModel(name)

        try:
            position.save_to_db()
        except:
            return {'message': 'An error occurred while creating the position.'}, 500

        return position.json(), 201

    @jwt_required()
    def delete(self, name):
        is_admin = Position.is_admin()
        if not is_admin:
            return {'message': 'You are not privileged to continue!'}, 400

        data = Position.parser.parse_args()
        user = g.user

        if not user.verify_password(data['password']):
            return {'message': 'You can not delete a position because you have typed a wrong password!'}, 400

        position = PositionModel.find_by_name(name)
        if position:
            position.delete_from_db()

        return {'message': 'Position deleted'}

    @jwt_required()
    def put(self, name):
        is_admin = Position.is_admin()
        if not is_admin:
            return {'message': 'You are not privileged to continue!'}, 400

        data = Position.parser.parse_args()
        user = g.user

        if not user.verify_password(data['password']):
            return {'message': 'You can not update a position because you have typed a wrong password!'}, 400

        position = PositionModel.find_by_name(name)

        if position is None:
            position = PositionModel(name)
        else:
            position.name = name

        position.save_to_db()

        return position.json()


class PositionList(Resource):
    def get(self, branch_name=""):
        if not branch_name:
            return {'positions': [position.json() for position in PositionModel.query.all()]}

        branch = BranchModel.find_by_name(branch_name)
        if not branch:
            return {'message': 'Branch not found.'}, 404

        # return {'id of br': branch.id}  # gdansk => 1 GOOD
        positions_id = {user.position_id for user in UserModel.query.filter_by(branch_id=branch.id)}
        # return {'ids': [num for num in positions_id]}  # gdansk => [1, 2, 4] GOOD
        # return {'end': 'end'}
        # return {'positions': [position.json() for position in PositionModel.query.filter_by(id in positions_id)]}
        return {'positions': [position.branch_json(branch.id) for position in PositionModel.query.filter(PositionModel.id.in_(positions_id)).all()]}
