from os import path
from secrets import token_hex
from flask import Flask
from definitions import ROOT_PATH
from predict.classifier import StrokeClassifier
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = token_hex(16)

model_path = path.join(ROOT_PATH, "resources/stroke-prediction.joblib")
model_columns_path = path.join(ROOT_PATH, "resources/stroke-prediction-columns.joblib")
app.config['STROKE_CLASSIFIER'] = StrokeClassifier(model_path, model_columns_path)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///stroke.db"
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, "exported_data")
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


from . import routes, models
