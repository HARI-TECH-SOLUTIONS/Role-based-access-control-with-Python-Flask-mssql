from flask import Flask, flash, render_template, request, url_for, redirect, session, abort
from logzero import logger
import crud
from db import items
from functools import wraps
from flask import g

app = Flask(__name__)

app.secret_key = 'HARI'


def restricted(access_level):
    def decorator(function):

        @wraps(function)
        def wrapper(*args, **kwargs):
            print(access_level)
            user_id = session.get("UID")

            logger.warning("-----> user_id: {}".format(user_id))

            role = crud.getuserrole(user_id)

            if role:
                if role not in access_level:
                    abort(403)
            else:
                abort(404)

            return function(*args, **kwargs)

        return wrapper

    return decorator


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        get_UID = session.get('UID')
        logger.warning("get_UID: {}".format(get_UID))
        if not get_UID:

            return render_template('login.html')

        return f(*args, **kwargs)
    return decorated_function


@app.route('/', methods=['GET'])
def main():
    return render_template('main.html')


@app.route('/home', methods=['GET', 'POST'])
@login_required
@restricted(['user'])
def home():

    result = crud.getTaskdetails(uid=session.get("UID"))

    if result:
        data = result
    else:
        data = None

    return render_template('home.html', data=data)


@app.route('/admin_home', methods=['GET', 'POST'])
@login_required
@restricted(['admin', 'root'])
def admin_home():

    result = crud.getusers()
    # result = crud.gettasks()

    if result:
        data = result
    else:
        data = None

    return render_template('admin_home.html', users=data)


@app.route('/admin_home_tasks', methods=['GET', 'POST'])
@login_required
@restricted(['admin', 'root'])
def admin_home_tasks():

    # result = crud.getusers()
    result = crud.gettasks()

    if result:
        data = result
    else:
        data = None

    return render_template('tasks.html', tasks=data)


@app.route('/super_admin_home', methods=['GET', 'POST'])
@login_required
@restricted(['root'])
def super_admin_home():

    result = crud.getTaskdetails(uid=session.get("UID"))

    if result:
        data = result
    else:
        data = None

    return render_template('super_admin_home.html', data=data)


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'GET':
        return render_template('login.html')

    else:
        usn = str(request.form.get('email'))
        psw = str(request.form.get('password'))

        logger.info("Username: {} Password: {}".format(usn, psw))

        error = None

        result = crud.checkUser(usn, psw)

        logger.warning("-----> Result: {}".format(result))

        if result:

            if result.role == 'admin':

                flash('You were successfully logged in as Admin')
                # return render_template('admin_home.html')
                return redirect(url_for('admin_home'))

            elif result.role == 'root':

                flash('You were successfully logged in as SUper Admin')
                # return render_template('super_admin_home.html')
                return redirect(url_for('super_admin_home'))

            else:
                flash('You were successfully logged in as user')
                return redirect(url_for('home'))

        else:

            error = 'Invalid credentials'
            return render_template('login.html', error=error)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')

    else:
        fname = str(request.form.get('fname'))
        lname = str(request.form.get('lname'))
        uname = str(request.form.get('uname'))
        email = str(request.form.get('email'))
        password = str(request.form.get('password'))
        role = str(request.form.get('role'))

        logger.info("Fname: {} LName: {} UNamee: {} Email: {} password: {} role : {}".format(
            fname, lname, uname, email, password, role))

        crud.createUser(fname, lname, uname, email, password, role)

        return render_template('login.html')


@app.route('/admin_signup', methods=['GET', 'POST'])
@login_required
@restricted(['root'])
def admin_signup():
    if request.method == 'GET':
        return render_template('admin_signup.html')

    else:
        fname = str(request.form.get('fname'))
        lname = str(request.form.get('lname'))
        uname = str(request.form.get('uname'))
        email = str(request.form.get('email'))
        password = str(request.form.get('password'))

        logger.info("Fname: {} LName: {} UNamee: {} Email: {} password: {}".format(
            fname, lname, uname, email, password))

        crud.createUser(fname, lname, uname, email, password)

        return render_template('admin_login.html')


@app.route('/add', methods=['GET', 'POST'])
@login_required
@restricted(['user'])
def add():
    if request.method == 'GET':
        return render_template('add.html')
    else:
        item = str(request.form.get('item'))
        role = str(request.form.get('role'))

    logger.info("item: {}", "role: {}".format(item, role))

    crud.additem(item, role)

    return redirect('/home')


@app.route('/delete/<todo>/', methods=['POST', 'GET'])
@login_required
@restricted(['user'])
def delete(todo):
    try:
        if request.method == 'GET':

            result = crud.gettaskbyid(uid=session.get('UID'), todo=todo)

            return render_template('delete.html', task=result.item, id=todo)
        else:
            ID = todo
            # item = str(request.form.get('task'))

            logger.info("ID : {}".format(ID))

            result = crud.delitem(ID)
            logger.warning("-----> Result: {}".format(result))

    except Exception as e:
        print(e)

    return redirect(url_for("home"))


@app.route('/deltaskbyadmin/<todo>/', methods=['POST', 'GET'])
@login_required
@restricted(['admin'])
def deltaskbyadmin(todo):
    try:
        if request.method == 'GET':

            result = crud.deltaskbyadmin(uid=session.get('UID'), todo=todo)

            return render_template('delete.html', task=result.item, id=todo)
        else:
            ID = todo
            # item = str(request.form.get('task'))

            logger.info("ID : {}".format(ID))

            result = crud.delitem(ID)
            logger.warning("-----> Result: {}".format(result))

    except Exception as e:
        print(e)

    return redirect(url_for("home"))


@app.route('/update/<todo>', methods=['GET', 'POST'])
@login_required
@restricted(['user'])
def update(todo):
    try:
        if request.method == 'GET':

            result = crud.gettaskbyid(uid=session.get('UID'), todo=todo)

            return render_template("update.html", task=result.item, id=todo)
        else:

            ID = todo

            item = str(request.form.get('task'))

        logger.info("ID : {}".format(ID))
        logger.info("item : {}".format(item))

        result = crud.updateitem(ID, item)
        logger.warning("-----> Result: {}".format(result))

    except Exception as e:
        print(e)

    return redirect(url_for("home"))


@app.route('/updatetaskbyadmin', methods=['GET', 'POST'])
@login_required
@restricted(['admin'])
def updatetaskbyadmin(item):
    try:
        if request.method == 'GET':

            result = crud.gettaskadmin(item=item)

            return render_template("updatetaskbyadmin.html", task=result.item, item=item)
        else:

            item = str(request.form.get('task'))

            logger.info("item : {}".format(item))

            result = crud.updatetaskbyadmin(item)
            logger.warning("-----> Result: {}".format(result))

    except Exception as e:
        print(e)

    return redirect(url_for("admin_home"))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == '__main__':
    app.run(debug=True)
