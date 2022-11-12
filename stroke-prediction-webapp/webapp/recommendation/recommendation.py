from abc import ABC, abstractmethod
from typing import List
from flask import current_app
from webapp.forms import StrokePredictionForm
from webapp.utils import stroke_prediction_form_to_dict, calculate_bmi


class Recommendation(ABC):
    def __init__(self, form: StrokePredictionForm):
        self.form = form

    @abstractmethod
    def predict_recommendation(self):
        pass

    def _predict(self, key: str, value) -> int:
        health_data = stroke_prediction_form_to_dict(self.form)
        health_data[key] = value
        stroke_classifier = current_app.config["STROKE_CLASSIFIER"]
        return stroke_classifier.predict(health_data=health_data)


class WeightRecommendation(Recommendation):
    steps: int = 5

    def predict_recommendation(self):
        height = int(self.form.height.data)
        weight = int(self.form.weight.data)
        ideal_weight = int(((height - 100) + (30 / 10)) * 0.9)
        if weight + self.steps <= ideal_weight:
            return False, {'weight': weight}

        while weight >= ideal_weight:
            weight = weight - self.steps
            if self._predict("bmi", calculate_bmi(height, weight)) == 0:
                return True, {'weight': weight}

        return False, {'weight': weight}


class AvgGlucoseLevelRecommendation(Recommendation):
    steps: float = 5

    def predict_recommendation(self):
        avg_glucose_level = float(self.form.avg_glucose_level.data)
        if avg_glucose_level + self.steps <= 60:
            return False, {'avg_glucose_level': avg_glucose_level}

        while avg_glucose_level >= 60:
            avg_glucose_level = avg_glucose_level - self.steps
            if self._predict("avg_glucose_level", avg_glucose_level) == 0:
                return True, {'avg_glucose_level': avg_glucose_level}

        return False, {'avg_glucose_level': avg_glucose_level}


class WorkTypeRecommendation(Recommendation):
    work_types = ["Self-employed", "Govt_job", "Private"]

    def predict_recommendation(self):
        work_type = self.form.work_type.data
        if work_type == "children":
            return False, {'work_type': work_type}

        self.work_types.remove(work_type)
        for work_type in self.work_types:
            if self._predict("work_type", work_type) == 0:
                return True, {'work_type': work_type}

        return False, {'work_type': work_type}


class RecommendationProvider:
    def __init__(self, form: StrokePredictionForm):
        self.recommendations: List[Recommendation] = [WeightRecommendation(form), AvgGlucoseLevelRecommendation(form),
                                                      WorkTypeRecommendation(form)]

    def get_recommendations(self):
        recommendation_result = dict()
        for recommendation in self.recommendations:
            prediction, result = recommendation.predict_recommendation()
            recommendation_result.update(result)
            if prediction:
                return True, recommendation_result
        return False, recommendation_result
