from flask import render_template, jsonify, session
from ghoul import app, db
from ghoul.models import User
from ghoul.route_core import CATEGORIES, calculate_user_stats, get_distance_by_day, login_required

@app.route("/estatisticas")
@login_required
def estatisticas():
    user=db.session.get(User,session["usuario_id"]); stats=calculate_user_stats(user.id)
    return render_template("statistics.html", user=user, stats=stats, categories=CATEGORIES)

@app.route("/api/distance_by_day")
@login_required
def api_distance_by_day(): return jsonify(get_distance_by_day(session["usuario_id"]))

@app.route("/api/activities_by_category")
@login_required
def api_activities_by_category():
    stats=calculate_user_stats(session["usuario_id"])
    return jsonify([{"category":c,"name":CATEGORIES[c]["name"],"count":stats["category_counts"][c],"distance":stats["category_distances"][c],"color":CATEGORIES[c]["color"]} for c in CATEGORIES])

@app.route("/api/distance_by_category")
@login_required
def api_distance_by_category():
    stats=calculate_user_stats(session["usuario_id"])
    return jsonify([{"category":c,"name":CATEGORIES[c]["name"],"distance":stats["category_distances"][c],"color":CATEGORIES[c]["color"]} for c in CATEGORIES])
