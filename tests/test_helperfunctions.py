import unittest
from pathlib import Path
import os 
import censusapi.helperfunctions as hf #relative imports
import pandas as pd
import geopandas as gpd
import censusgeocode as cg

#Test file creation and merging given filepaths
class HelperFunctionTest(unittest.TestCase):
    """Helper Function Testing"""

    key = os.environ.get('secretUser')
    x = -76
    y = 41


    def test_census_lat_long(self):
        getgeoinfo = cg.coordinates(-76, 41)
        censusblock = getgeoinfo['2020 Census Blocks']
        block =censusblock[0] #unwrap the dictionary from the list
        stateID = block['STATE']

        self.assertEqual(stateID, str(42), "The state ID is not (42) Pensilvania. Instead it's:"+str(stateID))

        
    # #Makes a dataframe with US census information
    # def test_default_columns(self):
    #     out = hf.get_census_df(42, 83, self.key)
    #     expected = pd.DataFrame([1,1,1])
    #     self.assertEqual(out.head(), expected, "Did not pass test_default_columns(")


if __name__ == '__main__':
    unittest.main()