from flask_restful import Resource
from flask_jwt import jwt_required
import helpers.authorizators as auth
from models.log import LogModel


class Log(Resource):
    @jwt_required()
    def get(self, _id):
        log = LogModel.find_by_id(int(_id))
        is_admin = auth.is_admin()

        if log:
            if not is_admin:
                return {'message': 'You are not privileged to continue!'}, 400
            return log.json()

        return {'message': 'Log not found.'}, 404

    @jwt_required()
    def delete(self, _id):
        log = LogModel.find_by_id(int(_id))
        is_admin = auth.is_admin()

        if log:
            if not is_admin:
                return {'message': 'You are not privileged to continue!'}, 400
            log.delete_from_db()
            return {'message': 'Item deleted.'}

        return {'message': 'Log not found.'}, 404


class LogList(Resource):
    @jwt_required()
    def get(self):
        is_admin = auth.is_admin()

        if not is_admin:
            return {'message': 'You are not privileged to continue!'}, 400

        return {'logs': [log.json() for log in LogModel.query.all()]}
