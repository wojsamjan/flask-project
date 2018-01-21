import helpers.validators as hv


# position password
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


# password
def customer_register_validator(username, first_name, last_name, email, phone):
    # password
    args = [username, first_name, last_name, email, phone]
    # password
    validators = [hv.username_validator, hv.first_name_validator, hv.last_name_validator, hv.email_validator,
                  hv.phone_validator]

    if len(args) != len(validators):
        return {'customer validator': 'Incorrect number of passed arguments.'}

    validator_results = [validator(arg) for validator in validators for arg in args]
    error_results = [result for result in validator_results if len(result['validator message']) > 2]

    return {'error results': error_results}


# customer change password


# password
def customer_delete_validator(username):
    args = [username]
    validators = [hv.username_validator]

    if len(args) != len(validators):
        return {'customer validator': 'Incorrect number of passed arguments.'}

    validator_results = [validator(arg) for validator in validators for arg in args]
    error_results = [result for result in validator_results if len(result['validator message']) > 2]

    return {'error results': error_results}


# password
def user_validator(username, first_name, last_name, country, city, postal_code, street, email, phone, branch_id,
                   position_id, salary):
    args = [username, first_name, last_name, country, city, postal_code, street, email, phone, branch_id,
            position_id, salary]
    validators = [hv.username_validator, hv.first_name_validator, hv.last_name_validator, hv.country_validator,
                  hv.city_validator, hv.postal_code_validator, hv.street_validator, hv.email_validator,
                  hv.phone_validator, hv.branch_id_validator, hv.position_id_validator, hv.salary_validator]

    if len(args) != len(validators):
        return {'branch validator': 'Incorrect number of passed arguments.'}

    validator_results = [validator(arg) for validator in validators for arg in args]
    error_results = [result for result in validator_results if len(result['validator message']) > 2]

    return {'error results': error_results}
