import helpers.validators as hv


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
