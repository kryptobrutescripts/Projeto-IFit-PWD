from flask import render_template, session
from sqlalchemy import func

from ghoul import app, db
from ghoul.models import User, Activity
from ghoul.route_core import CATEGORIES, login_required


# Progressão por quantidade de atividades realizadas em cada modalidade.
# Os requisitos são o total acumulado necessário para alcançar cada divisão.
RANKS = [
    {"name": "Recruta", "slug": "recruta", "color": "#8E9AA8", "requirements": [1, 2, 3, 4, 5]},
    {"name": "Veterano", "slug": "veterano", "color": "#18A66A", "requirements": [6, 7, 8, 9, 10]},
    {"name": "Elite", "slug": "elite", "color": "#2389E8", "requirements": [12, 14, 16, 18, 20]},
    {"name": "Pro", "slug": "pro", "color": "#8B4DFF", "requirements": [23, 26, 29, 32, 35]},
    {"name": "Mestre", "slug": "mestre", "color": "#D98A18", "requirements": [38, 41, 44, 47, 50]},
]

DIVISIONS = ["I", "II", "III", "IV", "V"]
LEGENDARY_REQUIREMENT = 55

# Para receber a insígnia especial que aparece no filtro "Todas",
# o usuário precisa alcançar pelo menos Mestre I em TODAS as modalidades.
MASTER_MINIMUM = RANKS[4]["requirements"][0]
MASTER_ALL_BADGE = "mestre_todas.png"


def get_rank_for_total(total):
    """Retorna a patente/divisão mais alta já alcançada pelo total informado."""
    total = max(0, int(total or 0))

    # Ainda não realizou nenhuma atividade.
    if total < 1:
        return {
            "rank": "Sem patente",
            "rank_slug": None,
            "division": None,
            "division_number": None,
            "requirement": 0,
            "next": "Recruta I",
            "next_requirement": 1,
            "remaining": 1,
            "progress": 0,
            "color": "#8E9AA8",
            "badge": None,
        }

    # Lendário é a patente final.
    if total >= LEGENDARY_REQUIREMENT:
        return {
            "rank": "Lendário",
            "rank_slug": "lendario",
            "division": None,
            "division_number": None,
            "requirement": LEGENDARY_REQUIREMENT,
            "next": None,
            "next_requirement": None,
            "remaining": 0,
            "progress": 100,
            "color": "#E33A3A",
            "badge": "lendario.png",
        }

    # Procura TODAS as divisões e guarda a última que já foi alcançada.
    # Isso evita o erro anterior em que 6 atividades continuavam aparecendo
    # como Recruta I porque a função retornava na primeira correspondência.
    current_rank = None
    current_division_index = None
    current_requirement = None
    current_rank_index = None

    for rank_index, rank in enumerate(RANKS):
        for division_index, requirement in enumerate(rank["requirements"]):
            if total >= requirement:
                current_rank = rank
                current_rank_index = rank_index
                current_division_index = division_index
                current_requirement = requirement

    if current_rank is None:
        # Segurança; na prática total >= 1 já deveria ter encontrado Recruta I.
        return get_rank_for_total(0)

    # Próxima divisão dentro da mesma patente.
    if current_division_index < 4:
        next_requirement = current_rank["requirements"][current_division_index + 1]
        next_label = f"{current_rank['name']} {DIVISIONS[current_division_index + 1]}"
    else:
        # A divisão V é o fim da patente atual.
        # Se já estamos em Mestre V, a próxima etapa é Lendário,
        # evitando acessar uma posição inexistente em RANKS.
        if current_rank_index + 1 < len(RANKS):
            next_rank = RANKS[current_rank_index + 1]
            next_requirement = next_rank["requirements"][0]
            next_label = f"{next_rank['name']} I"
        else:
            next_requirement = LEGENDARY_REQUIREMENT
            next_label = "Lendário"

    gap = max(1, next_requirement - current_requirement)
    progress = int(max(0, min(100, ((total - current_requirement) / gap) * 100)))

    return {
        "rank": current_rank["name"],
        "rank_slug": current_rank["slug"],
        "division": DIVISIONS[current_division_index],
        "division_number": current_division_index + 1,
        "requirement": current_requirement,
        "next": next_label,
        "next_requirement": next_requirement,
        "remaining": max(0, next_requirement - total),
        "progress": progress,
        "color": current_rank["color"],
        "badge": f"{current_rank['slug']}{current_division_index + 1}.png",
    }


def get_category_totals(user):
    """Conta as atividades do usuário por modalidade."""
    return {
        category: sum(1 for activity in user.activities if activity.category == category)
        for category in CATEGORIES
    }


def has_mastery_in_all_categories(user):
    """True quando o usuário alcançou pelo menos Mestre I em todas as modalidades."""
    totals = get_category_totals(user)
    return all(total >= MASTER_MINIMUM for total in totals.values())


def get_rank_badge_for_user(user, category):
    """
    Retorna a insígnia que deve aparecer no ranking.

    - Em uma categoria específica: patente atual naquela categoria.
    - Em "Todas": somente a insígnia especial de Mestre em todas as modalidades.
    """
    if category == "todas":
        if not has_mastery_in_all_categories(user):
            return None

        return {
            "badge": MASTER_ALL_BADGE,
            "rank": "Mestre em todas as modalidades",
            "rank_slug": "mestre_todas",
            "division": None,
            "color": "#D4A72C",
        }

    total = sum(1 for activity in user.activities if activity.category == category)
    rank = get_rank_for_total(total)

    if not rank["badge"]:
        return None

    return {
        "badge": rank["badge"],
        "rank": (
            f"{rank['rank']} {rank['division']}"
            if rank["division"]
            else rank["rank"]
        ),
        "rank_slug": rank["rank_slug"],
        "division": rank["division"],
        "color": rank["color"],
    }


@app.route("/conquistas")
@login_required
def conquistas():
    usuario_id = session.get("usuario_id")
    usuario_atual = db.session.get(User, usuario_id)

    resultados = (
        db.session.query(
            Activity.category,
            func.count(Activity.id).label("total"),
        )
        .filter(Activity.user_id == usuario_id)
        .group_by(Activity.category)
        .all()
    )
    contagens = {resultado.category: int(resultado.total) for resultado in resultados}

    conquistas_por_categoria = []

    # Mostra todas as modalidades, inclusive as que ainda têm zero atividades.
    for categoria, categoria_info in CATEGORIES.items():
        total = contagens.get(categoria, 0)
        patente = get_rank_for_total(total)

        conquistas_por_categoria.append(
            {
                "categoria": categoria,
                "nome_categoria": categoria_info["name"],
                "cor": categoria_info["color"],
                "total": total,
                **patente,
            }
        )

    conquistas_por_categoria.sort(key=lambda item: item["nome_categoria"].lower())

    return render_template(
        "conquistas.html",
        usuario=usuario_atual,
        user=usuario_atual,
        conquistas=conquistas_por_categoria,
        categories=CATEGORIES,
        ranks=RANKS,
        legendary_requirement=LEGENDARY_REQUIREMENT,
    )
