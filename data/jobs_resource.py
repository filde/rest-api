from flask_restful import reqparse, abort, Api, Resource
from flask import jsonify
from .jobs import Jobs
from . import db_session


parser = reqparse.RequestParser()
parser.add_argument('job', required=True)
parser.add_argument('team_leader', required=True, type=int)
parser.add_argument('work_size', required=True, type=int)
parser.add_argument('collaborators', required=True)
parser.add_argument('is_finished', required=True, type=bool)


def abort_if_jobs_not_found(jobs_id):
    session = db_session.create_session()
    jobs = session.query(Jobs).get(jobs_id)
    if not jobs:
        abort(404, message=f"Jobs {jobs_id} not found")


class JobsResource(Resource):
    def get(self, jobs_id):
        abort_if_jobs_not_found(jobs_id)
        session = db_session.create_session()
        jobs = session.query(Jobs).get(jobs_id)
        return jsonify({'jobs': jobs.to_dict(
            only=('id', 'job', 'team_leader', 'work_size', 'collaborators', 
                  'start_date', 'end_date', 'is_finished'))})

    def delete(self, jobs_id):
        abort_if_jobs_not_found(jobs_id)
        session = db_session.create_session()
        jobs = session.query(Jobs).get(jobs_id)
        session.delete(jobs)
        session.commit()
        return jsonify({'success': 'OK'})
    
    def put(self, jobs_id):
        args = parser.parse_args()
        session = db_session.create_session()
        jobs = session.query(Jobs).get(jobs_id)
        if not jobs:
            abort(404, message=f"Jobs {jobs_id} not found")
        jobs.job = args['job']
        jobs.team_leader = args['team_leader']
        jobs.work_size = args['work_size']
        jobs.collaborators = args['collaborators']
        jobs.is_finished = args['is_finished']
        session.commit()
        return jsonify({'success': 'OK'})


class JobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        jobs = session.query(Jobs).all()
        return jsonify({'jobs':
                            [item.to_dict(only=('id', 'job', 'team_leader', 'work_size', 'collaborators', 
                                                'start_date', 'end_date', 'is_finished')) for item in jobs]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        jobs = Jobs(
            job=args['job'],
            team_leader=args['team_leader'],
            work_size=args['work_size'],
            collaborators=args['collaborators'],
            is_finished=args['is_finished']
        )
        session.add(jobs)
        session.commit()
        return jsonify({'success': 'OK'})