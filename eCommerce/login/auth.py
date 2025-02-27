from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from app import db
from models import User

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login/login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    
    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password): 
        flash('Incorrect login. Please check your login details and try again.')
        return redirect(url_for('auth.login'))
    
    login_user(user, remember=remember)

    return redirect(url_for('user_profile.profile'))

@auth.route('/signup')
def signup():
    return render_template('login/signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()

    if user:
        flash(str('User ') + str(username) + str(' already exists.'))
        return redirect(url_for('auth.signup'))

    password = request.form.get('password')
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')

    new_user = User(username=username, firstname=firstname, lastname=lastname, credits=125.55, password=generate_password_hash(password, method='sha256'))
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))