from flask import Blueprint, jsonify, request
from . import db_session
from .users import User

blueprint = Blueprint(
    'users_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users')
def get_users():
    db_sess = db_session.create_session()
    user = db_sess.query(User).all()
    print(user)
    return jsonify(
        {
            'users':
                [item.to_dict(only=('id', 'surname', 'name', 'age', 'position', 
                                    'speciality', 'address', 'email', 'hashed_password',
                                    'modified_date', 'city_from')) for item in user]
        }
    )


@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'users':
                user.to_dict(only=('id', 'surname', 'name', 'age', 'position', 
                                   'speciality', 'address', 'email', 'hashed_password',
                                   'modified_date', 'city_from'))
        }
    )


@blueprint.route('/api/users', methods=['POST'])
def create_user():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'surname', 'name', 'age', 'position', 
                  'speciality', 'address', 'email', 'password', 'city_from']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(request.json['id'])
    if user:
        return jsonify({'error': 'Id already exists'})
    user = User(
        id=request.json["id"],
        surname=request.json['surname'],
        name=request.json['name'],
        age=request.json['age'],
        position=request.json['position'],
        speciality=request.json['speciality'],
        address=request.json['address'],
        email=request.json['email'],
        city_from=request.json['city_from']
    )
    user.set_password(request.json['password'])
    db_sess.add(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    db_sess.delete(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['PUT'])
def put_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not request.json:
        return jsonify({'error': 'Empty request'})
    if not user:
        return jsonify({'error': 'Not found'})
    if 'surname' in request.json:
        user.surname = request.json['surname']
    if 'name' in request.json:
        user.name = request.json['name']
    if 'age' in request.json:
        user.age = request.json['age']
    if 'position' in request.json:
        user.position = request.json['position']
    if 'speciality' in request.json:
        user.speciality = request.json['speciality']
    if 'address' in request.json:
        user.address = request.json['address']
    if 'email' in request.json:
        user.email = request.json['email']
    if 'city_from' in request.json:
        user.city_from = request.json['city_from']
    if 'password' in request.json:
        user.set_password(request.json['password'])
    db_sess.commit()
    return jsonify({'success': 'OK'})