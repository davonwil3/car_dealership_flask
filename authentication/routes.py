
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from .forms import LoginForm
from .models import User
from . import db  
from werkzeug.security import check_password_hash  

auth = Blueprint("auth", __name__, template_folder="auth_templates")

@auth.route("/signup", methods=["GET", "POST"])
def signup():
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        print(email, password)

        user = User(email, password=password)

        db.session.add(user)
        db.session.commit()

        flash(f"You have successfully created a user account {email}", "user-created")
        return redirect(url_for("site.home"))
    return render_template("sign_up.html", form=form)

@auth.route("/signin", methods=["GET", "POST"])
def signin():
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        print(email, password)

        logged_user = User.query.filter(User.email == email).first()
        if logged_user and check_password_hash(logged_user.password, password):
            login_user(logged_user)
            flash("You were successfully logged in", "auth-success")
            return redirect(url_for("site.profile"))
        else:
            flash("Your Email/Password is incorrect", "auth-failed")
            return redirect(url_for("auth.signin"))
    return render_template("sign_in.html", form=form)



@auth.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have successfully logged out", "logout-success")
    return redirect(url_for("site.home"))