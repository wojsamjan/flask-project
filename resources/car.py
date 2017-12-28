from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.car import CarModel
from models.branch import BranchModel


class Car(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="Every car needs a price!"
    )
    parser.add_argument('year',
        type=int,
        required=True,
        help="Every car needs a year of production!"
    )
    parser.add_argument('car_type',
        type=str,
        required=True,
        help="Every car needs a car_type!"
    )
    parser.add_argument('vendor',
        type=str,
        required=True,
        help="Every car needs a vendor!"
    )
    parser.add_argument('model',
        type=str,
        required=True,
        help="Every car needs a model!"
    )
    parser.add_argument('colour',
        type=str,
        required=True,
        help="Every car needs a colour!"
    )
    parser.add_argument('seats',
        type=int,
        required=True,
        help="Every car needs a number of seats!"
    )
    parser.add_argument('transmission',
        type=str,
        required=True,
        help="Every car needs a transmission!"
    )
    parser.add_argument('drive',
        type=str,
        required=True,
        help="Every car needs a drive!"
    )
    parser.add_argument('fuel',
        type=str,
        required=True,
        help="Every car needs a fuel!"
    )
    parser.add_argument('engine_power',
        type=int,
        required=True,
        help="Every car needs a engine_power!"
    )
    parser.add_argument('branch_id',
        type=int,
        required=True,
        help="Every car needs a branch_id!"
    )

    def get(self, branch_name, name):
        branch = BranchModel.find_by_name(branch_name)
        car = CarModel.find_by_name_in_branch(branch.id, name)
        if car:
            return car.short_json()
        return {'message': 'Car not found.'}, 404

    @jwt_required()
    def post(self, branch_name, name):
        branch = BranchModel.find_by_name(branch_name)
        # return {'brid': branch.id}
        if not branch:
            return {'message': "Branch '{}' does not exist.".format(branch_name)}, 400

        data = Car.parser.parse_args()

        if branch.id != data['branch_id']:
            return {'message': "Branch: '{}' and id: '{}' does not suit with each other.".format(branch_name, data['branch_id'])}

        if CarModel.find_by_name_in_branch(branch.id, name):
            return {'message': "An car with name '{}' already exists.".format(name)}, 400

        car = CarModel(name, **data)  # data['price'], data['store_id']

        try:
            car.save_to_db()
        except:
            return {"message": "An error occurred inserting the car."}, 500  # Internal Server Error

        return car.json(), 201

    @jwt_required()
    def delete(self, branch_name, name):
        branch = BranchModel.find_by_name(branch_name)
        car = CarModel.find_by_name_in_branch(branch.id, name)
        if car:
            car.delete_from_db()

        return {'message': 'Car deleted.'}

    @jwt_required()
    def put(self, branch_name, name):
        data = Car.parser.parse_args()

        branch = BranchModel.find_by_name(branch_name)
        if not branch:
            return {'message': "Branch '{}' does not exist.".format(branch_name)}, 400
        car = CarModel.find_by_name_in_branch(branch.id, name)

        if car is None:
            car = CarModel(name, **data)  # data['price'], data['store_id']
        else:
            car.price = data['price']
            car.year = data['year']
            car.car_type = data['car_type']
            car.vendor = data['vendor']
            car.model = data['model']
            car.colour = data['colour']
            car.seats = data['seats']
            car.transmission = data['transmission']
            car.drive = data['drive']
            car.fuel = data['fuel']
            car.engine_power = data['engine_power']

            car.branch_id = data['branch_id']

        car.save_to_db()

        return car.json()


class CarReserve(Resource):
    def put(self, branch_name, name):
        branch = BranchModel.find_by_name(branch_name)
        car = CarModel.find_by_name_in_branch(branch.id, name)

        if car is None:
            return {'message': 'Car does not exist.'}

        if car.available == 0:
            return {"message": "Car is already reserved."}, 400

        car.available = 0

        car.save_to_db()

        return car.short_json()


class CarList(Resource):
    def get(self, branch_name="", param="", value_p=""):
        # return {'b': branch_name, 'p': param, 'v': value_p}

        # /cars
        if not branch_name and not param and not value_p:
            return {'cars': [car.short_json() for car in CarModel.query.all()]}

        branch = BranchModel.find_by_name(branch_name)

        # /<non existent branch>/cars
        if not branch and branch_name:
            return {'message': 'Branch not found.'}, 404

        # if param == "car-type" and (value_p == "delivery" or value_p == "van" or value_p == "sedan" or value_p == "estate" or value_p == "hatch" or value_p == "coupe"):
        if param == "car-type" and CarModel.is_car_type(value_p):
            if branch:
                return {'cars': [car.short_json() for car in CarModel.query.filter_by(car_type=value_p, branch_id=branch.id)]}
            return {'cars': [car.short_json() for car in CarModel.query.filter_by(car_type=value_p)]}
        elif param == "transmission" and value_p == "automatic":
            if branch:
                return {'cars': [car.short_json() for car in CarModel.query.filter_by(transmission=value_p, branch_id=branch.id)]}
            return {'cars': [car.short_json() for car in CarModel.query.filter_by(transmission=value_p)]}
        elif param == "drive" and value_p == "4wd":
            if branch:
                return {'cars': [car.short_json() for car in CarModel.query.filter_by(drive=value_p, branch_id=branch.id)]}
            return {'cars': [car.short_json() for car in CarModel.query.filter_by(drive=value_p)]}
        elif not param:
            if branch:
                return {'cars': [car.short_json() for car in CarModel.query.filter_by(branch_id=branch.id)]}
            return {'cars': [car.short_json() for car in CarModel.query.all()]}
            # return {'cars': [car.json() for car in CarModel.query.all()]}  # list comprehension
            # return {'cars': list(map(lambda x: x.json(), CarModel.query.all()))}  # lambda, mapping func() to elements
        else:
            return {'message': 'Wrong parameters of request!'}, 400


#       return cls.query.filter_by(name=name).first()
