import pytest

from portal.db import get_db

def test_create_course(client, auth):
    assert client.get('/courses/create').statuscode == 401

    auth.login()
    assert client.get('/courses/create').statuscode == 200
    response = client.get('/courses/create')
    assert b'Course' in response.data
    assert b'Meets' in response.data
