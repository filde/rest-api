from flask import Flask, render_template, redirect, request, make_response, jsonify
from data import db_session, jobs_api, users_api, users_resource, jobs_resource
from data.users import User
from data.jobs import Jobs
from data.departments import Department
from data.category import Category
from forms.user import RegisterForm
from forms.login import LoginForm
from forms.job import JobsForm
from forms.department import DepartmentForm
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from requests import get
from flask_restful import reqparse, abort, Api, Resource


app = Flask(__name__)
api = Api(app)
api.add_resource(users_resource.UsersListResource, '/api/v2/users') 
api.add_resource(users_resource.UsersResource, '/api/v2/users/<int:users_id>')
api.add_resource(jobs_resource.JobsListResource, '/api/v2/jobs') 
api.add_resource(jobs_resource.JobsResource, '/api/v2/jobs/<int:jobs_id>')
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
db_sess = ''


def main():
    global db_sess
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()
    app.register_blueprint(jobs_api.blueprint)
    app.register_blueprint(users_api.blueprint)
    #add_users(db_sess)
    #add_jobs(db_sess)
    app.run()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def add_users(db_sess):
    cap = User(surname="Scott", name="Ridley", age=21, 
               position="captain", speciality="research engineer",
               address="module_1", email="scott_chief@mars.org", city_from='Москва')
    cap.set_password('cap')
    db_sess.add(cap)

    user1 = User(surname="Faber", name="Harry", age=28, 
               position="colonist", speciality="rover driver",
               address="module_1", email="farber_chief@mars.org", city_from='Санкт-Петербург')
    user1.set_password('user1')
    db_sess.add(user1)

    user2 = User(surname="Charlson", name="Oliver", age=25, 
               position="colonist", speciality="climatologist",
               address="module_2", email="charlson_chief@mars.org", city_from='Смоленск')
    user2.set_password('user2')
    db_sess.add(user2)

    user3 = User(surname="Brooks", name="Charlie", age=30, 
               position="colonist", speciality="meteorologist",
               address="module_2", email="brooks_chief@mars.org", city_from='Рязань')
    user3.set_password('user3')
    db_sess.add(user3)

    db_sess.commit()


def add_jobs(db_sess):
    job = Jobs(team_leader=1, job="deployment of residential modules 1 and 2",
               work_size=15, collaborators="2, 3", is_finished=False)
    db_sess.add(job)
    db_sess.commit()


@app.route("/")
def index():
    global db_sess
    jobs = db_sess.query(Jobs).all()
    leaders = []
    category = []
    for i in jobs:
        leaders.append(i.user.surname + ' ' + i.user.name)
        category.append(', '.join([str(j.id) for j in i.categories]))
    return render_template("works_log.html", jobs=jobs, leaders=leaders, category=category,
                           title="Работы")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    global db_sess
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        if form.age.data.isdigit():
            age = int(form.age.data)
        else:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Возраст - натуральное число")
        user = User(
            email=form.email.data,
            name=form.name.data,
            surname=form.surname.data,
            age=age,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@login_manager.user_loader
def load_user(user_id):
    global db_sess
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    global db_sess
    form = LoginForm()
    if form.validate_on_submit():
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', title="Авторизация",
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/jobs',  methods=['GET', 'POST'])
@login_required
def new_job():
    global db_sess
    form = JobsForm()
    if form.validate_on_submit():
        jobs = Jobs()
        print(1)
        try:
            work_size = int(form.work_size.data)
        except Exception:
            return render_template('add_job.html', title='Добавление работы', 
                                    form=form, message="Время работы - целое неотрицательное количество часов")
        try:
            category = list(map(int, form.hazard.data.split(', ')))
            print(1)
            cat = db_sess.query(Category).filter(Category.id.in_(category))
            print(2)
            for i in cat:
                jobs.categories.append(i)
        except Exception:
            return render_template('add_job.html', title='Добавление работы', 
                                    form=form, message="С категориями что-то не так")
        jobs.work_size = work_size
        jobs.job = form.title.data
        jobs.collaborators = form.collaborators.data
        jobs.is_finished = form.is_finished.data
        current_user.jobs.append(jobs)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('add_job.html', title='Добавление работы', 
                           form=form)


@app.route('/jobs/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_jobs(id):
    global db_sess
    form = JobsForm()
    if request.method == "GET":
        jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                          ((Jobs.user == current_user) | (current_user.id == 1)),
                                          ).first()
        if jobs:
            form.title.data = jobs.job
            form.work_size.data = str(jobs.work_size)
            form.collaborators.data = jobs.collaborators
            form.hazard.data = ', '.join([str(i.id) for i in jobs.categories])
            form.is_finished.data = jobs.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                          ((Jobs.user == current_user) | (current_user.id == 1)),
                                          ).first()
        if jobs:
            try:
                work_size = int(form.work_size.data)
            except Exception:
                return render_template('add_job.html', title='Редактирование работы', 
                                        form=form, message="Время работы - целое неотрицательное количество часов")
            
            try:
                sp = jobs.categories
                sp1 = [i for i in jobs.categories]
                for i in sp1:
                    jobs.categories.remove(i)
                category = list(map(int, form.hazard.data.split(', ')))
                cat = db_sess.query(Category).filter(Category.id.in_(category))
                for i in cat:
                    jobs.categories.append(i)
            except Exception:
                jobs.categories = sp
                return render_template('add_job.html', title='Добавление работы', 
                                        form=form, message="С категориями что-то не так")
            jobs.job = form.title.data
            jobs.work_size = work_size
            jobs.collaborators = form.collaborators.data
            jobs.is_finished = form.is_finished.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('add_job.html',
                           title='Редактирование работы',
                           form=form)


@app.route('/jobs_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def jobs_delete(id):
    global db_sess
    jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                          ((Jobs.user == current_user) | (current_user.id == 1)),
                                          ).first()
    if jobs:
        db_sess.delete(jobs)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route("/departments")
def department():
    global db_sess
    departments = db_sess.query(Department).all()
    leaders = []
    for i in departments:
        leaders.append(i.user.surname + ' ' + i.user.name)
    return render_template("departments.html", deps=departments, leaders=leaders, 
                            title="Департаменты")


@app.route('/department_new',  methods=['GET', 'POST'])
@login_required
def new_department():
    global db_sess
    form = DepartmentForm()
    if form.validate_on_submit():
        department = Department()
        department.title = form.title.data
        department.members = form.members.data
        department.email = form.email.data
        current_user.departments.append(department)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/departments')
    return render_template('add_department.html', title='Добавление департамента', 
                           form=form)


@app.route('/departments/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    global db_sess
    form = DepartmentForm()
    if request.method == "GET":
        dep = db_sess.query(Department).filter(Department.id == id,
                                               ((Department.user == current_user) | (current_user.id == 1)),
                                               ).first()
        if dep:
            form.title.data = dep.title
            form.members.data = dep.members
            form.email.data = dep.email
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        dep = db_sess.query(Department).filter(Department.id == id,
                                               ((Department.user == current_user) | (current_user.id == 1)),
                                               ).first()
        if dep:
            dep.title = form.title.data
            dep.members = form.members.data
            dep.email = form.email.data
            db_sess.commit()
            return redirect('/departments')
        else:
            abort(404)
    return render_template('add_department.html',
                           title='Редактирование департамента',
                           form=form)


@app.route('/departments_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def department_delete(id):
    global db_sess
    dep = db_sess.query(Department).filter(Department.id == id,
                                            ((Department.user == current_user) | (current_user.id == 1)),
                                            ).first()
    if dep:
        db_sess.delete(dep)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/departments')


@app.route('/users_show/<int:user_id>')
def users_show(user_id):
    user = get(f'http://localhost:5000/api/users/{user_id}').json()['users']
    map_request = "http://static-maps.yandex.ru/1.x/"
    geo_request = "http://geocode-maps.yandex.ru/1.x/"
    map_params = {'l': 'sat',
                  'z': '13'}
    geo_params = {'apikey': '40d1649f-0493-4b70-98ba-98533de7710b',
                  'format': 'json',
                  'geocode': user['city_from']}
    response = get(geo_request, params=geo_params)
    if not response:
        return render_template('users_show.html',
                                title='Hometown',
                                user=user, file = '')
    response = response.json()
    last_response = response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
    map_params['ll'] = last_response['Point']['pos'].replace(' ', ',')
    response = get(map_request, params=map_params)
    if not response:
        return render_template('users_show.html',
                                title='Hometown',
                                user=user, file = '')
    name = 'static/img/' + str(user_id) + '.png'
    with open(name, "wb") as file:
        file.write(response.content)
    return render_template('users_show.html',
                           title='Hometown',
                           user=user, file=str(user_id) + '.png')


if __name__ == '__main__':
    main()