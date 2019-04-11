import psycopg2

from flask import Flask, render_template, flash

from portal.db import get_db

bp = Blueprint('courses', __name__, url_prefix='/courses')

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create_course(id):
    if request.method == 'POST':
        course = request.form['course']
        title =  request.form['title']
        meets =  request.form['meets']
        error = None

        if not course:
            error = 'Course abbreviation is required.'
        elif not title:
            error = 'Course title is required.'
        elif not meets:
            error = 'Course meet schedule is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            cur = db.cursor()
            cur.execute(
                'INSERT INTO courses (course, title, meets)'
                'VALUES (%s, %s, %s);',
                (course, title, meets)
                )
            cur.close()
            db.commit()

            return redirect(url_for('courses.list'))

    return render_template('courses/create.html')

@bp.route('/list', methods=('GET'))
@login_required
def list_courses(user_id):
    db = get_db()
    cur = db.cursor()
    cur.execute('SELECT * FROM courses WHERE instructor = user_id;')
    list = cur.fetchall()
    cur.close()

    return render_template('courses/list.html', list=list)
