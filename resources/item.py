from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from flask import g
from models.item import ItemModel
from models.branch import BranchModel
from models.position import PositionModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="Every item needs a price!"
    )
    parser.add_argument('year',
        type=int,
        required=True,
        help="Every item needs a year of production!"
    )
    parser.add_argument('item_type',
        type=str,
        required=True,
        help="Every item needs an item_type!"
    )
    parser.add_argument('vendor',
        type=str,
        required=True,
        help="Every item needs a vendor!"
    )
    parser.add_argument('model',
        type=str,
        required=True,
        help="Every item needs a model!"
    )
    parser.add_argument('branch_id',
        type=int,
        required=True,
        help="Every item needs a branch_id!"
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
        is_user = Item.is_user()
        if not is_user:
            return False

        user = g.user
        user_position = PositionModel.find_by_id(user.position_id)

        if user_position.name != Item.manager:
            return False
        return True

    @staticmethod
    def is_admin():
        is_user = Item.is_user()
        if not is_user:
            return False

        user = g.user
        user_position = PositionModel.find_by_id(user.position_id)

        if user_position.name != Item.admin:
            return False
        return True

    def get(self, branch_name, name):
        branch = BranchModel.find_by_name(branch_name)
        if not branch:
            return {'message': "Branch '{}' does not exist.".format(branch_name)}, 400

        item = ItemModel.find_by_name_in_branch(branch.id, name)
        is_admin = Item.is_admin()

        if item:
            if not is_admin:
                return item.short_json()
            return item.json()

        return {'message': 'Item not found.'}, 404

    @jwt_required()
    def post(self, branch_name, name):
        is_admin = Item.is_admin()
        is_manager = Item.is_manager()

        if not is_admin and not is_manager:
            return {'message': 'You are not privileged to continue!'}, 400

        branch = BranchModel.find_by_name(branch_name)
        if not branch:
            return {'message': "Branch '{}' does not exist.".format(branch_name)}, 400

        if g.user.branch_id != branch.id and not is_admin:
            return {'message': 'You are not privileged to continue!'}, 400

        data = Item.parser.parse_args()

        if branch.id != data['branch_id']:
            return {'message': "Branch: '{}' and id: '{}' does not suit with each other.".format(branch_name, data['branch_id'])}

        if ItemModel.find_by_name_in_branch(branch.id, name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        item = ItemModel(name, **data)  # data['price'], ..., data['branch_id']

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500  # Internal Server Error

        if not is_admin:
            return item.short_json(), 201
        return item.json(), 201

    @jwt_required()
    def delete(self, branch_name, name):
        is_admin = Item.is_admin()
        if not is_admin:
            return {'message': 'You are not privileged to continue!'}, 400

        branch = BranchModel.find_by_name(branch_name)
        if not branch:
            return {'message': "Branch '{}' does not exist.".format(branch_name)}, 400

        item = ItemModel.find_by_name_in_branch(branch.id, name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted.'}

    @jwt_required()
    def put(self, branch_name, name):
        is_admin = Item.is_admin()
        if not is_admin:
            return {'message': 'You are not privileged to continue!'}, 400

        branch = BranchModel.find_by_name(branch_name)
        if not branch:
            return {'message': "Branch '{}' does not exist.".format(branch_name)}, 400

        data = Item.parser.parse_args()
        item = ItemModel.find_by_name_in_branch(branch.id, name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
            item.year = data['year']
            item.item_type = data['item_type']
            item.vendor = data['vendor']
            item.model = data['model']

            item.branch_id = data['branch_id']

        item.save_to_db()

        return item.json()


class ItemReserve(Resource):
    @jwt_required()
    def put(self, branch_name, name):
        branch = BranchModel.find_by_name(branch_name)
        if not branch:
            return {'message': "Branch '{}' does not exist.".format(branch_name)}, 400

        item = ItemModel.find_by_name_in_branch(branch.id, name)

        if item is None:
            return {'message': 'Item does not exist.'}

        if item.available == 0:
            return {"message": "Item is already reserved."}, 400

        item.available = 0
        is_user = Item.is_user()
        if is_user:
            item.reserved_by = g.user.username
        else:
            item.reserved_by = g.customer.username

        item.save_to_db()

        # return item.short_json()
        return {"message": "Item reserved."}


class ItemCancelReservation(Resource):
    @jwt_required()
    def put(self, branch_name, name):
        is_user = Item.is_user()

        branch = BranchModel.find_by_name(branch_name)
        if not branch:
            return {'message': "Branch '{}' does not exist.".format(branch_name)}, 400

        item = ItemModel.find_by_name_in_branch(branch.id, name)

        if item is None:
            return {'message': 'Item does not exist.'}

        if item.available == 1:
            return {"message": "Item is not reserved yet."}, 400

        if not is_user:
            if not g.customer.username == item.reserved_by:
                return {'message': 'You are not privileged to continue!'}, 400

        # branch = BranchModel.find_by_name(branch_name)
        # if not branch:
        #     return {'message': "Branch '{}' does not exist.".format(branch_name)}, 400
        #
        # item = ItemModel.find_by_name_in_branch(branch.id, name)

        # if item is None:
        #     return {'message': 'Item does not exist.'}
        #
        # if item.available == 1:
        #     return {"message": "Item is not reserved yet."}, 400

        item.available = 1
        item.reserved_by = None

        item.save_to_db()

        # return item.short_json()
        return {'message': 'Item reservation canceled.'}


class ItemList(Resource):
    def get(self, branch_name="", param="", value_p=""):
        branch = BranchModel.find_by_name(branch_name)

        # /<non existent branch>/items
        # /<non existent branch>/items/<param>/<value_p>
        if not branch:
            return {'message': 'Branch not found.'}, 404

        if param == "item-type" and ItemModel.is_item_type(value_p):
            return {'items': [item.short_json() for item in ItemModel.query.filter_by(item_type=value_p, branch_id=branch.id)]}
        elif not param:
            return {'items': [item.short_json() for item in ItemModel.query.filter_by(branch_id=branch.id)]}
            # return {'items': [item.json() for item in ItemModel.query.all()]}  # list comprehension
        else:
            return {'message': 'Wrong parameters of request!'}, 400
            # return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}  # lambda, map func() to elements


class ItemReservedByList(Resource):
    @jwt_required()
    def get(self):
        if Item.is_user():
            user = g.user
            return {'items': [item.short_json() for item in ItemModel.query.filter_by(reserved_by=user.username)]}
        else:
            customer = g.customer
            return {'items': [item.short_json() for item in ItemModel.query.filter_by(reserved_by=customer.username)]}


class ItemListAdmin(Resource):
    @jwt_required()
    def get(self, param="", value_p=""):
        is_admin = Item.is_admin()

        print('ADMIN ITEMS LIST')

        if not is_admin:
            return {'message': 'You are not privileged to continue!'}, 400

        if param == "item-type" and ItemModel.is_item_type(value_p):
            return {'items': [item.json() for item in ItemModel.query.filter_by(item_type=value_p)]}
        elif not param:
            # /items
            return {'items': [item.json() for item in ItemModel.query.all()]}
        else:
            return {'message': 'Wrong parameters of request!'}, 400
