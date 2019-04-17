import psycopg2

from flask import Flask, render_template, flash, Blueprint, g, request, redirect, url_for, abort

from portal.db import get_db
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

            db = get_db()
            cur = db.cursor()
            cur.execute(
                'INSERT INTO courses (course_number, course_title, instructor_id)'
                'VALUES (%s, %s, %s);',
                (course_number, course_title, user[0])
                )
            cur.close()
            db.commit()
            db.close()

            return redirect(url_for('courses.list_courses'))

        return render_template('courses/create.html', user=user)

    else:
        abort(401)

@bp.route('/list')
@login_required
def list_courses():
    user = g.user

    if user[3] == 'teacher':
        db = get_db()
        cur = db.cursor()
        cur.execute('SELECT * FROM courses WHERE instructor_id = %s', (user[0],))
        list = cur.fetchall()

        cur.close()
        db.close()

        return render_template('courses/list.html', list=list, user=user)

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

            con = get_db()
            cur = con.cursor()
            cur.execute("UPDATE courses SET course_number = %s, course_title = %s WHERE course_id = %s", (course_number, course_title, id,))
            cur.close()
            con.commit()
            con.close()

            return redirect(url_for('courses.list_courses'))

        return render_template('courses/edit.html', course=course, user=user)

    else:
        abort(401)

def get_course(id):
    con = get_db()
    cur = con.cursor()
    cur.execute("SELECT * FROM courses WHERE course_id=%s", (id,))
    course = cur.fetchone()
    cur.close()

    if course is None:
        abort(404)

    return course
