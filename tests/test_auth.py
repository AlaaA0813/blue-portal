import pytest
from flask import g, session
from portal.db import get_db

def test_login(client, auth):
    with client:
        assert client.get('/').status_code == 200
        response = auth.login_student()
        assert response.status_code == 200
        client.get('/')
        assert g.user[1] == "student@stevenscollege.edu"


    with client:
        client.get('/')
        assert session['user_id'] == 2


def test_logout_student(client, auth):
    with client:
        response = auth.login_student()
        assert b'Logout' in response.data
        assert session['user_id'] == 2
        response = auth.logout()
        assert 'user_id' not in session
        assert response.status_code == 302
        assert response.headers['Location'] == 'http://localhost/'

def test_login_wrong_email(client, auth):
    with client:
        assert client.get('/').status_code == 200
        response = auth.login('test@email.com','test')
        assert b'Incorrect email.' in response.data

def test_login_wrong_password(client, auth):
    with client:
        assert client.get('/').status_code == 200
        response = auth.login('student@stevenscollege.edu','stud')
        assert b'Incorrect password.' in response.data
