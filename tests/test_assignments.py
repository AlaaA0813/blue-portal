import pytest

from portal.db import get_db
from portal import db
from portal.assignments import get_assignment

from conftest import auth

def test_create_assignment_teacher(client, auth, app):
    #testing get request
    assert client.get('/assignments/1/create').status_code == 302
    auth.login_teacher()
    assert client.get('/assignments/1/create').status_code == 200
    response = client.get('/assignments/1/create')
    assert b'Assignment Name' in response.data
    assert b'Assignment Description' in response.data
    #testing post request
    # assignment.create('test', 'testing')
    client.post('/assignments/1/create', data={'assignment_name': 'test', 'assignment_description': 'testing'})
    with app.app_context():
        con = get_db()
        cur = con.cursor()
        check = cur.execute("SELECT * FROM assignments WHERE assignment_name = 'test'")
        check = cur.fetchone()
        assert check is not None
        cur.close()

def test_create_assignment_student(client, auth):
    assert client.get('/assignments/1/create').status_code == 302
    auth.login_student()
    assert client.get('/assignments/1/create').status_code == 401

def test_edit_assignments(client, auth, app):
    auth.login_teacher()
    # assignment.create('test', 'testing')
    client.post('/assignments/1/create', data={'assignment_name': 'test', 'assignment_description': 'testing'})
    assert client.get('assignments/edit/1').status_code == 200
    client.post('assignments/edit/1', data = {'assignment_name': 'test2', 'assignment_description': 'testing2'})

    with app.app_context():
        con = get_db()
        cur = con.cursor()
        cur.execute("SELECT * FROM assignments WHERE id = 1")
        assignment = cur.fetchone()
        cur.close()

    assert assignment[1] == 'test2'

def test_list_course_assignments_teacher(client, auth):
    auth.login_teacher()
    assert client.get('courses/1/course').status_code == 200
    response = client.get('courses/1/course')
    assert b'Your Assignments' in response.data
