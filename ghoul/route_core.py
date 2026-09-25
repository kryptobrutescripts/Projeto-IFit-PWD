from functools import wraps
from flask import session, redirect, url_for
from sqlalchemy import func
from ghoul import db
from ghoul.models import User, Activity

CATEGORIES = {
    "walking": {"name": "Caminhada", "color": "#2EAD5B"},
    "cycling": {"name": "Ciclismo", "color": "#1E88E5"},
    "running": {"name": "Corrida", "color": "#E53935"},
    "swimming": {"name": "Natação", "color": "#F4C400"},
    "hiking": {"name": "Trilha", "color": "#E91E63"},
    "rowing": {"name": "Remo", "color": "#8E44AD"},
    "skating": {"name": "Patinação", "color": "#F57C00"},
    "elliptical": {"name": "Elíptico", "color": "#6D4C41"},
}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        usuario_id = session.get("usuario_id")
        usuario = db.session.get(User, usuario_id) if usuario_id else None

        # A sessão pode continuar existindo mesmo depois que o usuário
        # não está mais presente no banco. Nesse caso, força um novo login
        # em vez de deixar as rotas trabalharem com user=None.
        if usuario is None:
            session.clear()
            from flask import flash
            flash("Sua sessão expirou ou o usuário não foi encontrado. Faça login novamente.", "warning")
            return redirect(url_for("login"))

        return f(*args, **kwargs)
    return decorated_function

def get_user_ranking_position(user_id):
    ranking = []
    for user in User.query.all():
        total_distance = sum(a.distance for a in user.activities)
        ranking.append((user.id, total_distance))
    ranking.sort(key=lambda item: item[1], reverse=True)
    for position, (uid, _) in enumerate(ranking, start=1):
        if uid == user_id:
            return "99+" if position > 99 else position
    return None

def calculate_user_stats(user_id):
    activities = Activity.query.filter_by(user_id=user_id).all()
    return {
        "total_distance": round(sum(a.distance for a in activities), 2),
        "total_duration": sum(a.duration for a in activities),
        "total_activities": len(activities),
        "category_counts": {c: sum(1 for a in activities if a.category == c) for c in CATEGORIES},
        "category_distances": {c: round(sum(a.distance for a in activities if a.category == c), 2) for c in CATEGORIES},
    }

def get_distance_by_day(user_id):
    rows = (db.session.query(Activity.date, func.sum(Activity.distance).label("total_distance"))
        .filter(Activity.user_id == user_id).group_by(Activity.date).order_by(Activity.date).all())
    return [{"date": r.date.strftime("%Y-%m-%d"), "distance": float(r.total_distance or 0)} for r in rows]
