import psycopg2

from flask import Flask, render_template, flash, Blueprint, g, request

from portal.db import get_db
from portal import login_required

bp = Blueprint('courses', __name__, url_prefix='/courses')

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create_course():
    if request.method == 'POST':
        course_number = request.form['course_number']
        course_title =  request.form['course_title']
        error = None
        user = g.user

        if not course_number:
            error = 'Course number is required.'
        elif not course_title:
            error = 'Course title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            cur = db.cursor()
            cur.execute(
                'INSERT INTO courses (course_number, course_title, instructor)'
                'VALUES (%s, %s, %s);',
                (course_number, course_title, user[0])
                )
            cur.close()
            db.commit()
            db.close()

            return render_template('courses/list.html')

    return render_template('courses/create.html')

@bp.route('/list')
@login_required
def list_courses():
    user = g.user[0]
    db = get_db()
    cur = db.cursor()
    cur.execute('SELECT * FROM courses WHERE instructor = %s', (user,))
    list = cur.fetchall()

    cur.close()
    db.close()

    return render_template('courses/list.html', list=list)
