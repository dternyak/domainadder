# models.py


from views import db


class Domain(db.Model):

    import datetime

    __tablename__ = "domains"
    task_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    posted_date = db.Column(db.Date, default=datetime.datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, name, posted_date, user_id):
        self.name = name
        self.posted_date = posted_date
        self.user_id = user_id

    def __repr__(self):
        return '<name %r>' % (self.name)


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    tasks = db.relationship('Domain', backref='poster')

    def __init__(self, name=None, email=None, password=None):
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.name)
