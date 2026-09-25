from flask import render_template, request, redirect, url_for, flash, session
from ghoul import app, db
from ghoul.models import User, Group
from ghoul.route_core import login_required, get_user_ranking_position

@app.route("/grupos")
@app.route("/painel_grupos")
@login_required
def painel_grupos():
    user=db.session.get(User, session["usuario_id"])
    user_group_ids={g.id for g in user.groups}
    groups=[g for g in Group.query.all() if g.id not in user_group_ids and g.creator_id != user.id]
    return render_template("groups_panel.html", user=user, groups=groups, recommended_groups=groups)

@app.route("/criar_grupo", methods=["GET","POST"])
@login_required
def criar_grupo():
    user=db.session.get(User, session["usuario_id"])
    if request.method=="POST":
        name=request.form.get("name","").strip(); description=request.form.get("description","").strip()
        if not name:
            flash("Preencha todos os campos", "danger"); return render_template("create_group.html", user=user)
        group=Group(name=name, description=description, creator_id=user.id)
        group.members.append(user); db.session.add(group); db.session.commit()
        flash("Grupo criado com sucesso!", "success"); return redirect(url_for("meus_grupos"))
    return render_template("create_group.html", user=user)

@app.route("/associar_grupo", methods=["GET","POST"])
@login_required
def associar_grupo():
    user=db.session.get(User, session["usuario_id"])
    if request.method=="POST":
        group_id=request.form.get("group_id"); group=db.session.get(Group,int(group_id)) if group_id else None
        if not group: flash("Grupo não encontrado", "danger"); return redirect(url_for("associar_grupo"))
        if group in user.groups: flash("Você já participa deste grupo", "warning"); return redirect(url_for("meus_grupos"))
        group.members.append(user); db.session.commit(); flash("Você entrou no grupo com sucesso!", "success"); return redirect(url_for("meus_grupos"))
    groups=[g for g in Group.query.all() if g not in user.groups]
    return render_template("join_group.html", user=user, groups=groups)

@app.route("/meus_grupos")
@login_required
def meus_grupos():
    user=db.session.get(User, session["usuario_id"])
    return render_template("my_groups.html", user=user, groups=user.groups)

@app.route("/grupo/<int:group_id>/membros")
@login_required
def grupo_membros(group_id):
    user=db.session.get(User, session["usuario_id"]); group=db.session.get(Group,group_id)
    if not group: flash("Grupo não encontrado", "danger"); return redirect(url_for("meus_grupos"))
    if group not in user.groups: flash("Você não tem permissão para ver este grupo", "danger"); return redirect(url_for("meus_grupos"))
    members=[{"user":m,"position":get_user_ranking_position(m.id)} for m in group.members]
    return render_template("group_members.html", user=user, group=group, members_with_position=members)
