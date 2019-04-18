import psycopg2

bp = Blueprint('sessions', __name__, url_prefix='/sessions')

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create_session(id):
    course = get_course(id)
    user = g.user
    if user[3] == 'teacher':
        if request.method == 'POST':

            db = get_db()
            cur = db.cursor()
            cur.execute('SELECT COUNT(*) FROM sessions WHERE course_id = %s', (course[0]))
            number_of_sessions = cur.fetchone()


            session_letter = str(chr(number_of_sessions + 65))
            #A is 65 in ASCII

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
