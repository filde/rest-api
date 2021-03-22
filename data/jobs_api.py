from flask import Blueprint, jsonify, request
from . import db_session
from .jobs import Jobs

blueprint = Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(only=('id', 'job', 'team_leader', 'work_size', 'collaborators', 
                                    'start_date', 'end_date', 'is_finished')) for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_one_job(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'jobs':
                job.to_dict(only=('id', 'job', 'team_leader', 'work_size', 'collaborators', 
                                    'start_date', 'end_date', 'is_finished'))
        }
    )


@blueprint.route('/api/jobs', methods=['POST'])
def create_jobs():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'job', 'team_leader', 'work_size', 'collaborators', 'is_finished']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(request.json['id'])
    if job:
        return jsonify({'error': 'Id already exists'})
    jobs = Jobs(
        id=request.json["id"],
        job=request.json['job'],
        team_leader=request.json['team_leader'],
        work_size=request.json['work_size'],
        collaborators=request.json['collaborators'],
        is_finished=request.json['is_finished']
    )
    db_sess.add(jobs)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['DELETE'])
def delete_jobs(jobs_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(jobs_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    db_sess.delete(jobs)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['PUT'])
def put_jobs(jobs_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(jobs_id)
    if not request.json:
        return jsonify({'error': 'Empty request'})
    if not jobs:
        return jsonify({'error': 'Not found'})
    if 'job' in request.json:
        jobs.job = request.json['job']
    if 'team_leader' in request.json:
        jobs.team_leader = request.json['team_leader']
    if 'work_size' in request.json:
        jobs.work_size = request.json['work_size']
    if 'collaborators' in request.json:
        jobs.collaborators = request.json['collaborators']
    if 'is_finished' in request.json:
        jobs.is_finished = request.json['is_finished']
    db_sess.commit()
    return jsonify({'success': 'OK'})