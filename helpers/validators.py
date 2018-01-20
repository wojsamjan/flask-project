from string import ascii_letters as letters
from string import ascii_lowercase as lowercase
from string import ascii_uppercase as uppercase
from string import digits


def country_city_validator(country):
    country_city_regex = letters + ' ' + '-'
    for sign in country:
        if sign not in country_city_regex:
            return False
    return True


def postal_code_validator(postal_code):
    postal_regex = digits + ' ' + '-'
    for sign in postal_code:
        if sign not in postal_regex:
            return False
    return True


def street_validator(street):
    street_regex = letters + digits + ' ' + '-'
    for sign in street:
        if sign not in street_regex:
            return False
    return True
