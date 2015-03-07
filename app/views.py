# views.py


from flask import Flask, flash, redirect, render_template, request, \
    session, url_for
from forms import AddDomainForm
from functools import wraps
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')


db = SQLAlchemy(app)

from models import Domain

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap


@app.route('/logout/')
def logout():
    session.pop('logged_in', None)
    flash('You are logged out. Bye. :(')
    return redirect(url_for('login'))


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] \
                or request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid Credentials. Please try again.'
            return render_template('login.html', error=error)
        else:
            session['logged_in'] = True
            return redirect(url_for('tasks'))
    if request.method == 'GET':
        return render_template('login.html')


@app.route('/tasks/')
@login_required
def tasks():
    domain_names = db.session.query(Domain) 
    return render_template(
        'tasks.html',
        form=AddDomainForm(request.form),
        domain_names=domain_names
        )
    
# Add new tasks:
@app.route('/add/', methods=['POST'])
@login_required
def new_task():
    form = AddDomainForm(request.form)
    if request.method == 'POST':
        new_domain = Domain(
            form.name.data,
            )
        db.session.add(new_domain)
        db.session.commit()
        flash("New domain was succesfully posted. Thanks.")
        return redirect(url_for('tasks'))





