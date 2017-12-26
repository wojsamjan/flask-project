from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.branch import BranchModel


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

    def get(self, name):
        branch = BranchModel.find_by_name(name)
        if branch:
            return branch.short_json()
        return {'message': 'Branch not found'}, 404

    @jwt_required()
    def post(self, name):
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
        branch = BranchModel.find_by_name(name)
        if branch:
            branch.delete_from_db

        return {'message': 'Branch deleted.'}

    @jwt_required()
    def put(self, name):
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
    def get(self, country=""):
        if country:
            return {'branches': [branch.short_json() for branch in BranchModel.query.filter_by(country=country)]}
        else:
            return {'branches': [branch.short_json() for branch in BranchModel.query.all()]}


# class Store(Resource):
#     def get(self, name):
#         store = StoreModel.find_by_name(name)
#         if store:
#             return store.json()
#         return {'message': 'Store not found'}, 404
#
#     def post(self, name):
#         if StoreModel.find_by_name(name):
#             return {'message': "A store with name '{}' already exists.".format(name)}, 400
#
#         store = StoreModel(name)
#         try:
#             store.save_to_db()
#         except:
#             return {'message': 'An error occurred while creating the store.'}, 500
#
#         return store.json(), 201
#
#     def delete(self, name):
#         store = StoreModel.find_by_name(name)
#         if store:
#             store.delete_from_db()
#
#         return {'message': 'Store deleted'}
#
#
# class StoreList(Resource):
#     def get(self):
#         return {'store': [store.json() for store in StoreModel.query.all()]}
