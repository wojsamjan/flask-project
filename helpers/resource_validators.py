import helpers.validators as hv


def validator(args, validators, source):
    if len(args) != len(validators):
        return {source: 'Incorrect number of passed arguments.'}

    validator_results = list(map(lambda validator, arg: validator(arg), validators, args))
    error_results = [result for result in validator_results if len(result['validation message']) > 2]
    print(error_results)

    return {'error validation': error_results}


def position_validator(password):
    args = [password]
    validators = [hv.password_validator]

    return validator(args, validators, source='position validator')


def branch_validator(country, city, postal_code, street, email, phone):
    args = [country, city, postal_code, street, email, phone]
    print(args)
    validators = [hv.country_validator, hv.city_validator, hv.postal_code_validator, hv.street_validator,
                  hv.email_validator, hv.phone_validator]

    return validator(args, validators, source='branch validator')


def customer_register_validator(username, password, first_name, last_name, email, phone):
    args = [username, password, first_name, last_name, email, phone]
    validators = [hv.username_validator, hv.password_validator, hv.first_name_validator, hv.last_name_validator,
                  hv.email_validator, hv.phone_validator]

    return validator(args, validators, source='customer-register validator')


def change_password_validator(old_password, new_password):
    args = [old_password, new_password]
    validators = [hv.password_validator, hv.password_validator]

    return validator(args, validators, source='change-password validator')


def delete_validator(username, password):
    args = [username, password]
    validators = [hv.username_validator, hv.password_validator]

    return validator(args, validators, source='delete validator')


def user_register_validator(username, password, first_name, last_name, country, city, postal_code, street, email,
                            phone, branch_id, position_id, salary):
    args = [username, password, first_name, last_name, country, city, postal_code, street, email, phone, branch_id,
            position_id, salary]
    validators = [hv.username_validator, hv.password_validator, hv.first_name_validator, hv.last_name_validator,
                  hv.country_validator, hv.city_validator, hv.postal_code_validator, hv.street_validator,
                  hv.email_validator, hv.phone_validator, hv.branch_id_validator, hv.position_id_validator,
                  hv.salary_validator]

    return validator(args, validators, source='user-register validator')


def item_validator(price, year, item_type, vendor, model, branch_id):
    args = [price, year, item_type, vendor, model, branch_id]
    validators = [hv.price_validator, hv.year_validator, hv.item_type_validator, hv.vendor_validator,
                  hv.model_validator, hv.branch_id_validator]

    return validator(args, validators, source='item validator')


def car_validator(price, year, car_type, vendor, model, colour, seats, transmission, drive, fuel, engine_power,
                  branch_id):
    args = [price, year, car_type, vendor, model, colour, seats, transmission, drive, fuel, engine_power, branch_id]
    validators = [hv.price_validator, hv.year_validator, hv.car_type_validator, hv.vendor_validator,
                  hv.model_validator, hv.colour_validator, hv.seats_validator, hv.transmission_validator,
                  hv.drive_validator, hv.fuel_validator, hv.engine_power_validator, hv.branch_id_validator]

    return validator(args, validators, source='car validator')
