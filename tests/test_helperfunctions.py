import unittest
from pathlib import Path
import os 
import censusapi.helperfunctions as hf #relative imports
import pandas as pd
import geopandas as gpd
import censusgeocode as cg
import census

#Test file creation and merging given filepaths
class HelperFunctionTest(unittest.TestCase):
    """Helper Function Testing"""

    key = os.environ.get('secretKey')
    x = -76
    y = 41

    #Returns true if state is matching that of lat/long
    def test_census_lat_long(self):
        getgeoinfo = cg.coordinates(-76, 41)
        censusblock = getgeoinfo['2020 Census Blocks']
        block =censusblock[0] #unwrap the dictionary from the list
        stateID = block['STATE']

        self.assertEqual(stateID, str(42), "The state ID is not (42) Pensilvania. Instead it's:"+str(stateID))

        
    #Makes a dataframe with US census information
    def test_default_columns(self):
        k = census.Census(self.key)
        out = hf.get_census_df(-76, 41, k)
        self.assertTrue({'B19013_001M'}.issubset(out.columns))
        self.assertTrue({'GEOID'}.issubset(out.columns))

    
    # Returns true if the census dataset is created with different census variables
    def test_optional_columns(self):
        variables = ('NAME','B01001_001E')
        print(variables)
        k = census.Census(self.key)
        out = hf.get_census_df(-76, 41, k, variables)
        self.assertTrue({'B01001_001E'}.issubset(out.columns))
        
        


if __name__ == '__main__':
    unittest.main()