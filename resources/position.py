from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.position import PositionModel
from models.branch import BranchModel
from models.user import UserModel


class Position(Resource):
    # parser = reqparse.RequestParser()
    # parser.add_argument('salary',
    #     type=int,  # str float
    #     required=True,
    #     help="Every position needs a salary!"
    # )

    def get(self, name):
        position = PositionModel.find_by_name(name)
        if position:
            return position.json()
        return {'message': 'Position not found'}, 404

    @jwt_required()
    def post(self, name):
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
        position = PositionModel.find_by_name(name)
        if position:
            position.delete_from_db()

        return {'message': 'Position deleted'}

    @jwt_required()
    def put(self, name):
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

        positions_id = {user.position_id for user in UserModel.query.filter_by(branch_id=branch.id)}
        return {'positions': [position.json() for position in PositionModel.query.filter_by(id in positions_id)]}
