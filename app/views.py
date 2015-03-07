# views.py


from flask import Flask, flash, redirect, render_template, request, \
    session, url_for
from forms import AddDomainForm, RegisterForm, LoginForm
from functools import wraps
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')


db = SQLAlchemy(app)

from models import Domain, User

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

@app.route("/register/", methods=['GET', 'POST'])
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
            flash("Thanks for registering. Please Login.")
            return redirect(url_for('login'))
        else: 
            return render_template('register.html', form=form, error=error)
    if request.method == 'GET':
        return render_template("register.html", form=form)

@app.route('/logout/')
def logout():
    session.pop('logged_in', None)
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
                error = "Invalid username or password"
                return render_template("login.html",
                    form=form,
                    error=error)
            else: 
                session['logged_in'] = True
                flash("You are logged in.")
                return redirect(url_for("tasks"))
        else: 
            return render_template(
                "login.html",
                form=form,
                error=error)
    if request.method == "GET":
        return render_template("login.html", form=form)
        
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





