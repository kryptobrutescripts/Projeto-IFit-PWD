from datetime import datetime
from ghoul import db

group_members = db.Table(
    "group_members",
    db.Column("user_id", db.Integer, db.ForeignKey("usuarios.id"), primary_key=True),
    db.Column("group_id", db.Integer, db.ForeignKey("grupos.id"), primary_key=True),
)

class User(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    display_name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.String(20))
    gender = db.Column(db.String(50))
    photo = db.Column(db.String(255))
    password_hash = db.Column(db.String(255), nullable=False)
    register_date = db.Column(db.String(30))
    last_name_change = db.Column(db.String(30))
    name_changes_today = db.Column(db.Integer, default=0)
    groups = db.relationship("Group", secondary=group_members, back_populates="members")
    activities = db.relationship("Activity", back_populates="user", lazy=True, cascade="all, delete-orphan")

class Activity(db.Model):
    __tablename__ = "atividades"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    distance = db.Column(db.Float, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship("User", back_populates="activities")

class Group(db.Model):
    __tablename__ = "grupos"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    creator_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    members = db.relationship("User", secondary=group_members, back_populates="groups")
    creator = db.relationship("User", foreign_keys=[creator_id])
