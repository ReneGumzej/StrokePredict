from . import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(users):
    return User.query.get(int(users))

class Userinput(db.Model):
    # X-Data
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.String(10), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    hypertension = db.Column(db.String(3), nullable=False)
    heart_disease = db.Column(db.String(3), nullable=False)
    ever_married = db.Column(db.String(3), nullable=False)
    work_type = db.Column(db.String(20), nullable=False)
    residence_type = db.Column(db.String(10), nullable=False)
    avg_glucose_level = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    smoking_status = db.Column(db.String(15), nullable=False)
    #y-Data
    stroke_status = db.Column(db.Integer, nullable=False)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)