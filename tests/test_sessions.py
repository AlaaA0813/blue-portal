import pytest

from portal import db
from portal.courses import get_course
from conftest import auth

def test_create_session_teacher(client, auth, app, course):
    #Testing GET request
    assert client.get('/sessions/create').status_code == 302
    auth.login_teacher()
    assert client.get('/sessions/create').status_code == 200
    response = client.get('/sessions/create')
    assert b'Session Time' in response.data
    assert b'Student Email' in response.data
    #Testing POST request
    course.create('test', 'testing')
    client.post('/sessions/1/create', data={'session_time': 'test time', 'student_list': ['test@email.com', 'test2@email.com', 'test3@email.com']})
    with app.app_context():
        with db.get_db() as con:
            with con.cursor() as cur:
                cur.execute("SELECT * FROM sessions WHERE course_id = 1")
                check = cur.fetchone()
        assert check is 1
        assert check[1] is 'A'

def test_create_session_student(client, auth):
    assert client.get('/sessions/create').status_code == 302
    auth.login_student()
    assert client.get('/sessions/create').status_code == 401

def test_edit_sessions(client, course, auth, app):
    auth.login_teacher()
    course.create('test', 'testing')
    client.post('/sessions/1/create', data={'session_time': 'test time', 'student_list': ['test@email.com', 'test2@email.com', 'test3@email.com']})

    assert client.get('sessions/1/edit').status_code == 200
    client.post('sessions/1/edit', data = {'session_time': 'test time2', 'student_list': ['test2@email.com', 'test3@email.com', 'test4@email.com', 'test5@email.com']})

    with app.app_context():
        with db.get_db() as con:
            with con.cursor() as cur:
                cur.execute("SELECT * FROM sessions WHERE id = 1")
                session = cur.fetchone()

        assert session[3] == 'test time2'

        with db.get_db() as con:
            with con.cursor() as cur:
                cur.execute("SELECT * FROM user_sessions WHERE session_id = 1")
                students = cur.fetchall()
        assert len(students) == 4
