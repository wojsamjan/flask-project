from string import ascii_letters as letters
from string import ascii_lowercase as lowercase
from string import ascii_uppercase as uppercase
from string import digits


def country_city_validator(country):
    country_city_regex = letters + ' ' + '-'
    for sign in country:
        if sign not in country_city_regex:
            return {'validator message': 'Incorrect country and/or city name.'}
    return {'validator message': 'OK'}


def postal_code_validator(postal_code):
    postal_regex = digits + ' ' + '-'
    for sign in postal_code:
        if sign not in postal_regex:
            return {'validator message': 'Incorrect postal code.'}
    return {'validator message': 'OK'}


def street_validator(street):
    street_regex = letters + digits + ' ' + '-'
    for sign in street:
        if sign not in street_regex:
            return {'validator message': 'Incorrect street name.'}
    return {'validator message': 'OK'}


def email_validator(email):
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
