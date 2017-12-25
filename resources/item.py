from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel
from models.branch import BranchModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="Every item needs a price!"
    )
    # parser.add_argument('store_id',
    #     type=int,
    #     required=True,
    #     help="Every item needs a store id!"
    # )
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

    def get(self, branch_name, name):
        branch = BranchModel.find_by_name(branch_name)
        item = ItemModel.find_by_name_in_branch(branch.id, name)
        if item:
            return item.short_json()
        return {'message': 'Item not found.'}, 404

    @jwt_required()
    def post(self, branch_name, name):
        branch = BranchModel.find_by_name(branch_name)
        if ItemModel.find_by_name_in_branch(branch.id, name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)  # data['price'], data['store_id']

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500  # Internal Server Error

        return item.json(), 201

    @jwt_required()
    def delete(self, branch_name, name):
        branch = BranchModel.find_by_name(branch_name)
        item = ItemModel.find_by_name_in_branch(branch.id, name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted.'}

    @jwt_required()
    def put(self, branch_name, name):
        branch = BranchModel.find_by_name(branch_name)
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name_in_branch(branch.id, name)

        if item is None:
            item = ItemModel(name, **data)  # data['price'], data['store_id']
        else:
            item.price = data['price']
            item.year = data['year']
            item.item_type = data['item_type']
            item.vendor = data['vendor']
            item.model = data['model']
            # item.store_id = data['store_id']

            item.branch_id = data['branch_id']

        item.save_to_db()

        return item.json()


class ItemReserve(Resource):
    def put(self, branch_name, name):
        branch = BranchModel.find_by_name(branch_name)
        item = ItemModel.find_by_name_in_branch(branch.id, name)

        if item is None:
            return {'message': 'Item does not exist.'}

        if item.available == 0:
            return {"message": "Item is already reserved."}, 400

        item.available = 0

        item.save_to_db()

        return item.short_json()


class ItemList(Resource):
    def get(self, branch_name="", param="", value_p=""):
        branch = BranchModel.find_by_name(branch_name)
        if not branch:
            return {'message': 'Branch not found.'}, 404
        # if param == "item-type" and (value_p == "ski" or value_p == "snowboard" or value_p == "surfing-board" or value_p == "pedalo" or value_p == "bike" or value_p == "rollerblades" or value_p == "longboard" or value_p == "tent" or value_p == "sleeping-bag" or value_p == "gps" or value_p == "caravan" or value_p == "cool-box" or value_p == "rucksack"):
        if param == "item-type" and ItemModel.is_item_type(value_p):
            return {'items': [item.short_json() for item in ItemModel.query.filter_by(item_type=value_p, branch_id=branch.id)]}
        elif not param:
            return {'items': [item.short_json() for item in ItemModel.query.filter_by(branch_id=branch.id)]}
            # return {'items': [item.json() for item in ItemModel.query.all()]}  # list comprehension
        else:
            return {'message': 'Wrong parameters of request!'}
            # return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}  # lambda, mapping func() to elements
