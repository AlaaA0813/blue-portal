import psycopg2

from flask import Flask, render_template, flash, Blueprint, g, request, redirect, url_for, abort

from portal import db
from . import login_required
from portal import courses

bp = Blueprint('sessions', __name__, url_prefix='/sessions')

@bp.route('/<int:id>/create', methods=('GET', 'POST'))
@login_required
def create_session(id):
    course = courses.get_course(id)
    user = g.user

    if user[3] == 'teacher':
        if request.method == 'POST':
            with db.get_db() as con:
                with con.cursor() as cur:
                    cur.execute('SELECT COUNT(*) FROM sessions WHERE course_id = %s', (course[0],))
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
                    con.commit()
                    cur.execute("SELECT * FROM sessions ORDER BY id DESC")
                    session = cur.fetchone()

                    for each in student_list:
                        cur.execute("SELECT * FROM users WHERE email = %s", (each,))
                        student = cur.fetchone()

                        cur.execute(
                            'INSERT INTO user_sessions (student_id, session_id, student_email)'
                            'VALUES (%s, %s, %s)',
                            (student[0], session[0], student[1])
                            )
                        con.commit()

            return redirect(url_for('courses.list_courses'))

        return render_template('sessions/create.html', user=user)

    else:
        abort(401)


@bp.route('/<int:id>/edit', methods=('GET', 'POST'))
@login_required
def edit_session(id):
    session = get_session(id)
    user = g.user
    with db.get_db() as con:
        with con.cursor() as cur:
            cur.execute("SELECT * FROM user_sessions WHERE session_id = %s", (session[0],))
            students_in_session = cur.fetchall()

    if user[3] == 'teacher':
        if request.method == 'POST':
            session_time = request.form['session_time']
            student_list =  request.form.getlist('student_email')

            with db.get_db() as con:
                with con.cursor() as cur:
                    cur.execute("UPDATE sessions SET meets = %s WHERE id = %s", (session_time, session[0],))
                con.commit()

            with db.get_db() as con:
                with con.cursor() as cur:
                    cur.execute("DELETE FROM user_sessions WHERE session_id = %s", (session[0],))
                    con.commit()
                    for each in student_list:
                        cur.execute("SELECT email FROM users WHERE role = 'student'")
                        students = cur.fetchall()
                        for email_tuple in students:
                            if each in email_tuple:
                                cur.execute("SELECT * FROM users WHERE email = %s", (each,))
                                student = cur.fetchone()
                                cur.execute(
                                    'INSERT INTO user_sessions (student_id, session_id, student_email)'
                                    'VALUES (%s, %s, %s);',
                                    (student[0], session[0], student[1])
                                    )
                                con.commit()

            return redirect(url_for('courses.list_courses'))

        return render_template('sessions/edit.html', session=session, students=students_in_session, user=user)

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
