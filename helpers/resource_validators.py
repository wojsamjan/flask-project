import helpers.validators as hv


def position_validator(password):
    args = [password]
    validators = [hv.password_validator]

    if len(args) != len(validators):
        return {'customer validator': 'Incorrect number of passed arguments.'}

    validator_results = [validator(arg) for validator in validators for arg in args]
    error_results = [result for result in validator_results if len(result['validator message']) > 2]

    return {'error results': error_results}


def branch_validator(country, city, postal_code, street, email, phone):
    args = [country, city, postal_code, street, email, phone]
    validators = [hv.country_validator, hv.city_validator, hv.postal_code_validator, hv.street_validator,
                  hv.email_validator, hv.phone_validator]

    if len(args) != len(validators):
        return {'branch validator': 'Incorrect number of passed arguments.'}

    validator_results = [validator(arg) for validator in validators for arg in args]
    # print(list(filter(lambda x: x != 13, my_list)))
    # [y for y in a if y not in b]
    error_results = [result for result in validator_results if len(result['validator message']) > 2]

    return {'error results': error_results}


def customer_register_validator(username, password, first_name, last_name, email, phone):
    args = [username, password, first_name, last_name, email, phone]
    validators = [hv.username_validator, hv.password_validator, hv.first_name_validator, hv.last_name_validator,
                  hv.email_validator, hv.phone_validator]

    if len(args) != len(validators):
        return {'customer validator': 'Incorrect number of passed arguments.'}

    validator_results = [validator(arg) for validator in validators for arg in args]
    error_results = [result for result in validator_results if len(result['validator message']) > 2]

    return {'error results': error_results}


def change_password_validator(old_password, new_password):
    args = [old_password, new_password]
    validators = [hv.password_validator, hv.password_validator]

    if len(args) != len(validators):
        return {'customer validator': 'Incorrect number of passed arguments.'}

    validator_results = [validator(arg) for validator in validators for arg in args]
    error_results = [result for result in validator_results if len(result['validator message']) > 2]

    return {'error results': error_results}


def delete_validator(username, password):
    args = [username, password]
    validators = [hv.username_validator, hv.password_validator]

    if len(args) != len(validators):
        return {'customer validator': 'Incorrect number of passed arguments.'}

    validator_results = [validator(arg) for validator in validators for arg in args]
    error_results = [result for result in validator_results if len(result['validator message']) > 2]

    return {'error results': error_results}


def user_register_validator(username, password, first_name, last_name, country, city, postal_code, street, email,
                            phone, branch_id, position_id, salary):
    args = [username, password, first_name, last_name, country, city, postal_code, street, email, phone, branch_id,
            position_id, salary]
    validators = [hv.username_validator, hv.password_validator, hv.first_name_validator, hv.last_name_validator,
                  hv.country_validator, hv.city_validator, hv.postal_code_validator, hv.street_validator,
                  hv.email_validator, hv.phone_validator, hv.branch_id_validator, hv.position_id_validator,
                  hv.salary_validator]

    if len(args) != len(validators):
        return {'branch validator': 'Incorrect number of passed arguments.'}

    validator_results = [validator(arg) for validator in validators for arg in args]
    error_results = [result for result in validator_results if len(result['validator message']) > 2]

    return {'error results': error_results}


def item_validator(price, year, item_type, vendor, model, branch_id):
    args = [price, year, item_type, vendor, model, branch_id]
    validators = [hv.price_validator, hv.year_validator, hv.item_type_validator, hv.vendor_validator,
                  hv.model_validator, hv.branch_id_validator]

    if len(args) != len(validators):
        return {'branch validator': 'Incorrect number of passed arguments.'}

    validator_results = [validator(arg) for validator in validators for arg in args]
    error_results = [result for result in validator_results if len(result['validator message']) > 2]

    return {'error results': error_results}


def car_validator(price, year, car_type, vendor, model, colour, seats, transmission, drive, fuel, engine_power,
                  branch_id):
    args = [price, year, car_type, vendor, model, colour, seats, transmission, drive, fuel, engine_power, branch_id]
    validators = [hv.price_validator, hv.year_validator, hv.car_type_validator, hv.vendor_validator,
                  hv.model_validator, hv.colour_validator, hv.seats_validator, hv.transmission_validator,
                  hv.drive_validator, hv.fuel_validator, hv.engine_power_validator, hv.branch_id_validator]

    if len(args) != len(validators):
        return {'branch validator': 'Incorrect number of passed arguments.'}

    validator_results = [validator(arg) for validator in validators for arg in args]
    error_results = [result for result in validator_results if len(result['validator message']) > 2]

    return {'error results': error_results}
