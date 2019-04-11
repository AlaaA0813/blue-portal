import pytest
from flask import g, session
from portal.db import get_db

def test_login_student(client, auth):
    assert client.get('/').status_code == 200
    response = auth.login_student()
    assert response.status_code == 200
    assert b"student@stevenscollege.edu" in response.data

    
    with client:
        client.get('/')
        assert session['user_id'] == 2

def test_login_teacher(client, auth):
    assert client.get('/').status_code == 200
    response = auth.login_teacher()
    assert response.status_code == 200
    assert b"teacher@stevenscollege.edu" in response.data


    with client:
        client.get('/')
        assert session['user_id'] == 1
