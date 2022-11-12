from email.policy import default
from wtforms import SubmitField, SelectField, IntegerField, BooleanField, StringField, PasswordField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, NumberRange, Email



class StrokePredictionForm(FlaskForm):
    GENDER_CHOICE = [("", ""), ("Male", "Male"), ("Female", "Female")]
    YESNO_CHOICE = [("", ""), (1, "Yes"), (0, "No")]
    WORK_TYPE_CHOICE = [("", ""), ("Self-employed", "Self employed"), ("Govt_job", "Goverment job"),
                        ("Never_worked", "Never worked"), ("Private", "Private"), ("children", "Children")]
    RESIDENCE_CHOICE = [("", ""), ("Urban", "Urban"), ("Rural", "Rural")]
    SMOKING_CHOICE = [("", ""), ("smokes", "Smoke"), ("never smoked", "Never smoked")]

    gender = SelectField("Gender", choices=GENDER_CHOICE, validators=[DataRequired()])
    age = IntegerField("Age", validators=[DataRequired()])
    hypertension = SelectField("Hypertension", choices=YESNO_CHOICE, validators=[DataRequired()])
    heart_disease = SelectField("Heart disease", choices=YESNO_CHOICE, validators=[DataRequired()])
    ever_married = SelectField("Ever married", choices=YESNO_CHOICE, validators=[DataRequired()])
    work_type = SelectField("Work type", choices=WORK_TYPE_CHOICE, validators=[DataRequired()])
    residence_type = SelectField("Residence type", choices=RESIDENCE_CHOICE, validators=[DataRequired()])
    avg_glucose_level = IntegerField("Glucose level", validators=[DataRequired(), NumberRange(30, 380)])
    height = IntegerField("Height (cm)", validators=[DataRequired()])
    weight = IntegerField("Weight (kg)", validators=[DataRequired()])
    smoking_status = SelectField("Smoking status", choices=SMOKING_CHOICE, validators=[DataRequired()])
    stroke_status = IntegerField("Stroke status")
    submit = SubmitField('Predict')
    #checkbox = BooleanField('store your data?', validators=[DataRequired()],)


class ButtonForm(FlaskForm):
    redirect_button = SubmitField('New Prediciton')
    checkbox = BooleanField('store data ?')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ExportDataForm(FlaskForm):
    DATA_CHOICE = [("", ""), ("csv", "CSV"), ("json", "JSON"),("xlsx", "XLSX")]

    dataformats = SelectField("Data formats", choices=DATA_CHOICE, validators=[DataRequired()])
    export_csv_button = SubmitField('Export')