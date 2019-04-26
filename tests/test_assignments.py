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
    client.post('/assignments/1/create', data={'assignment_name': 'test', 'assignment_description': 'testing'})
    with app.app_context():
        with db.get_db() as con:
            with con.cursor() as cur:
                check = cur.execute("SELECT * FROM assignments WHERE assignment_name = 'test'")
                check = cur.fetchone()
        assert check is not None

def test_create_assignment_student(client, auth):
    assert client.get('/assignments/1/create').status_code == 302
    auth.login_student()
    assert client.get('/assignments/1/create').status_code == 401

def test_edit_assignment_teacher(client, auth, app):
    auth.login_teacher()
    assert client.get('assignments/edit/1').status_code == 200
    client.post('assignments/edit/1', data = {'assignment_name': 'test2', 'assignment_description': 'testing2'})

    with app.app_context():
        with db.get_db() as con:
            with con.cursor() as cur:
                cur.execute("SELECT * FROM assignments WHERE id = 1")
                assignment = cur.fetchone()

    assert assignment[1] == 'test2'

def test_edit_assignment_student(client, auth):
    auth.login_student()
    assert client.get('assignments/edit/1').status_code == 401

def test_show_assignment_student(client, auth):
    auth.login_student()
    assert client.get('assignments/1/assignment').status_code == 200
    response = client.get('assignments/1/assignment')
    assert b'<h2>Math Homework</h2>' in response.data

def test_show_assignment_teacher(client, auth):
    auth.login_teacher()
    assert client.get('assignments/1/assignment').status_code == 401

def test_get_assignment(client, auth):
    auth.login_student()
    assert client.get('assignments/9/assignment').status_code == 404
