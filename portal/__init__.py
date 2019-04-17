import functools
from flask import Flask, render_template, session, request, redirect, url_for, g, flash
from werkzeug.security import check_password_hash, generate_password_hash

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DB_NAME='portal',
        DB_USER='portal_user',
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    from . import courses
    app.register_blueprint(courses.bp)

    from . import db
    db.init_app(app)

    @app.route('/', methods=["GET", "POST"])
    def index():
        user = g.user

        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']

            con = db.get_db()
            error = None

            cur = con.cursor()
            cur.execute(
                'SELECT * FROM users WHERE email = %s', (email,)
            )
            user = cur.fetchone()


            if user is None:
                error = 'Incorrect email.'

            elif not check_password_hash(user[2], password):
                error = 'Incorrect password.'

            if error is None:
                session.clear()
                session['user_id'] = user[0]
                g.user = user

            flash(error)

        return render_template('index.html', user=g.user)


    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('index'))


    @app.before_request
    def load_logged_in_user():
        user_id = session.get('user_id')

        if user_id is None:
            g.user = None
        else:
            con = db.get_db()
            cur = con.cursor()
            cur.execute('SELECT * FROM users WHERE user_id = %s', (user_id,))
            g.user = cur.fetchone()
            cur.close()

    return app

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('index'))

        return view(**kwargs)

    return wrapped_view
