from pathlib import Path
import os 


#Example Filepath
THIS_DIR = Path(__file__).parent
my_data_path = THIS_DIR /"data"/"input"/ 'testdata.geojson'
my_output_path = THIS_DIR /"data"/"output"/ 'resultdata.geojson'
key = os.environ.get('secretUser')

import censusapi.censusgdf as cdf

#Example 1: Augmenting shapefile given an input and output filepath
cdf.add_census_to_geojson(my_data_path,my_output_path, key)

#Example 2: Augmenting shapefile given an input and output filepath
cdf.add_census_to_geojson(my_data_path,my_output_path, key)

