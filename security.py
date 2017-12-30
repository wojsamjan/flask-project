from werkzeug.security import safe_str_cmp
from models.user import UserModel


def authenticate(username, password):
    user = UserModel.find_by_username(username)
    # password_hash = user.hash_password(password)
    # print(password_hash)
    # print(user.password_hash)
    # if user and safe_str_cmp(user.password_hash, password_hash):
    if user and user.verify_password(password):
        return user


def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
