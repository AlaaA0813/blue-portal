import pytest

from portal.db import get_db
from portal.assignments import get_assignment

from conftest import auth

def test_create_assignment_teacher(client, auth, app, assignment):
    #testing get request
    assert client.get('/assignments/create').status_code == 302
    auth.login_teacher()
    assert client.get('/assignments/create').status_code == 200
    response = client.get('/assignments/create')
    assert b'Assignment Name' in response.data
    assert b'Assignment Description' in response.data
    #testing post request
    assignment.create('test', 'testing')
    with app.app_context():
        con = get_db()
        cur = con.cursor()
        check = cur.execute("SELECT * FROM assignments WHERE assignment_name = 'test'")
        check = cur.fetchone()
        assert check is not None
        cur.close()

def test_create_assignment_student(client, auth):
    assert client.get('/assignments/create').status_code == 302
    auth.login_student()
    assert client.get('/assignments/create').status_code == 401

def test_list_assignments_teacher(client, auth):
    assert client.get('/assignments/list').status_code == 302
    auth.login_teacher()
    assert client.get('/assignments/list').status_code == 200
    response = client.get('/assignments/list')
    assert b'Your Assignments' in response.data

def test_list_assignments_student(client, auth):
    assert client.get('/assignments/list').status_code == 302
    auth.login_student()
    assert client.get('/assignments/list').status_code == 401

def test_edit_assignments(client, assignment, auth, app):
    auth.login_teacher()
    assignment.create('test', 'testing')

    assert client.get('assignments/1/edit').status_code == 200
    client.post('assignments/1/edit', data = {'assignment_name': 'test2', 'assignment_description': 'testing2'})

    with app.app_context():
        con = get_db()
        cur = con.cursor()
        cur.execute("SELECT * FROM assignments WHERE assignment_id = 1")
        assignment = cur.fetchone()
        cur.close()

    assert assignment[1] == 'test2'