# views.py

#################
#### imports ####
#################

from flask import Flask, flash, redirect, render_template, request, \
    session, url_for
from functools import wraps
from flask.ext.sqlalchemy import SQLAlchemy
from forms import AddDomainForm, RegisterForm, LoginForm


################
#### config ####
################

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from models import Domain, User


##########################
#### helper functions ####
##########################

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap


################
#### routes ####
################

@app.route('/logout/')
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    flash('You are logged out. Bye. :(')
    return redirect(url_for('login'))


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            u = User.query.filter_by(
                name=request.form['name'],
                password=request.form['password']
            ).first()
            if u is None:
                error = 'Invalid username or password.'
                return render_template(
                    "login.html",
                    form=form,
                    error=error
                )
            else:
                session['logged_in'] = True
                session['user_id'] = u.id
                flash('You are logged in. Go Crazy.')
                return redirect(url_for('domains'))
        else:
            return render_template(
                "login.html",
                form=form,
                error=error
            )
    if request.method == 'GET':
        return render_template('login.html', form=form)


@app.route('/domains/')
@login_required
def domains():
    domain_names = db.session.query(Domain) 
    return render_template(
        'domains.html',
        form=AddDomainForm(request.form),
        domain_names=domain_names
    )


# Add new domains:
@app.route('/add/', methods=['GET', 'POST'])
@login_required
def new_domain():
    import datetime
    error = None
    form = AddDomainForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_domain = Domain(
                form.name.data,
                datetime.datetime.utcnow(),
                session['user_id']
            )
            db.session.add(new_domain)
            db.session.commit()
            flash('New entry was successfully posted. Thanks.')
            return redirect(url_for('domains'))
        else:
            return render_template('domains.html', form=form, error=error)
    if request.method == 'GET':
        return render_template('domains.html', form=form)


# User Registration:
@app.route('/register/', methods=['GET', 'POST'])
def register():
    error = None
    form = RegisterForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_user = User(
                form.name.data,
                form.email.data,
                form.password.data,
            )
            db.session.add(new_user)
            db.session.commit()
            flash('Thanks for registering. Please login.')
            return redirect(url_for('login'))
        else:
            return render_template('register.html', form=form, error=error)
    if request.method == 'GET':
        return render_template('register.html', form=form)

