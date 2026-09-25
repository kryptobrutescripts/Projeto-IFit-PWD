import re
from datetime import datetime
from flask import render_template, request, redirect, url_for, flash, session
from ghoul import app, db, bcrypt
from ghoul.models import User, Activity
from ghoul.route_core import CATEGORIES, calculate_user_stats, login_required

@app.route("/")
def index():
    if session.get("usuario_id"):
        return redirect(url_for("home"))
    return redirect(url_for("login"))

@app.route("/dashboard")
@login_required
def home():
    user = db.session.get(User, session["usuario_id"])
    activities = Activity.query.filter_by(user_id=user.id).order_by(Activity.date.desc()).all()
    stats = calculate_user_stats(user.id)
    return render_template("dashboard.html", user=user, activities=activities, stats=stats, categories=CATEGORIES, datetime=datetime)

@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("usuario_id"):
        return redirect(url_for("home"))
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password_hash, password):
            session.permanent = True
            session["usuario_id"] = user.id
            session["usuario"] = user.email
            session["nome_usuario"] = user.display_name
            flash(f"Login realizado com sucesso! Bem-vindo(a), {user.display_name}.", "success")
            return redirect(url_for("home"))
        flash("E-mail ou senha inválidos", "danger")
    return render_template("login.html")

@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    flash("Você foi desconectado!", "warning")
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("usuario_id"):
        return redirect(url_for("home"))
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        username = request.form.get("username", "").lower().strip()
        display_name = request.form.get("display_name", "").strip()
        birth_date = request.form.get("birth_date", "")
        gender = request.form.get("gender", "")
        password = request.form.get("password", "")
        if not all([email, username, display_name, birth_date, gender, password]):
            flash("Preencha todos os campos", "danger")
            return render_template("register.html")
        if not re.match(r"^[a-z0-9_]{3,20}$", username):
            flash("Nome de usuário inválido", "danger")
            return render_template("register.html")
        if len(password) < 8:
            flash("A senha deve ter pelo menos 8 caracteres", "danger")
            return render_template("register.html")
        if User.query.filter_by(email=email).first():
            flash("Email já cadastrado", "danger")
            return render_template("register.html")
        if User.query.filter_by(username=username).first():
            flash("Nome de usuário já está em uso", "danger")
            return render_template("register.html")
        try:
            datetime.strptime(birth_date, "%Y-%m-%d")
        except ValueError:
            flash("Data de nascimento inválida.", "danger")
            return render_template("register.html")
        now = datetime.now()
        user = User(email=email, username=username, display_name=display_name,
                    birth_date=birth_date, gender=gender, photo="",
                    password_hash=bcrypt.generate_password_hash(password).decode("utf-8"),
                    register_date=now.strftime("%Y-%m-%d %H:%M:%S"),
                    last_name_change=now.isoformat(), name_changes_today=0)
        db.session.add(user)
        db.session.commit()
        flash("Cadastro realizado com sucesso! Faça o login.", "success")
        return redirect(url_for("login"))
    return render_template("register.html")
