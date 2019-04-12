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
        print(response.data)
        assert b'Logout' in response.data
        assert session['user_id'] == 2

        response = auth.logout()
        assert 'user_id' not in session
        assert response.status_code == 302
        assert response.headers['Location'] == 'http://localhost/'
