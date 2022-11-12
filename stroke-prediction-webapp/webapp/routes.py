
from flask import flash, request, current_app, render_template, redirect, url_for, session, send_file
from . import app, db, bcrypt
from webapp.models import Userinput, User
from webapp.forms import StrokePredictionForm, ButtonForm, LoginForm, ExportDataForm
from webapp.recommendation.recommendation import RecommendationProvider
from webapp.utils import stroke_prediction_form_to_dict
from webapp.dataprocessing.export_data import ExportCSV, ExportJSON, ExportXLS
from flask_login import  login_required, login_user, logout_user, current_user



@app.route('/', methods=['GET', 'POST'])
def handle_predict_request():
    form = StrokePredictionForm(request.form)
    btn_form = ButtonForm(request.form)

    if request.method == 'POST' and form.is_submitted():
        health_data = stroke_prediction_form_to_dict(form)
        stroke_classifier = current_app.config["STROKE_CLASSIFIER"]

        if request.form.get("checkbox") == "True":
                prediction = stroke_classifier.predict(health_data=health_data)
    
                input_data = Userinput(gender=form.gender.data, age=form.age.data, hypertension=form.hypertension.data,
                                    heart_disease=form.heart_disease.data, ever_married=form.ever_married.data, work_type=form.work_type.data,
                                    residence_type=form.residence_type.data, avg_glucose_level=form.avg_glucose_level.data, height=form.height.data,
                                    weight=form.weight.data, smoking_status=form.smoking_status.data,stroke_status=int(prediction))
                db.session.add(input_data)
                db.session.commit()
        else:
            prediction = stroke_classifier.predict(health_data=health_data)
        
        if prediction == 1:
            recommendation_provider = RecommendationProvider(form)
            recommendation_success, recommendations = recommendation_provider.get_recommendations()
            if recommendation_success:
                session['RECOMMENDATIONS'] = recommendations
            
            return redirect(url_for("handle_recommendation_request"))

        else:
            return render_template("predict.html", title="Prediction", form=form, btn_form=btn_form ,output=prediction)

    return render_template("predict.html", title="Prediction", form=form, btn_form=btn_form)

@app.route('/recommend', methods=['GET', 'POST'])
def handle_recommendation_request():
    form = ButtonForm(request.form)
    if form.is_submitted():
        return redirect(url_for('handle_predict_request'))
    if request.method != 'GET':
        return redirect(url_for("handle_predict_request"))
    try:
        recommendations = session['RECOMMENDATIONS']
        return render_template("recommend.html", title="Recommendation", recommendations=recommendations, form=form)
    except KeyError:
        return render_template("recommend.html", title="Recommendation", form=form)

@app.route('/admin', methods=['GET','POST'])
def admin():
    form = ExportDataForm(request.form)
    db_path = "sqlite:///webapp/stroke.db"
    csv_file = ExportCSV(db_path)
    json_file = ExportJSON(db_path)
    xls_file = ExportXLS(db_path)

    if form.is_submitted():
        if form.dataformats.data == 'csv':
            csv_file = csv_file.download_data("Userinput.csv")
            return csv_file
        if form.dataformats.data == 'json':
            json_file = json_file.download_data("Userinput.json")
            return json_file
        if form.dataformats.data == 'xlsx':
            xls_file = xls_file.download_data("Userinput.xlsx")
            return xls_file
       
    return render_template("adminpage.html", title="Adminpage", form=form)


@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('handle_predict_request'))
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first() 
        if user:
            checked_pw = bcrypt.check_password_hash(user.password, form.password.data)
            if checked_pw:
                login_user(user)
                return redirect(url_for('admin'))
        else:
            flash(f'Login was not successful. Please check your email or password', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html', title="Login", form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('handle_predict_request'))


 
    #für Latex: init.py , models.py, form.py, routes.py