import os,re
from uuid import uuid4
from datetime import datetime,timedelta
from flask import render_template,request,redirect,url_for,flash,session
from werkzeug.utils import secure_filename
from ghoul import app,db,bcrypt
from ghoul.models import User
from ghoul.route_core import login_required,calculate_user_stats,get_user_ranking_position

ALLOWED_EXTENSIONS={"png","jpg","jpeg","gif","webp"}
def allowed_file(filename): return "." in filename and filename.rsplit(".",1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/perfil")
@app.route("/profile")
@login_required
def profile():
    user=db.session.get(User,session["usuario_id"]); stats=calculate_user_stats(user.id); position=get_user_ranking_position(user.id)
    now=datetime.now(); changes=user.name_changes_today or 0; can_change_display=changes<2
    return render_template("profile.html",user=user,stats=stats,user_position=position,can_change_display_name=can_change_display,can_change_username=True)

@app.route("/upload_photo",methods=["POST"])
@login_required
def upload_photo():
    user=db.session.get(User,session["usuario_id"]); file=request.files.get("photo")
    if not file or not file.filename or not allowed_file(file.filename): flash("Erro ao atualizar foto","danger"); return redirect(url_for("profile"))
    ext=file.filename.rsplit(".",1)[1].lower(); filename=secure_filename(f"{uuid4().hex}.{ext}"); path=os.path.join(app.config["UPLOAD_FOLDER"],filename); file.save(path)
    if user.photo:
        old=os.path.join(app.config["UPLOAD_FOLDER"],os.path.basename(user.photo))
        if os.path.exists(old):
            try: os.remove(old)
            except OSError: pass
    user.photo=filename; db.session.commit(); flash("Foto atualizada com sucesso!","success"); return redirect(url_for("profile"))

@app.route("/remove_photo",methods=["POST"])
@login_required
def remove_photo():
    user=db.session.get(User,session["usuario_id"])
    if user.photo:
        path=os.path.join(app.config["UPLOAD_FOLDER"],os.path.basename(user.photo))
        if os.path.exists(path): os.remove(path)
        user.photo=""; db.session.commit(); flash("Foto removida com sucesso!","success")
    else: flash("Você não possui uma foto para remover.","warning")
    return redirect(url_for("profile"))

@app.route("/update_profile",methods=["POST"])
@app.route("/atualizar_perfil",methods=["POST"])
@login_required
def update_profile():
    user=db.session.get(User,session["usuario_id"]); display=request.form.get("display_name","").strip(); birth=request.form.get("birth_date",""); gender=request.form.get("gender","")
    if not all([display,birth,gender]): flash("Preencha todos os campos","danger"); return redirect(url_for("profile"))
    try: datetime.strptime(birth,"%Y-%m-%d")
    except ValueError: flash("Data de nascimento inválida.","danger"); return redirect(url_for("profile"))
    today=datetime.now().date(); last=None
    if user.last_name_change:
        try: last=datetime.fromisoformat(user.last_name_change).date()
        except ValueError: pass
    changes=user.name_changes_today or 0
    if last != today: changes=0
    if changes>=2 and display != user.display_name:
        flash("Você só pode mudar o nome de exibição 2 vezes por dia","danger"); return redirect(url_for("profile"))
    if display != user.display_name: changes += 1
    user.display_name=display; user.birth_date=birth; user.gender=gender; user.name_changes_today=changes; user.last_name_change=datetime.now().isoformat(); session["nome_usuario"]=display
    db.session.commit(); flash("Perfil atualizado com sucesso!","success"); return redirect(url_for("profile"))

@app.route("/change_username",methods=["POST"])
@login_required
def change_username():
    user=db.session.get(User,session["usuario_id"]); new=request.form.get("new_username","").lower().strip()
    if not re.match(r"^[a-z0-9_]{3,20}$",new): flash("Nome de usuário inválido","danger"); return redirect(url_for("profile"))
    if new != user.username and User.query.filter(User.username==new,User.id!=user.id).first(): flash("Nome de usuário já está em uso","danger"); return redirect(url_for("profile"))
    last=None
    if user.last_name_change:
        try: last=datetime.fromisoformat(user.last_name_change)
        except ValueError: pass
    if new != user.username and last and datetime.now()-last < timedelta(days=7): flash("Você só pode mudar o nome de usuário uma vez por semana","danger"); return redirect(url_for("profile"))
    user.username=new; user.last_name_change=datetime.now().isoformat(); db.session.commit(); flash("Nome de usuário alterado com sucesso!","success"); return redirect(url_for("profile"))

@app.route("/change_password",methods=["POST"])
@login_required
def change_password():
    user=db.session.get(User,session["usuario_id"]); current=request.form.get("current_password"); new=request.form.get("new_password"); confirm=request.form.get("confirm_password")
    if not all([current,new,confirm]): flash("Preencha todos os campos","danger"); return redirect(url_for("profile"))
    if new!=confirm: flash("As senhas não coincidem","danger"); return redirect(url_for("profile"))
    if len(new)<8: flash("A senha deve ter pelo menos 8 caracteres","danger"); return redirect(url_for("profile"))
    if not bcrypt.check_password_hash(user.password_hash,current): flash("Senha atual incorreta","danger"); return redirect(url_for("profile"))
    if bcrypt.check_password_hash(user.password_hash,new): flash("A nova senha deve ser diferente da senha atual","danger"); return redirect(url_for("profile"))
    user.password_hash=bcrypt.generate_password_hash(new).decode("utf-8"); db.session.commit(); flash("Senha alterada com sucesso!","success"); return redirect(url_for("profile"))
