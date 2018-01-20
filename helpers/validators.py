from string import ascii_letters as letters
# from string import ascii_lowercase as lowercase
# from string import ascii_uppercase as uppercase
from string import digits


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


# customer
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
