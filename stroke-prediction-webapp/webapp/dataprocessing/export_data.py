from webapp import db
from flask import send_file, send_from_directory
from abc import ABC, abstractmethod
import pandas as pd 
import os
from flask import current_app

class Download(ABC):
    
    def __init__(self, db_file: str):
        self.db_file = db_file

    @abstractmethod
    def download_data(self):
        pass

    def query_data(self):
        connection = db.create_engine(self.db_file,{})
        query = pd.read_sql_query("SELECT * FROM userinput", connection)
        return query


class ExportCSV(Download):

    def download_data(self,filename: str):
        df = self.query_data()
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        df.to_csv(file_path, index=False)
        downloaded_file = send_file(file_path, as_attachment=True)
        return downloaded_file
    

class ExportJSON(Download):

    def download_data(self, filename: str):
        df = self.query_data()
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        df.to_json(file_path, orient="table" ,index=False)
        downloaded_file = send_file(file_path, as_attachment=True)
        return downloaded_file

    
class ExportXLS(Download):
    
    def download_data(self, filename: str):
        df = self.query_data()
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
            df.to_excel(writer, index=False)
        downloaded_file = send_file(file_path, as_attachment=True)
        return downloaded_file

