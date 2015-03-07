from views import db

class Domain(db.Model):

	__tablename__ = "domains"
	task_id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False)

	def __init__(self, name):
		self.name = name


	def __repr__(self):
		return '<name %r>' % (self.name)