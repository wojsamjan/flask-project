from flask import g
from models.position import PositionModel


# [base]: resources/item.py   [usage]: resources/log.py
admin = 'admin'
manager = 'manager'


def is_employee():
    try:
        if g.user:
            return True
    except:
        return False


def is_manager():
    is_user = is_employee()
    if not is_user:
        return False

    user = g.user
    user_position = PositionModel.find_by_id(user.position_id)

    if user_position.name != manager:
        return False
    return True


def is_admin():
    is_user = is_employee()
    if not is_user:
        return False

    user = g.user
    user_position = PositionModel.find_by_id(user.position_id)

    if user_position.name != admin:
        return False
    return True
