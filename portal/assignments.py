import psycopg2, os

from flask import Flask, current_app, render_template, flash, Blueprint, g, request, redirect, url_for, abort, send_from_directory
from werkzeug.utils import secure_filename

from portal import db, login_required
from portal.courses import get_course
from portal.sessions import get_sessions


ALLOWED_EXTENSIONS = set(['txt', 'rtf', 'odf', 'ods', 'gnumeric', 'abw', 'doc', 'docx', 'xls', 'xlsx', 'jpg', 'jpe', 'jpeg', 'png', 'gif', 'svg', 'bmp', 'csv', 'ini'])


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
                        'VALUES (%s, %s, %s, %s, %s)'
                        'RETURNING id;',
                        (assignment_name, assignment_description, course['id'], type, points))
                    assignment_added = cur.fetchone()[0]
                    course_sessions = get_sessions(id)
                    for session in course_sessions:
                        cur.execute("SELECT student_id FROM user_sessions WHERE session_id = %s", (session['id'],))
                        students = cur.fetchall()
                    for student in students:
                        cur.execute(
                            'INSERT INTO submissions (points_scored, feedback, graded, assignment_id, student_id)'
                            'VALUES (null, null, %s, %s, %s);',
                            (False, assignment_added, student[0]))

            return redirect(url_for('courses.course', id=id))

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
    course = get_course(assignment['course_id'])

    if g.user['role'] == 'teacher':
        with db.get_db() as con:
            with con.cursor() as cur:
                cur.execute("""
                    SELECT s.*,
                           u.name
                    FROM submissions AS s
                    JOIN users AS u ON u.id = s.student_id
                    WHERE s.assignment_id = %s""", (assignment['id'],))
                submissions = cur.fetchall()

        return render_template('assignments/list.html', assignment=assignment, course=course, submissions=submissions)

    elif g.user['role'] == 'student':
        return render_template('assignments/list.html', assignment=assignment, course=assignment['course_id'])

    else:
        abort(401)


@bp.route('/grade/<int:id>/<int:student_id>', methods=('GET', 'POST'))
@login_required
def grade_assignment(id, student_id):
    assignment = get_assignment(id)
    student = get_student(student_id)

    if g.user['role'] == 'teacher':
        if request.method == 'POST':
            points_scored = request.form['points_scored']
            feedback =  request.form['feedback']

            with db.get_db() as con:
                with con.cursor() as cur:
                    cur.execute("""UPDATE submissions
                                   SET points_scored = %s,
                                       feedback = %s,
                                       graded = %s
                                    WHERE student_id = %s AND assignment_id = %s""", (points_scored, feedback, True, student_id, id))

            return redirect(url_for('assignments.assignment', id=id))

        return render_template('assignments/grade.html', assignment=assignment)

    else:
        abort(401)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route('/<int:id>/upload', methods=['GET', 'POST'])
@login_required
def upload_file(id):
    assignment = get_assignment(id)
    if g.user['role'] == 'student':
        if request.method == 'POST':
            file = request.files['file']
            if 'file' not in request.files or file.filename == '':
                return redirect(url_for('assignments.assignment', id=assignment[0]))
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                return render_template('assignments/upload.html', assignment=assignment)
        return render_template('assignments/upload.html', assignment=assignment)


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
