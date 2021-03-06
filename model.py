"""Models and database functions for project."""

from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()

##############################################################################
# Model definitions


class User(db.Model):
	"""projectdemo users."""

	__tablename__ = "users"

	user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	email = db.Column(db.String(64), nullable=False)
	phone_num = db.Column(db.String(50))
	password = db.Column(db.String(200), nullable=False)
	username = db.Column(db.String(25), nullable=False)


	#define relationship to calls
	calls = db.relationship("Phonecalls", backref="user")


	def __repr__(self):
		"""provide helpful representation when printed."""

		return "<User user_id={} username={} email={} phone_num={} password={}>".format(self.user_id,
																			self.username,
																			self.email,
																			self.phone_num,
																			self.password)
class Phonecalls(db.Model):
	"""user calls."""

	__tablename__ = "calls"	

	record_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
	call_duration = db.Column(db.String(200))
	call_datetime = db.Column(db.String(50), nullable=False)
	call_sid = db.Column(db.String(200), nullable=False)
	recording_url = db.Column(db.String)
	recording_sid = db.Column(db.String(200))
	number_called = db.Column(db.String(50))
	user_comments = db.Column(db.String(60))

	def __repr__(self):
		"""Provide helpful representation when printed."""

		return "<Phonecalls record_id={} user_id={} call_duration={} call_datetime={} call_sid={} recording_url={} recording_sid={} user_comments={}>".format(
																	self.record_id,
																	self.user_id,
																	self.call_duration,
																	self.call_datetime,
																	self.call_sid,
																	self.recording_url,
																	self.recording_sid,
																	self.user_comments)

########################### HELPER FUNCTIONS ######################################

def connect_to_db(app):
	"""Connect the database to our Flask app."""

	#Configure to use our PstgreSQL database
	app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///userinfo'
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	app.config['SQLALCHEMY_ECHO'] = True
	db.app = app
	db.init_app(app)

if __name__ == "__main__":
	#As a convenience, if we run this module interactively, it will leave
	#you in a state of being able to work with the database directly.

	from server import app
	connect_to_db(app)
	print("Connected to DB")