import psycopg2

from flask import Flask, render_template, flash, Blueprint, g, request, redirect, url_for, abort

from portal import db, login_required
from portal.courses import get_course


bp = Blueprint('assignments', __name__, url_prefix='/assignments')

@bp.route('/<int:id>/create', methods=('GET', 'POST'))
@login_required
def create_assignment(id):
    course = get_course(id)
    if g.user['role'] == 'teacher':
        if request.method == 'POST':
            assignment_name = request.form['assignment_name']
            assignment_description =  request.form['assignment_description']
            type = request.form['type']
            points = request.form['total_points']

            with db.get_db() as con:
                with con.cursor() as cur:
                    cur.execute(
                        'INSERT INTO assignments (assignment_name, assignment_description, course_id, type, total_points)'
                        'VALUES (%s, %s, %s, %s, %s);',
                        (assignment_name, assignment_description, course['id'], type, points)
                        )

            return redirect(url_for('courses.course', id=course[0]))

        return render_template('assignments/create.html')

    else:
        abort(401)

@bp.route('/edit/<int:id>', methods=('GET', 'POST'))
@login_required
def edit_assignment(id):
    assignment = get_assignment(id)
    if g.user['role'] == 'teacher':
        if request.method == 'POST':
            assignment_name = request.form['assignment_name']
            assignment_description =  request.form['assignment_description']
            points = request.form['total_points']

            with db.get_db() as con:
                with con.cursor() as cur:
                    cur.execute("UPDATE assignments SET assignment_name = %s, assignment_description = %s, total_points = %s WHERE id = %s", (assignment_name, assignment_description, points, id,))
                    cur.execute("SELECT course_id FROM assignments WHERE id= %s", (id,))
                    course = cur.fetchone()

            return redirect(url_for('courses.course', id=course[0]))

        return render_template('assignments/edit.html', assignment=assignment)

    else:
        abort(401)

@bp.route('/<int:id>')
@login_required
def assignment(id):
    assignment = get_assignment(id)

    if g.user['role'] == 'teacher':
        with db.get_db() as con:
            with con.cursor() as cur:
                cur.execute('SELECT * FROM user_sessions WHERE course_id = %s', (assignment['course_id'],))
                students = cur.fetchall()
                cur.execute('SELECT student_id FROM submissions WHERE assignment_id = %s', (assignment['id'],))
                submissions = cur.fetchall()

        return render_template('assignments/list.html', assignment=assignment, students=students, course=assignment['course_id'], submissions=submissions)

    elif g.user['role'] == 'student':
        return render_template('assignments/list.html', assignment=assignment, course=assignment['course_id'])

    else:
        abort(401)

@bp.route('/grade/<int:id>/<int:student_id>', methods=('GET', 'POST'))
@login_required
def grade_assignment(id, student_id):
    assignment = get_assignment(id)
    student = get_student(student_id)

    if request.method == 'POST':
        if g.user['role'] == 'teacher':
            points_scored = request.form['points_scored']
            feedback =  request.form['feedback']

            with db.get_db() as con:
                with con.cursor() as cur:
                    cur.execute(
                                'INSERT INTO submissions(points_scored, feedback)'
                                'VALUES (%s, %s);',
                                (points_scored, feedback,)
                                )

            return redirect(url_for('assignments/<int:id>', id=id))

        else:
            abort(401)

    return render_template('assignments/grade.html')


def get_assignment(id):
    with db.get_db() as con:
        with con.cursor() as cur:
            cur.execute("SELECT * FROM assignments WHERE id = %s", (id,))
            assignment = cur.fetchone()

    if assignment is None:
        abort(404)

    return assignment

def get_student(id):
    with db.get_db() as con:
        with con.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE id = %s", (id,))
            student = cur.fetchone()

    if student is None:
        abort(404)

    return student
