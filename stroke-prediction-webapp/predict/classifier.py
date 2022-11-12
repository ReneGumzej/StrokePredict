import pandas as pd
from joblib import load
from webapp.forms import ButtonForm


class StrokeClassifier:
    def __init__(self, model_path, model_columns_path):
        with open(model_path, "rb") as model_file:
            self.model = load(model_file)
        with open(model_columns_path, "rb") as model_columns_file:
            self.model_columns = load(model_columns_file)

    def predict(self, health_data):
        data_frame = pd.DataFrame.from_dict([health_data])
        dummies = pd.get_dummies(data_frame)
        dummies = dummies.reindex(columns=self.model_columns, fill_value=0)
        return self.model.predict(dummies)[0]
