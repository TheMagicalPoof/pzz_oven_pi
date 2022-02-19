from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for("schedule.main"))
    else:
        return signin()

@auth.route('/signin')
def signin():
    return render_template("login.html")

@auth.route('/signup', methods=["POST"])
def signup_post():
    login = request.form.get("login")
    password = request.form.get("password")
    user = User.query.filter_by(login=login).first()
    if user:
        return redirect(url_for("auth.signin"))

    new_user = User(login=login, password=generate_password_hash(password, method="sha256"), admin=False)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for("auth.login"))

@auth.route("/login", methods=['POST'])
def login_post():
    login = request.form.get("username")
    password = request.form.get("password")
    remember = True if request.form.get('remember') else False
    user = User.query.filter_by(login=login).first()

    if not user or not check_password_hash(user.password, password):
        flash('Неверные данные авторизации')
        return signin()
    login_user(user, remember=remember)
    return redirect(url_for("schedule.main"))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return signin()
