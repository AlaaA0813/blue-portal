from flask import Flask, render_template, session, request, redirect, url_for
from werkzeug.security import check_password_hash

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

    from . import db
    db.init_app(app)

    @app.route('/', methods=["GET", "POST"])
    def index():
        user_email = None

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

            elif user[2] != password:
                error = 'Incorrect password.'

            if error is None:
                session.clear()
                session['user_id'] = user[0]
                session['user_email'] = user[1]


        return render_template('index.html', user_email=session.get('user_email'))

    @app.route('/logout', methods=["GET"])
    def logout():
        session.clear()
        return redirect(url_for('index'))

    return app
