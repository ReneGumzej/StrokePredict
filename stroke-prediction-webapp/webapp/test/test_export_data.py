import unittest
from webapp.dataprocessing.export_data import ExportCSV, ExportJSON, ExportXLS
import pandas as pd

class TestExport(unittest.TestCase):
     
     def test_export_csv(self):
        db_file = ExportCSV("sqlite:///webapp/stroke.db")

        self.assertEqual(db_file.query_data(), pd.DataFrame)



if __name__ == "__main__":
   unittest.main()