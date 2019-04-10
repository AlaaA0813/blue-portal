import pytest
from flask import g, session
from portal.db import get_db

def test_login(client, auth):
    assert client.get('/').status_code == 200
    response = auth.login()
    #assert response.headers['Location'] == 'http://localhost/'

    with client:
        client.get('/')

        #assert session['user_id'] == user[0]
        #assert session['user_email'] = user[1]

        #assert session['id'] == 0

        #assert g.user['username'] == 'test'
