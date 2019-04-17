import psycopg2
import pytest

from portal.db import get_db, add_user


def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db(), 'get_db should always return the same connection'

    with pytest.raises(psycopg2.InterfaceError) as e:
        cur = db.cursor()
        cur.execute('SELECT 1')

    assert 'closed' in str(e), 'connection should be closed after app context'


def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('portal.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output
    assert Recorder.called


def test_add_user_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_add_user(email, password, role):
        Recorder.called = True

    monkeypatch.setattr('portal.db.add_user', fake_add_user('email', 'password', 'role'))
    result = runner.invoke(args=['add-user'])
    assert 'Begin' in result.output
    assert Recorder.called

def test_add_user(runner, monkeypatch, app):
    with app.app_context():
        con = get_db()
        cur = con.cursor()
        check = cur.execute("SELECT * FROM users WHERE email = 'test'")
        assert check == None
        add_user('test', 'test', 'teacher', 'test')
        check = cur.execute("SELECT * FROM users WHERE email = 'test'")
        check = cur.fetchone()
        assert check is not None
        cur.close()
