from flask import redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user

from flinterest import app, bcrypt, database
from flinterest.forms import CreateAccountForm, LoginForm
from flinterest.models import Post, User


@app.route("/", methods=["GET", "POST"])
def homepage():
    loginform = LoginForm()
    if loginform.validate_on_submit():
        user = User.query.filter_by(email=loginform.email.data).first()
        if user and bcrypt.check_password_hash(user.password, loginform.password.data):
            login_user(user)
            return redirect(url_for("profile", user_id=user.id))
    return render_template("homepage.html", form=loginform)


@app.route("/create-account", methods=["GET", "POST"])
def createaccount():
    createaccountform = CreateAccountForm()
    if createaccountform.validate_on_submit():
        password = bcrypt.generate_password_hash(createaccountform.password.data)
        user = User(
            username=createaccountform.username.data,
            email=createaccountform.email.data,
            password=password,
        )
        database.session.add(user)
        database.session.commit()
        login_user(user, remember=True)
        return redirect(url_for("profile", user_id=user.id))
    return render_template("createaccount.html", form=createaccountform)


@app.route("/profile/<user_id>")
@login_required
def profile(user_id):
    if int(user_id) == int(current_user.id):
        return render_template("profile.html", user=current_user)
    else:
        user = User.query.get(int(user_id))
        return render_template("profile.html", user=user)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))
