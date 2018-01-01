from werkzeug.security import safe_str_cmp
from flask import g
from models.user import UserModel
from models.customer import CustomerModel


def authenticate(username, password):
    user = UserModel.find_by_username(username)
    customer = CustomerModel.find_by_username(username)
    # password_hash = user.hash_password(password)
    # print(password_hash)
    # print(user.password_hash)
    # if user and safe_str_cmp(user.password_hash, password_hash):
    if user and user.verify_password(password):
        print('authXXX')
        # g.user = user
        return user
    elif customer and customer.verify_password(password):
        return customer


def identity(payload):
    _id = payload['identity']
    print(payload)
    user = UserModel.find_by_id(_id)
    customer = CustomerModel.find_by_id(_id)
    if user:
        g.user = user
        return user
    else:
        g.customer = customer
        return customer

    # return UserModel.find_by_id(user_id)
