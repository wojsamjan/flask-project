from flask_restful import Resource
import helpers.validators as hv


class Devel(Resource):
    def get(self, fk_id):
        result = hv.branch_id_validator(fk_id)
        result = hv.position_id_validator(fk_id)
        result = hv.salary_validator(1000000)
        return result
