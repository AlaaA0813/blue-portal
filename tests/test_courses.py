import pytest

from portal.db import get_db

from conftest import auth

def test_create_course(client, app):
    assert client.get('/courses/create').status_code == 401

    auth.login()
    assert client.get('/courses/create').status_code == 200
    response = client.get('/courses/create')
    assert b'Course Number' in response.data
    assert b'Course Title' in response.data

def test_list_courses(client, app):
    assert client.get('/courses/list').status_code == 200
