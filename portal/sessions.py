import psycopg2

from portal import db

bp = Blueprint('sessions', __name__, url_prefix='/sessions')

@bp.route('<int:id>/create', methods=('GET', 'POST'))
@login_required
def create_session(id):
    course = get_course(id)
    user = g.user

    if user[3] == 'teacher':
        if request.method == 'POST':
            with db.get_db() as con:
                with con.cursor() as cur:
                    cur.execute('SELECT COUNT(*) FROM sessions WHERE course_id = %s', (course[0]))
                    number_of_sessions = cur.fetchone()

            session_letter = str(chr(number_of_sessions + 65))  #A is 65 in ASCII
            session_time = request.form['session_time']
            student_list =  request.form['student_list']

            with db.get_db() as con:
                with con.cursor() as cur:
                    session = cur.execute("SELECT * FROM sessions WHERE letter = session_letter")

            for each in student_list:
                student = cur.execute("SELECT * FROM users WHERE email = each")
                cur.execute(
                    'INSERT INTO user_sessions (student_id, session_id)'
                    'VALUES (%s, %s);',
                    (student[0], session[0])
                    )
                db.commit()

            return redirect(url_for('courses.list_courses'))

        return render_template('sessions/<int:id>/create.html', user=user)

    else:
        abort(401)


@bp.route('/<int:id>/edit', methods=('GET', 'POST'))
@login_required
def edit_session(id):
    session = get_session(id)
    user = g.user

    if user[3] == 'teacher':
        if request.method == 'POST':
            session_time = request.form['session_time']
            student_list =  request.form['student_list']

            with db.get_db() as con:
                with con.cursor() as cur:
                    cur.execute("UPDATE sessions SET meets = %s WHERE id = %s", (session_time, session[0],))
                con.commit()

            with db.get_db() as con:
                with con.cursor() as cur:
                    cur.execute("DELETE FROM user_sessions WHERE session_id = %s", (session[0],))
                    for each in student_list:
                        student = cur.execute("SELECT * FROM users WHERE email = each")
                        cur.execute(
                            'INSERT INTO user_sessions (student_id, session_id)'
                            'VALUES (%s, %s);',
                            (student[0], session[0])
                            )
                        db.commit()

            return redirect(url_for('courses.list_courses'))

        return render_template('sessions/edit.html', session=session, user=user)

    else:
        abort(401)


def get_session(id):
    with db.get_db() as con:
        with con.cursor() as cur:
            cur.execute("SELECT * FROM sessions WHERE id = %s", (id,))
            session = cur.fetchone()

    if sesssion is None:
        abort(404)

    return session
