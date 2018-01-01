from flask import g
from models.user import UserModel
from models.customer import CustomerModel


def authenticate(username, password):
    user = UserModel.find_by_username(username)
    customer = CustomerModel.find_by_username(username)
    # print('authXXX')
    if user and user.verify_password(password):
        return user
    elif customer and customer.verify_password(password):
        return customer


def identity(payload):
    _id = payload['identity']
    # print(payload)
    user = UserModel.find_by_id(_id)
    customer = CustomerModel.find_by_id(_id)
    if user:
        print("as user")
        g.user = user
        return user
    else:
        print("as customer")
        g.customer = customer
        return customer
