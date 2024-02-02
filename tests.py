import unittest
from flask import json
from app import app, db, User, Note

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def register_user(self, username, password):
        return self.app.post('/api/register', json={'username': username, 'password': password})

    def login_user(self, username, password):
        return self.app.post('/api/login', json={'username': username, 'password': password})

    def create_note(self, title, content, access_token):
        headers = {'Authorization': f'Bearer {access_token}'}
        return self.app.post('/api/notes', json={'title': title, 'content': content}, headers=headers)

    def test_register_user(self):
        response = self.register_user('testuser', 'testpassword')
        self.assertEqual(response.status_code, 201)

    def test_login_user(self):
        # Register a user
        self.register_user('testuser', 'testpassword')

        # Login with the registered user
        response = self.login_user('testuser', 'testpassword')
        self.assertEqual(response.status_code, 200)

    def test_create_note(self):
        # Register a user and login
        self.register_user('testuser', 'testpassword')
        response = self.login_user('testuser', 'testpassword')
        self.assertEqual(response.status_code, 200)
        access_token = json.loads(response.get_data(as_text=True))['access_token']

        # Create a note with the logged-in user
        response = self.create_note('Test Note', 'This is a test note', access_token)
        self.assertEqual(response.status_code, 201)

    def test_get_notes(self):
        # Register a user and login
        self.register_user('testuser', 'testpassword')
        response = self.login_user('testuser', 'testpassword')
        self.assertEqual(response.status_code, 200)
        access_token = json.loads(response.get_data(as_text=True))['access_token']

        # Create a note with the logged-in user
        self.create_note('Test Note', 'This is a test note', access_token)

        # Retrieve notes with the access token
        headers = {'Authorization': f'Bearer {access_token}'}
        response = self.app.get('/api/notes', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.get_data(as_text=True))), 1)

    def test_get_note(self):
        # Register a user and login
        self.register_user('testuser', 'testpassword')
        response = self.login_user('testuser', 'testpassword')
        self.assertEqual(response.status_code, 200)
        access_token = json.loads(response.get_data(as_text=True))['access_token']

        # Create a note with the logged-in user
        create_response = self.create_note('Test Note', 'This is a test note', access_token)
        note_id = json.loads(create_response.get_data(as_text=True))['message'].split(":")[1].strip()

        # Retrieve the created note with the access token
        headers = {'Authorization': f'Bearer {access_token}'}
        response = self.app.get(f'/api/notes/{note_id}', headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_update_note(self):
        # Register a user and login
        self.register_user('testuser', 'testpassword')
        response = self.login_user('testuser', 'testpassword')
        self.assertEqual(response.status_code, 200)
        access_token = json.loads(response.get_data(as_text=True))['access_token']

        # Create a note with the logged-in user
        create_response = self.create_note('Test Note', 'This is a test note', access_token)
        note_id = json.loads(create_response.get_data(as_text=True))['message'].split(":")[1].strip()

        # Update the created note with the access token
        headers = {'Authorization': f'Bearer {access_token}'}
        update_response = self.app.put(f'/api/notes/{note_id}', json={'title': 'Updated Note', 'content': 'Updated content'}, headers=headers)
        self.assertEqual(update_response.status_code, 200)

    def test_delete_note(self):
        # Register a user and login
        self.register_user('testuser', 'testpassword')
        response = self.login_user('testuser', 'testpassword')
        self.assertEqual(response.status_code, 200)
        access_token = json.loads(response.get_data(as_text=True))['access_token']

        # Create a note with the logged-in user
        create_response = self.create_note('Test Note', 'This is a test note', access_token)
        note_id = json.loads(create_response.get_data(as_text=True))['message'].split(":")[1].strip()

        # Delete the created note with the access token
        headers = {'Authorization': f'Bearer {access_token}'}
        delete_response = self.app.delete(f'/api/notes/{note_id}', headers=headers)
        self.assertEqual(delete_response.status_code, 200)

if __name__ == '__main__':
    unittest.main()