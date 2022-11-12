from webapp.forms import StrokePredictionForm


def stroke_prediction_form_to_dict(form: StrokePredictionForm) -> dict:
    return {
        "age": form.age.data,
        "hypertension": int(form.hypertension.data),
        "heart_disease": int(form.heart_disease.data),
        "avg_glucose_level": float(form.avg_glucose_level.data),
        "bmi": calculate_bmi(form.height.data, form.weight.data),
        "ever_married": int(form.ever_married.data),
        "Residence_type": form.residence_type.data,
        "gender": form.gender.data,
        "work_type": form.work_type.data,
        "smoking_status": form.smoking_status.data
    }


def calculate_bmi(height, weight) -> float:
    height_m = int(height) / 100
    return int(weight) / (height_m ** 2)
