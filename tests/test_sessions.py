import pytest

from portal import db
from portal.courses import get_course
from conftest import auth

def test_create_session_teacher(client, auth, app, course):
    #Testing GET request
    assert client.get('/sessions/1/create').status_code == 302
    auth.login_teacher()
    assert client.get('/sessions/1/create').status_code == 200
    response = client.get('/sessions/1/create')
    assert b'Session Time' in response.data
    assert b'Student Email' in response.data
    #Testing POST request
    course.create('test', 'testing')
    client.post('/sessions/1/create', data={'session_time': 'test time', 'student_list': ['student@stevenscollege.edu', 'student2@stevenscollege.edu', 'student3@stevenscollege.edu']})
    with app.app_context():
        with db.get_db() as con:
            with con.cursor() as cur:
                cur.execute("SELECT * FROM sessions WHERE course_id = 1")
                check = cur.fetchone()
        assert check['id'] is 1
        assert check['letter'] is 'A'

def test_create_session_student(client, auth):
    assert client.get('/sessions/1/create').status_code == 302
    auth.login_student()
    assert client.get('/sessions/1/create').status_code == 401

def test_edit_sessions(client, auth):
    auth.login_teacher()
    assert client.get('sessions/1/edit').status_code == 200
    with client:
        client.post('sessions/1/edit', data = {'session_time': 'MTWRF', 'student_email': ['student@stevenscollege.edu', 'student2@stevenscollege.edu', 'student3@stevenscollege.edu', 'student4@stevenscollege.edu']})

        with db.get_db() as con:
            with con.cursor() as cur:
                cur.execute("SELECT * FROM sessions WHERE id = 1")
                session = cur.fetchone()
                assert session['meets'] == 'MTWRF'

                cur.execute("SELECT * FROM user_sessions WHERE session_id = 1")
                students = cur.fetchall()
                print(students)
                assert len(students) == 4
