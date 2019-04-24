import psycopg2

from flask import Flask, render_template, flash, Blueprint, g, request, redirect, url_for, abort

from portal.db import get_db
from portal import login_required


bp = Blueprint('assignments', __name__, url_prefix='/assignments')

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create_assignment():
    user = g.user
    if user[3] == 'teacher':
        if request.method == 'POST':
            assignment_name = request.form['assignment_name']
            assignment_description =  request.form['assignment_description']

            db = get_db()
            cur = db.cursor()
            cur.execute(
                'INSERT INTO assignments (assignment_name, assignment_description)'
                'VALUES (%s, %s);',
                (assignment_name, assignment_description)
                )
            cur.close()
            db.commit()
            db.close()

            return redirect(url_for('assignments.list_assignments'))

        return render_template('assignments/create.html', user=user)

    else:
        abort(401) # TODO: Fix this later

@bp.route('/list')
@login_required
def list_assignments():
    user = g.user

    if user[3] == 'teacher':
        db = get_db()
        cur = db.cursor()
        cur.execute('SELECT * FROM assignments')
        list = cur.fetchall()

        cur.execute('SELECT course_title FROM courses AT course_id = course.id')
        course = cur.fetchone()

        cur.close()
        db.close()

        return render_template('courses/course.html', list=list, user=user, course=course)

    else:
        abort(401) # TODO: Fix this later

@bp.route('/<int:id>/edit', methods=('GET', 'POST'))
@login_required
def edit_assignment(id):
    assignment = get_assignment(id)
    user = g.user
    if user[3] == 'teacher':
        if request.method == 'POST':
            assignment_name = request.form['assignment_name']
            assignment_description =  request.form['assignment_description']

            con = get_db()
            cur = con.cursor()
            cur.execute("UPDATE assignments SET assignment_name = %s, assignment_description = %s WHERE id = %s", (assignment_name, assignment_description, id,))
            cur.close()
            con.commit()
            con.close()

            return redirect(url_for('assignments.list_assignments'))

        return render_template('assignments/edit.html', assignment=assignment, user=user)

    else:
        abort(401) # TODO: Fix this later

def get_assignment(id):
    con = get_db()
    cur = con.cursor()
    cur.execute("SELECT * FROM assignments WHERE id = %s", (id,))
    assignment = cur.fetchone()
    cur.close()

    if assignment is None:
        abort(404) # TODO: Fix this later

    return assignment
