import psycopg2

from flask import Flask, render_template, flash, Blueprint, g, request, redirect, url_for, abort

from portal import db, courses
from . import login_required

bp = Blueprint('sessions', __name__, url_prefix='/sessions')

@bp.route('/<int:id>/create', methods=('GET', 'POST'))
@login_required
def create_session(id):
    course = courses.get_course(id)
    if g.user['role'] == 'teacher':
        if request.method == 'POST':
            with db.get_db() as con:
                with con.cursor() as cur:
                    cur.execute('SELECT COUNT(*) FROM sessions WHERE course_id = %s', (course['id'],))
                    number_of_sessions = cur.fetchone()
                    number_of_sessions = int(number_of_sessions[0])

            session_letter = str(chr(number_of_sessions + 65))  #A is 65 in ASCII
            session_time = request.form['session_time']
            student_list =  request.form.getlist('student_email')

            with db.get_db() as con:
                with con.cursor() as cur:
                    cur.execute(
                        'INSERT INTO sessions (letter, course_id, meets)'
                        'VALUES (%s, %s, %s)',
                        (session_letter, id, session_time,)
                        )
                    cur.execute("SELECT * FROM sessions ORDER BY id DESC")
                    session = cur.fetchone()

                    for each in student_list:
                        cur.execute("SELECT * FROM users WHERE email = %s", (each,))
                        student = cur.fetchone()

                        cur.execute(
                            'INSERT INTO user_sessions (student_id, session_id)'
                            'VALUES (%s, %s)',
                            (student['id'], session['id'])
                            )
                    cur.execute("SELECT course_id FROM sessions WHERE id= %s", (id,))
                    course = cur.fetchone()

                    return redirect(url_for('courses.course', id=id))

        return render_template('sessions/create.html')

    else:
        abort(401)


@bp.route('/<int:id>/edit', methods=('GET', 'POST'))
@login_required
def edit_session(id):
    session = get_session(id)

    with db.get_db() as con:
        with con.cursor() as cur:
            cur.execute("""
                        SELECT us.*,
                               u.email
                        FROM user_sessions AS us
                        JOIN users AS u ON us.student_id = u.id
                        WHERE session_id = %s""", (session['id'],))
            students_in_session = cur.fetchall()
            cur.execute("SELECT * FROM assignments WHERE course_id = %s", (session['course_id'],))
            assignments = cur.fetchall()

    if g.user['role'] == 'teacher':
        if request.method == 'POST':
            session_time = request.form['session_time']
            student_list =  request.form.getlist('student_email')
            user_students = []

            with db.get_db() as con:
                with con.cursor() as cur:
                    cur.execute("UPDATE sessions SET meets = %s WHERE id = %s", (session_time, session['id'],))
                    cur.execute("DELETE FROM user_sessions WHERE session_id = %s", (session['id'],))
                    cur.execute("SELECT email FROM users WHERE role = 'student'")
                    students = cur.fetchall()
                    for tuple in students:
                        for each in tuple:
                            user_students.append(each)
                    for each in student_list:
                        if each in user_students:
                            cur.execute("SELECT * FROM users WHERE email = %s", (each,))
                            student = cur.fetchone()
                            cur.execute(
                                'INSERT INTO user_sessions (student_id, session_id)'
                                'VALUES (%s, %s)',
                                (student['id'], session['id'],)
                                )
                    cur.execute("SELECT course_id FROM sessions WHERE id= %s", (id,))
                    course = cur.fetchone()

            return redirect(url_for('courses.course', id=course[0]))

        return render_template('sessions/edit.html', session=session, students=students_in_session, assignments=assignments)

    else:
        abort(401)


def get_session(id):
    with db.get_db() as con:
        with con.cursor() as cur:
            cur.execute("SELECT * FROM sessions WHERE id = %s", (id,))
            session = cur.fetchone()

    if session is None:
        abort(404)

    return session

def get_sessions(id):
    with db.get_db() as con:
        with con.cursor() as cur:
            cur.execute("SELECT * FROM sessions WHERE course_id = %s", (id,))
            sessions = cur.fetchall()

    if sessions is None:
        abort(404)

    return sessions
