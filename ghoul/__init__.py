from datetime import timedelta
from pathlib import Path
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

BASE_DIR = Path(__file__).resolve().parent.parent

app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "templates"),
    static_folder=str(BASE_DIR / "static")
)
app.secret_key = "chave_secreta"
app.permanent_session_lifetime = timedelta(hours=1)
app.config["UPLOAD_FOLDER"] = str(BASE_DIR / "static" / "images" / "user_images")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + str(BASE_DIR / "instance" / "ifit+.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

Path(app.config["UPLOAD_FOLDER"]).mkdir(parents=True, exist_ok=True)
Path(BASE_DIR / "instance").mkdir(parents=True, exist_ok=True)

db = SQLAlchemy()
db.init_app(app)
bcrypt = Bcrypt(app)

from ghoul import models

with app.app_context():
    db.create_all()

@app.context_processor
def inject_user():
    user = None
    user_id = session.get("usuario_id")
    if user_id:
        user = db.session.get(models.User, user_id)
        # Não expõe uma referência inválida caso a conta tenha sido removida.
        if user is None:
            session.pop("usuario_id", None)
            session.pop("usuario", None)
            session.pop("nome_usuario", None)
    return {"user": user}

from ghoul import routes
