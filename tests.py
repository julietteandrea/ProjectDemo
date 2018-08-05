import unittest

from server import app
from model import db, connect_to_db
from authy.api import AuthyApiClient
from aux import sanitize, sanitize_comments
from flask import session

class HomepageTests(unittest.TestCase):
	
	def setUp(self):
		self.client = app.test_client()
		app.config['TESTING'] = True
		# connect_to_db(app)
		# db.create_all()
	
	# def tearDown(self):
		# db.session.close()
		# db.drop_all()

	def test_display_forms(self):
		"""test if login and registrastion form displays on the homepage."""
		result = self.client.get("/")
		self.assertIn(b"Login", result.data)
		self.assertIn(b"register", result.data)

	def test_redirect(self):
		"""test if login redirects to profile page."""
		result = self.client.post("/", data={"username": "juliette", "password": "mynpass"},
									follow_redirects=True)
		self.assertIn(b"Make a call", result.data)

	def test_profile_route(self):
		"""test if profile page displays."""
		result = self.client.get("/")
		self.assertEqual(result.status_code, 200)
		self.assertIn(b"<h3>Call Log</h3>", result.data)

if __name__ == '__main__':
	unittest.main()