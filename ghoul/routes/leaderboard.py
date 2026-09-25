from flask import render_template, request, session

from ghoul import app, db
from ghoul.models import User
from ghoul.route_core import CATEGORIES, login_required, get_user_ranking_position
from ghoul.routes.achievements import get_rank_badge_for_user


@app.route("/quadro_lideres")
@login_required
def quadro_lideres():
    category = request.args.get("categoria", "todas")

    if category not in CATEGORIES and category != "todas":
        category = "todas"

    ranking = []

    for user in User.query.all():
        activities = (
            user.activities
            if category == "todas"
            else [activity for activity in user.activities if activity.category == category]
        )

        if not activities:
            continue

        entry = {
            "user": user,
            "total_distance": round(sum(activity.distance for activity in activities), 2),
            "total_duration": sum(activity.duration for activity in activities),
            "total_activities": len(activities),
            # No filtro de categoria, mostra a patente daquela modalidade.
            # Em "Todas", só aparece a insígnia especial quando o usuário
            # é Mestre I ou superior em todas as modalidades.
            "rank_badge": get_rank_badge_for_user(user, category),
        }

        ranking.append(entry)

    ranking.sort(key=lambda item: item["total_distance"], reverse=True)

    for position, entry in enumerate(ranking, 1):
        entry["position"] = "99+" if position > 99 else position

    user = db.session.get(User, session["usuario_id"])

    # Mantém os dados do próprio usuário disponíveis caso ele esteja fora do top 99.
    current_entry = next(
        (entry for entry in ranking if entry["user"].id == user.id),
        None,
    )

    return render_template(
        "leaderboard.html",
        user=user,
        ranking=ranking,
        categories=CATEGORIES,
        CATEGORIES=CATEGORIES,
        filter=category,
        user_position=get_user_ranking_position(user.id),
        current_entry=current_entry,
    )
