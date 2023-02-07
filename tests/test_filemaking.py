import unittest
from pathlib import Path
import os 
import censusapi.censusgdf as cdf #relative imports
import pandas as pd
import geopandas as gpd


#Test file creation and merging given filepaths
class CreatingFileTest(unittest.TestCase):
    """Blackbox testing for censusgdf.py"""

    #Attributes
    THIS_DIR = Path(__file__).parent
    my_data_path = THIS_DIR /"data"/"input"/ 'testdata.geojson'
    my_output_path = THIS_DIR /"data"/"output"/ 'resultdata.geojson'
    key = os.environ.get('secretUser')
    invalid_path = THIS_DIR /"data"/"test"/"input"/ 'testdata.geojson'

    def test(self):
        self.assertTrue(True)

     #Returns true if the out_pth is created
    def test_out_path(self):
        cdf.add_census_to_geojson(self.my_data_path, self.my_output_path, self.key)
        t = os.path.exists(self.my_output_path)
        self.assertTrue(t)

    #Returns true if the out_pth is created
    def test_invalid_path(self):
        cdf.add_census_to_geojson(self.invalid_path, self.my_output_path, self.key)


if __name__ == '__main__':
    unittest.main()