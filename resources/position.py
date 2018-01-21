from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from flask import g
from models.position import PositionModel
from models.branch import BranchModel
from models.user import UserModel
import helpers.resource_validators as validators


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
            if g.user:
                return True
        except:
            return False

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
        is_admin = Position.is_admin()
        if not is_admin:
            return {'message': 'You are not privileged to continue!'}, 400

        position = PositionModel.find_by_name(name)
        if position:
            return position.json()
        return {'message': 'Position not found.'}, 404

    @jwt_required()  # this too
    def post(self, name):
        # begin
        is_admin = Position.is_admin()
        if not is_admin:
            return {'message': 'You are not privileged to continue!'}, 400
        # end

        data = Position.parser.parse_args()
        validators.position_validator(**data)

        user = g.user  # this

        # start
        if not user.verify_password(data['password']):
            return {'message': 'You can not add a new position because you have typed a wrong password!'}, 400
        # end

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

        return {'message': 'Position deleted.'}

    @jwt_required()
    def put(self, name):
        is_admin = Position.is_admin()
        if not is_admin:
            return {'message': 'You are not privileged to continue!'}, 400

        data = Position.parser.parse_args()
        validators.position_validator(**data)

        user = g.user

        if not user.verify_password(data['password']):
            return {'message': 'You can not update a position because you have typed a wrong password!'}, 400

        position = PositionModel.find_by_name(name)

        if position is None:
            position = PositionModel(name)
        # else:
        #     position.name = name

        position.save_to_db()

        return position.json()


class PositionList(Resource):
    @jwt_required()
    def get(self, branch_name=""):
        is_admin = Position.is_admin()
        is_manager = Position.is_manager()

        if not is_admin and not is_manager:
            return {'message': 'You are not privileged to continue!'}, 400

        # all branches
        if not branch_name:
            if not is_admin:
                return {'message': 'You are not privileged to continue!'}, 400
            return {'positions': [position.json() for position in PositionModel.query.all()]}

        # specific branch
        branch = BranchModel.find_by_name(branch_name)
        if not branch:
            return {'message': 'Branch not found.'}, 404

        positions_id = {user.position_id for user in UserModel.query.filter_by(branch_id=branch.id)}

        if not is_admin:
            if g.user.branch_id != branch.id:
                return {'message': 'You are not privileged to continue!'}, 400
            return {'positions': [position.branch_short_json(branch.id) for position in PositionModel.query.filter(PositionModel.id.in_(positions_id)).all()]}
        return {'positions': [position.branch_json(branch.id) for position in PositionModel.query.filter(PositionModel.id.in_(positions_id)).all()]}
