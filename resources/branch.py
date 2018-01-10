import string
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from flask import g
from models.branch import BranchModel
from models.position import PositionModel


class Branch(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('country',
        type=str,
        required=True,
        help="Every branch needs a country!"
    )
    parser.add_argument('city',
        type=str,
        required=True,
        help="Every branch needs a city!"
    )
    parser.add_argument('postal_code',
        type=str,
        required=True,
        help="Every branch needs a postal code!"
    )
    parser.add_argument('street',
        type=str,
        required=True,
        help="Every branch needs a street!"
    )
    parser.add_argument('email',
        type=str,
        required=True,
        help="Every branch needs a email!"
    )
    parser.add_argument('phone',
        type=str,
        required=True,
        help="Every branch needs a phone!"
    )

    admin = 'admin'

    @staticmethod
    def is_admin():
        try:
            if g.customer:
                return False
        except:
            pass

        user = g.user
        user_position = PositionModel.find_by_id(user.position_id)

        if user_position.name != Branch.admin:
            return False

        return True

    @jwt_required()
    def get(self, name):
        is_admin = Branch.is_admin()
        if not is_admin:
            return {'message': 'You are not privileged to continue!'}, 400

        branch = BranchModel.find_by_name(name)
        if branch:
            return branch.json()
        return {'message': 'Branch not found.'}, 404

    # @jwt_required()  # this too
    def post(self, name):
        # begin
        # is_admin = Branch.is_admin()
        # if not is_admin:
        #     return {'message': 'You are not privileged to continue!'}, 400
        # end

        if BranchModel.find_by_name(name):
            return {'message': "A branch with name '{} already exists.".format(name)}, 400

        data = Branch.parser.parse_args()

        branch = BranchModel(name, **data)

        try:
            branch.save_to_db()
        except:
            return {'message': 'An error occurred inserting the branch.'}, 500  # Internal Server Error

        return branch.json(), 201

    @jwt_required()
    def delete(self, name):
        is_admin = Branch.is_admin()
        if not is_admin:
            return {'message': 'You are not privileged to continue!'}, 400

        branch = BranchModel.find_by_name(name)
        if branch:
            branch.delete_from_db()

        return {'message': 'Branch deleted.'}

    @jwt_required()
    def put(self, name):
        is_admin = Branch.is_admin()
        if not is_admin:
            return {'message': 'You are not privileged to continue!'}, 400

        data = Branch.parser.parse_args()

        branch = BranchModel.find_by_name(name)

        if branch is None:
            branch = BranchModel(name, **data)
        else:
            branch.country = data['country']
            branch.city = data['city']
            branch.postal_code = data['postal_code']
            branch.street = data['street']
            branch.email = data['email']
            branch.phone = data['phone']

        branch.save_to_db()

        return branch.json()


class BranchList(Resource):
    @jwt_required()
    def get(self, country=""):
        is_admin = Branch.is_admin()
        if not is_admin:
            return {'message': 'You are not privileged to continue!'}, 400

        if country:
            country = string.capwords(country)
            return {'branches': [branch.json() for branch in BranchModel.query.filter_by(country=country)]}
        else:
            return {'branches': [branch.json() for branch in BranchModel.query.all()]}
