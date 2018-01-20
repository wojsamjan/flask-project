from string import ascii_letters as letters
# from string import ascii_lowercase as lowercase
# from string import ascii_uppercase as uppercase
from string import digits
from models.position import PositionModel
from models.branch import BranchModel


# position
# branch
def country_validator(country):
    if len(country) > 40:
        return {'validator message': 'Incorrect country length(40).'}

    country_regex = letters + ' ' + '-'
    for sign in country:
        if sign not in country_regex:
            return {'validator message': 'Incorrect country name.'}
    return {'validator message': 'OK'}


def city_validator(city):
    if len(city) > 40:
        return {'validator message': 'Incorrect city length(40).'}

    city_regex = letters + ' ' + '-'
    for sign in city:
        if sign not in city_regex:
            return {'validator message': 'Incorrect city name.'}
    return {'validator message': 'OK'}


def postal_code_validator(postal_code):
    if len(postal_code) > 16:
        return {'validator message': 'Incorrect postal code length(16).'}

    postal_regex = digits + ' ' + '-'
    for sign in postal_code:
        if sign not in postal_regex:
            return {'validator message': 'Incorrect postal code.'}
    return {'validator message': 'OK'}


def street_validator(street):
    if len(street) > 40:
        return {'validator message': 'Incorrect street length(40).'}

    street_regex = letters + digits + ' ' + '-'
    for sign in street:
        if sign not in street_regex:
            return {'validator message': 'Incorrect street name.'}
    return {'validator message': 'OK'}


def email_validator(email):
    if len(email) > 320:
        return {'validator message': 'Incorrect email length(320).'}

    email_regex = letters + digits + '-' + '.'
    at_counter = 0
    for sign in email:
        if sign not in email_regex:
            if sign == '@':
                at_counter += 1
                if at_counter > 1:
                    return False
            return False
    return {'validator message': 'OK'}


def phone_validator(phone):
    if len(phone) > 40:
        return {'validator message': 'Incorrect phone length(40).'}

    phone_regex = digits + ' ' + '-'
    for sign in phone:
        if sign not in phone_regex:
            return {'validator message': 'Incorrect phone number.'}
    return {'validator message': 'OK'}


# customer PASSWORD ??
def username_validator(username):
    if len(username) > 40:
        return {'validator message': 'Incorrect username length(40).'}
    return {'validator message': 'OK'}


def first_name_validator(first_name):
    if len(first_name) > 40:
        return {'validator message': 'Incorrect first name length(40).'}

    first_name_regex = letters + ' ' + '-'
    for sign in first_name:
        if sign not in first_name_regex:
            return {'validator message': 'Incorrect first name.'}
    return {'validator message': 'OK'}


def last_name_validator(last_name):
    if len(last_name) > 40:
        return {'validator message': 'Incorrect last name length(40).'}

    last_name_regex = letters + ' ' + '-'
    for sign in last_name:
        if sign not in last_name_regex:
            return {'validator message': 'Incorrect last name.'}
    return {'validator message': 'OK'}


# user TOO SMALL   TOO BIG
def branch_id_validator(branch_id):
    # branch_id = int(branch_id)
    # min_branch = BranchModel.query.order_by(BranchModel.id.asc()).first()
    # max_branch = BranchModel.query.order_by(BranchModel.id.desc()).first()
    # # print(max_branch.name)
    # if branch_id < 0:
    #     return {'validator message': 'Incorrect branch index.'}
    # elif min_branch.id > branch_id:
    #     return {'validator message': 'Too small branch index.'}
    # elif max_branch.id < branch_id:
    #     return {'validator message': 'Too big branch index.'}
    branch = BranchModel.query.filter_by(id=int(branch_id)).first()
    # print(branch.id)
    if not branch:
        return {'validator message': 'Incorrect branch index.'}
    return {'validator message': 'OK'}


def position_id_validator(position_id):
    position = PositionModel.query.filter_by(id=int(position_id)).first()
    # print(position.id)
    if not position:
        return {'validator message': 'Incorrect position index.'}
    return {'validator message': 'OK'}


def salary_validator(salary):
    # salary_regex = digits + ' ' + '-' + '.'
    salary_regex = digits + ' ' + '.'
    for digit in str(salary):
        if digit not in salary_regex:
            return {'validator message': 'Incorrect salary.'}

    if salary < 0 or salary > 1000000:
        return {'validator message': 'Incorrect salary. It must be <0-1.000.000>.'}

    return {'validator message': 'OK'}


# item
def price_validator(price):
    price_regex = digits + ' ' + '.'
    for digit in str(price):
        if digit not in price_regex:
            return {'validator message': 'Incorrect price.'}

    if price <= 0 or price >= 10000:
        return {'validator message': 'Incorrect price.'}

    return {'validator message': 'OK'}


def year_validator(year):
    if year < 1900 or year > 2018:
        return {'validator message': 'Incorrect year.'}
    return {'validator message': 'OK'}


def item_type_validator(item_type):
    if len(item_type) > 30:
        return {'validator message': 'Incorrect item type length(30).'}
    return {'validator message': 'OK'}


def vendor_validator(vendor):
    if len(vendor) > 30:
        return {'validator message': 'Incorrect vendor length(30).'}
    return {'validator message': 'OK'}


def model_validator(model):
    if len(model) > 40:
        return {'validator message': 'Incorrect model length(40).'}
    return {'validator message': 'OK'}


def car_type_validator(car_type):
    if len(car_type) > 20:
        return {'validator message': 'Incorrect car type length(20).'}
    return {'validator message': 'OK'}


def colour_validator(colour):
    if len(colour) > 20:
        return {'validator message': 'Incorrect colour length(20).'}
    return {'validator message': 'OK'}

    colour_regex = letters + ' ' + '-'
    for sign in colour:
        if sign not in colour_regex:
            return {'validator message': 'Incorrect colour.'}
    return {'validator message': 'OK'}


def seats_validator(seats):
    if seats < 1 or seats > 120:
        return {'validator message': 'Incorrect seats number.'}
    return {'validator message': 'OK'}
