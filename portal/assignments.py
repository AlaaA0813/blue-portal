import psycopg2

from flask import Flask, render_template, flash, Blueprint, g, request, redirect, url_for, abort

from portal import db, login_required
from portal.courses import get_course


bp = Blueprint('assignments', __name__, url_prefix='/assignments')

@bp.route('/<int:id>/create', methods=('GET', 'POST'))
@login_required
def create_assignment(id):
    course = get_course(id)
    user = g.user
    if user[3] == 'teacher':
        if request.method == 'POST':
            assignment_name = request.form['assignment_name']
            assignment_description =  request.form['assignment_description']

            with db.get_db() as con:
                with con.cursor() as cur:
                    cur.execute(
                        'INSERT INTO assignments (assignment_name, assignment_description, course_id)'
                        'VALUES (%s, %s, %s);',
                        (assignment_name, assignment_description, course[0])
                        )

            return redirect(url_for('courses.course', id=course[0]))

        return render_template('assignments/create.html', user=user)

    else:
        abort(401)

@bp.route('/edit/<int:id>', methods=('GET', 'POST'))
@login_required
def edit_assignment(id):
    assignment = get_assignment(id)
    user = g.user
    if user[3] == 'teacher':
        if request.method == 'POST':
            assignment_name = request.form['assignment_name']
            assignment_description =  request.form['assignment_description']

            with db.get_db() as con:
                with con.cursor() as cur:
                    cur.execute("UPDATE assignments SET assignment_name = %s, assignment_description = %s WHERE id = %s", (assignment_name, assignment_description, id,))
                    cur.execute("SELECT course_id FROM assignments WHERE id= %s", (id,))
                    course = cur.fetchone()

            return redirect(url_for('courses.course', id=course[0]))

        return render_template('assignments/edit.html', assignment=assignment, user=user)

    else:
        abort(401)

def get_assignment(id):
    with db.get_db() as con:
        with con.cursor() as cur:
            cur.execute("SELECT * FROM assignments WHERE id = %s", (id,))
            assignment = cur.fetchone()

    if assignment is None:
        abort(404)

    return assignment
