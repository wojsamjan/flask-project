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
        return {'validation message': 'Incorrect country length(40).'}

    country_regex = letters + ' ' + '-'
    for sign in country:
        if sign not in country_regex:
            return {'validation message': 'Incorrect country name.'}
    return {'validation message': 'OK'}


def city_validator(city):
    if len(city) > 40:
        return {'validation message': 'Incorrect city length(40).'}

    city_regex = letters + ' ' + '-'
    for sign in city:
        if sign not in city_regex:
            return {'validation message': 'Incorrect city name.'}
    return {'validation message': 'OK'}


def postal_code_validator(postal_code):
    if len(postal_code) > 16:
        return {'validation message': 'Incorrect postal code length(16).'}

    postal_regex = digits + ' ' + '-'
    for sign in postal_code:
        if sign not in postal_regex:
            return {'validation message': 'Incorrect postal code.'}
    return {'validation message': 'OK'}


def street_validator(street):
    if len(street) > 40:
        return {'validation message': 'Incorrect street length(40).'}

    street_regex = letters + digits + ' ' + '-'
    for sign in street:
        if sign not in street_regex:
            return {'validation message': 'Incorrect street name.'}
    return {'validation message': 'OK'}


def email_validator(email):
    if len(email) > 320:
        return {'validation message': 'Incorrect email length(320).'}

    email_regex = letters + digits + '-' + '.'
    at_counter = 0
    for sign in email:
        if sign not in email_regex:
            if sign == '@':
                at_counter += 1
                if at_counter > 1:
                    return False
            return False
    return {'validation message': 'OK'}


def phone_validator(phone):
    if len(phone) > 40:
        return {'validation message': 'Incorrect phone length(40).'}

    phone_regex = digits + ' ' + '-'
    for sign in phone:
        if sign not in phone_regex:
            return {'validation message': 'Incorrect phone number.'}
    return {'validation message': 'OK'}


# customer PASSWORD ??
def username_validator(username):
    if len(username) > 40:
        return {'validation message': 'Incorrect username length(40).'}
    return {'validation message': 'OK'}


def password_validator(password):
    if len(password) > 24:
        return {'validation message': 'Incorrect password length(24).'}
    return {'validation message': 'OK'}


def first_name_validator(first_name):
    if len(first_name) > 40:
        return {'validation message': 'Incorrect first name length(40).'}

    first_name_regex = letters + ' ' + '-'
    for sign in first_name:
        if sign not in first_name_regex:
            return {'validation message': 'Incorrect first name.'}
    return {'validation message': 'OK'}


def last_name_validator(last_name):
    if len(last_name) > 40:
        return {'validation message': 'Incorrect last name length(40).'}

    last_name_regex = letters + ' ' + '-'
    for sign in last_name:
        if sign not in last_name_regex:
            return {'validation message': 'Incorrect last name.'}
    return {'validation message': 'OK'}


# user TOO SMALL   TOO BIG
def branch_id_validator(branch_id):
    # branch_id = int(branch_id)
    # min_branch = BranchModel.query.order_by(BranchModel.id.asc()).first()
    # max_branch = BranchModel.query.order_by(BranchModel.id.desc()).first()
    # # print(max_branch.name)
    # if branch_id < 0:
    #     return {'validation message': 'Incorrect branch index.'}
    # elif min_branch.id > branch_id:
    #     return {'validation message': 'Too small branch index.'}
    # elif max_branch.id < branch_id:
    #     return {'validation message': 'Too big branch index.'}
    branch = BranchModel.query.filter_by(id=int(branch_id)).first()
    # print(branch.id)
    if not branch:
        return {'validation message': 'Incorrect branch index.'}
    return {'validation message': 'OK'}


def position_id_validator(position_id):
    position = PositionModel.query.filter_by(id=int(position_id)).first()
    # print(position.id)
    if not position:
        return {'validation message': 'Incorrect position index.'}
    return {'validation message': 'OK'}


def salary_validator(salary):
    # salary_regex = digits + ' ' + '-' + '.'
    salary_regex = digits
    for digit in str(salary):
        if digit not in salary_regex:
            return {'validation message': 'Incorrect salary.'}

    if salary < 0 or salary > 1000000:
        return {'validation message': 'Incorrect salary. It must be <0-1.000.000>.'}
    return {'validation message': 'OK'}


# item
def price_validator(price):
    price_regex = digits
    for digit in str(price):
        if digit not in price_regex:
            return {'validation message': 'Incorrect price.'}

    if price <= 0 or price >= 10000:
        return {'validation message': 'Incorrect price.'}
    return {'validation message': 'OK'}


def year_validator(year):
    year_regex = digits
    for digit in str(year):
        if digit not in year_regex:
            return {'validation message': 'Incorrect year.'}

    if year < 1900 or year > 2018:
        return {'validation message': 'Incorrect year.'}
    return {'validation message': 'OK'}


def item_type_validator(item_type):
    if len(item_type) > 30:
        return {'validation message': 'Incorrect item type length(30).'}
    return {'validation message': 'OK'}


def vendor_validator(vendor):
    if len(vendor) > 30:
        return {'validation message': 'Incorrect vendor length(30).'}
    return {'validation message': 'OK'}


def model_validator(model):
    if len(model) > 40:
        return {'validation message': 'Incorrect model length(40).'}
    return {'validation message': 'OK'}


# car
def car_type_validator(car_type):
    if len(car_type) > 20:
        return {'validation message': 'Incorrect car type length(20).'}
    return {'validation message': 'OK'}


def colour_validator(colour):
    if len(colour) > 20:
        return {'validation message': 'Incorrect colour length(20).'}

    colour_regex = letters + ' ' + '-'
    for sign in colour:
        if sign not in colour_regex:
            return {'validation message': 'Incorrect colour.'}
    return {'validation message': 'OK'}


def seats_validator(seats):
    seats_regex = digits
    for digit in str(seats):
        if digit not in seats_regex:
            return {'validation message': 'Incorrect seats.'}

    if seats < 1 or seats > 120:
        return {'validation message': 'Incorrect seats number.'}
    return {'validation message': 'OK'}


def transmission_validator(transmission):
    if len(transmission) > 20:
        return {'validation message': 'Incorrect transmission length(20).'}

    transmission_regex = letters + ' ' + '-'
    for sign in transmission:
        if sign not in transmission_regex:
            return {'validation message': 'Incorrect transmission.'}
    return {'validation message': 'OK'}


def drive_validator(drive):
    if len(drive) > 20:
        return {'validation message': 'Incorrect drive length(20).'}

    drive_regex = letters + digits + ' ' + '-'
    for sign in drive:
        if sign not in drive_regex:
            return {'validation message': 'Incorrect drive.'}
    return {'validation message': 'OK'}


def fuel_validator(fuel):
    if len(fuel) > 20:
        return {'validation message': 'Incorrect fuel length(20).'}

    fuel_regex = letters + digits + ' ' + '-'
    for sign in fuel:
        if sign not in fuel_regex:
            return {'validation message': 'Incorrect fuel.'}
    return {'validation message': 'OK'}


def engine_power_validator(engine_power):
    engine_power_regex = digits
    for digit in str(engine_power):
        if digit not in engine_power_regex:
            return {'validation message': 'Incorrect engine power.'}

    if engine_power < 1 or engine_power > 2500:
        return {'validation message': 'Incorrect engine power.'}
    return {'validation message': 'OK'}
