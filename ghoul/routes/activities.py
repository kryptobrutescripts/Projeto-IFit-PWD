from datetime import datetime
from flask import render_template, request, redirect, url_for, flash, session
from ghoul import app, db
from ghoul.models import User, Activity
from ghoul.route_core import CATEGORIES, login_required

@app.route("/atividades")
@login_required
def listar_atividades():
    user = db.session.get(User, session["usuario_id"])
    activities = Activity.query.filter_by(user_id=user.id).order_by(Activity.date.desc()).all()
    return render_template("index.html", user=user, activities=activities, categories=CATEGORIES)

@app.route("/cadastro_atividade")
@login_required
def cadastro_atividade():
    user = db.session.get(User, session["usuario_id"])
    return render_template("cadastro_atividade.html", user=user, CATEGORIES=CATEGORIES, categories=CATEGORIES, activity=None, id=0, datetime=datetime)

@app.route("/add_activity", methods=["POST"])
@login_required
def add_activity():
    category = request.form.get("category")
    date = request.form.get("date")
    distance = request.form.get("distance")
    duration = request.form.get("duration")
    if category not in CATEGORIES or not all([date, distance, duration]):
        flash("Preencha todos os campos.", "danger")
        return redirect(url_for("home"))
    try:
        distance = float(distance.replace(",", "."))
        duration = int(duration)
        activity_date = datetime.strptime(date, "%Y-%m-%d")
        if distance <= 0 or duration <= 0: raise ValueError
    except (ValueError, TypeError):
        flash("Distância ou duração inválida", "danger")
        return redirect(url_for("home"))
    db.session.add(Activity(category=category, date=activity_date, distance=distance, duration=duration, user_id=session["usuario_id"]))
    db.session.commit()
    flash("Atividade adicionada com sucesso!", "success")
    return redirect(url_for("home"))

@app.route("/editar/<int:activity_id>")
@login_required
def edit_activity(activity_id):
    activity = Activity.query.filter_by(id=activity_id, user_id=session["usuario_id"]).first()
    if not activity:
        flash("Atividade não encontrada", "danger")
        return redirect(url_for("home"))
    user = db.session.get(User, session["usuario_id"])
    return render_template("edit_activity.html", user=user, activity=activity, categories=CATEGORIES)

@app.route("/update_activity/<int:activity_id>", methods=["POST"])
@login_required
def update_activity(activity_id):
    activity = Activity.query.filter_by(id=activity_id, user_id=session["usuario_id"]).first()
    if not activity:
        flash("Atividade não encontrada", "danger")
        return redirect(url_for("home"))
    category, date, distance, duration = (request.form.get(x) for x in ("category", "date", "distance", "duration"))
    if category not in CATEGORIES or not all([date, distance, duration]):
        flash("Preencha todos os campos.", "danger")
        return redirect(url_for("edit_activity", activity_id=activity_id))
    try:
        distance=float(distance.replace(",", ".")); duration=int(duration); activity_date=datetime.strptime(date, "%Y-%m-%d")
        if distance<=0 or duration<=0: raise ValueError
    except (ValueError, TypeError):
        flash("Distância ou duração inválida", "danger")
        return redirect(url_for("edit_activity", activity_id=activity_id))
    activity.category=category; activity.date=activity_date; activity.distance=distance; activity.duration=duration
    db.session.commit()
    flash("Atividade atualizada com sucesso!", "success")
    return redirect(url_for("home"))

@app.route("/delete_activity/<int:activity_id>", methods=["POST"])
@login_required
def delete_activity(activity_id):
    activity = Activity.query.filter_by(id=activity_id, user_id=session["usuario_id"]).first()
    if not activity:
        flash("Atividade não encontrada", "danger")
        return redirect(url_for("home"))
    db.session.delete(activity); db.session.commit()
    flash("Atividade excluída com sucesso!", "success")
    return redirect(url_for("home"))
