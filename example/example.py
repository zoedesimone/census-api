from pathlib import Path
import os 
import censusapi.censusgdf as cdf
import geopandas as gpd


#Example Filepath
this_dir = os.getcwd()
in_path = this_dir + "/tests/data/input/testdata.geojson"
my_output_path = this_dir + "/tests/data/output/resultdata.geojson"

#Add Secret Key from Census API
key = os.environ.get('secretUser')

#Example 1: Augmenting shapefile given an input and output filepath
cdf.add_census_to_geojson(in_path,my_output_path, key)

#Example 2: Augmenting shapefile given an existing geodataframe
df = gpd.read_file(in_path)
cdf.add_census_to_geojson_df(df, key)

#Example 3: Augmenting shapefile given an existing geodataframe with custom census variables
df = gpd.read_file(in_path)
optional_census_variables = ('NAME','B01001_001E')
cdf.add_census_to_geojson_df(df, key, optional_census_variables)