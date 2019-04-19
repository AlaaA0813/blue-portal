import psycopg2

from flask import Flask, render_template, flash, Blueprint, g, request, redirect, url_for, abort

from portal import db
from portal import login_required

bp = Blueprint('courses', __name__, url_prefix='/courses')

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create_course():
    user = g.user
    if user[3] == 'teacher':
        if request.method == 'POST':
            course_number = request.form['course_number']
            course_title =  request.form['course_title']

            with db.get_db() as con:
                with con.cursor() as cur:
                    cur.execute(
                        'INSERT INTO courses (course_number, course_title, instructor_id)'
                        'VALUES (%s, %s, %s);',
                        (course_number, course_title, user[0])
                        )
                    con.commit()


            return redirect(url_for('courses.list_courses'))

        return render_template('courses/create.html', user=user)

    else:
        abort(401)

@bp.route('/list')
@login_required
def list_courses():
    user = g.user
    sessions = None

    if user[3] == 'teacher':
        with db.get_db() as con:
            with con.cursor() as cur:
                cur.execute('SELECT * FROM courses WHERE instructor_id = %s', (user[0],))
                courses = cur.fetchall()

        for each in courses:
            with db.get_db() as con:
                with con.cursor() as cur:
                    cur.execute('SELECT * FROM sessions WHERE course_id = %s', (each[0],))
                    sessions = cur.fetchall()

        return render_template('courses/list.html', courses=courses, user=user, sessions=sessions)

    else:
        abort(401)


@bp.route('/<int:id>/edit', methods=('GET', 'POST'))
@login_required
def edit_course(id):
    course = get_course(id)
    user = g.user
    if user[3] == 'teacher':
        if request.method == 'POST':
            course_number = request.form['course_number']
            course_title =  request.form['course_title']

            with db.get_db() as con:
                with con.cursor() as cur:
                    cur.execute("UPDATE courses SET course_number = %s, course_title = %s WHERE id = %s", (course_number, course_title, id,))
                con.commit()

            return redirect(url_for('courses.list_courses'))

        return render_template('courses/edit.html', course=course, user=user)

    else:
        abort(401)

def get_course(id):
    with db.get_db() as con:
        with con.cursor() as cur:
            cur.execute("SELECT * FROM courses WHERE id = %s", (id,))
            course = cur.fetchone()

    if course is None:
        abort(404)

    return course
