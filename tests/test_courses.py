import pytest

from portal import db
from portal.courses import get_course
from conftest import auth

def test_create_course_teacher(client, auth, app, course):
    #Testing GET request
    assert client.get('/courses/create').status_code == 302
    auth.login_teacher()
    assert client.get('/courses/create').status_code == 200
    response = client.get('/courses/create')
    assert b'Course Number' in response.data
    assert b'Course Title' in response.data
    #Testing POST request
    course.create('test', 'testing')
    with app.app_context():
        with db.get_db() as con:
            with con.cursor() as cur:
                check = cur.execute("SELECT * FROM courses WHERE course_number = 'test'")
                check = cur.fetchone()
        assert check is not None

def test_create_course_student(client, auth):
    assert client.get('/courses/create').status_code == 302
    auth.login_student()
    assert client.get('/courses/create').status_code == 401

def test_list_courses_teacher(client, auth):
    assert client.get('/courses/list').status_code == 302
    auth.login_teacher()
    assert client.get('/courses/list').status_code == 200
    response = client.get('/courses/list')
    assert b'Your Courses' in response.data

def test_list_courses_student(client, auth, course):
    assert client.get('/courses/list').status_code == 302
    auth.login_student()
    assert client.get('/courses/list').status_code == 200
    response = client.get('/courses/list')
    assert b'Your Schedule' in response.data
    assert b'Math A' in response.data

def test_edit_courses(client, course, auth, app):
    auth.login_teacher()
    course.create('test', 'testing')

    assert client.get('courses/1/edit').status_code == 200
    client.post('courses/1/edit', data = {'course_number': 'test2', 'course_title': 'testing2'})

    with app.app_context():
        with db.get_db() as con:
            with con.cursor() as cur:
                cur.execute("SELECT * FROM courses WHERE id = 1")
                course = cur.fetchone()

    assert course[1] == 'test2'


def test_list_course_teacher(client, auth):
    auth.login_teacher()
    assert client.get('courses/1/course').status_code == 200
    response = client.get('courses/1/course')
    assert b'Your Assignments' in response.data

def test_list_course_student(client, auth):
    auth.login_student()
    assert client.get('courses/1/course').status_code == 200
    response = client.get('courses/1/course')
    assert b'<h1>1 Math</h1>' in response.data
