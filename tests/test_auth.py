import json


class TestLogin:
    def test_login_success(self, client, user1):
        resp = client.post('/PaySphereAPI/login', json={
            'num': 10001,
            'password': 'TestPass123!@',
        })
        assert resp.status_code == 200
        data = resp.get_json()
        assert 'access_token' in data
        assert 'refresh_token' in data

    def test_login_wrong_password(self, client, user1):
        resp = client.post('/PaySphereAPI/login', json={
            'num': 10001,
            'password': 'WrongPassword1!',
        })
        assert resp.status_code == 401

    def test_login_nonexistent_client(self, client, seed_refs):
        resp = client.post('/PaySphereAPI/login', json={
            'num': 99999,
            'password': 'TestPass123!@',
        })
        assert resp.status_code == 401

    def test_login_missing_fields(self, client, seed_refs):
        resp = client.post('/PaySphereAPI/login', json={})
        assert resp.status_code == 400

    def test_login_invalid_num_type(self, client, seed_refs):
        resp = client.post('/PaySphereAPI/login', json={
            'num': 'abc',
            'password': 'TestPass123!@',
        })
        assert resp.status_code == 400


class TestRegister:
    def test_register_success(self, client, seed_refs):
        resp = client.post('/PaySphereAPI/register', json={
            'id': 100,
            'nom': 'Nouveau',
            'prenom': 'User',
            'email': 'nouveau@test.com',
            'username': 'newuser',
            'password': 'NewUserPass1!@',
        })
        assert resp.status_code == 201

    def test_register_weak_password(self, client, seed_refs):
        resp = client.post('/PaySphereAPI/register', json={
            'username': 'newuser',
            'password': 'weak',
        })
        assert resp.status_code == 400

    def test_register_duplicate_username(self, client, user1):
        resp = client.post('/PaySphereAPI/register', json={
            'username': 'jdupont',
            'password': 'AnotherPass1!@',
        })
        assert resp.status_code == 400

    def test_register_missing_fields(self, client, seed_refs):
        resp = client.post('/PaySphereAPI/register', json={
            'username': 'onlyuser',
        })
        assert resp.status_code == 400


class TestLogout:
    def test_logout_success(self, client, user1, auth_headers):
        resp = client.post('/PaySphereAPI/logout', headers=auth_headers)
        assert resp.status_code == 200
        data = resp.get_json()
        assert 'Déconnexion' in data['message']

    def test_logout_no_token(self, client, seed_refs):
        resp = client.post('/PaySphereAPI/logout')
        assert resp.status_code == 401


class TestRefresh:
    def test_refresh_token(self, client, user1):
        login_resp = client.post('/PaySphereAPI/login', json={
            'num': 10001,
            'password': 'TestPass123!@',
        })
        refresh_token = login_resp.get_json()['refresh_token']

        resp = client.post('/PaySphereAPI/refresh', headers={
            'Authorization': f'Bearer {refresh_token}',
            'Content-Type': 'application/json',
        })
        assert resp.status_code == 200
        assert 'access_token' in resp.get_json()
