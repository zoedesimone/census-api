from pathlib import Path
import os 
import geopandas as gpd
import censusgdf as cdf
import helperfunctions as hp

#Example Filepath
this_dir = os.getcwd()
in_path = this_dir + "/tests/data/input/testdata.geojson"
my_output_path = this_dir + "/tests/data/output/resultdata.geojson"

#Add Secret Key from Census API
#key = os.environ.get('secretUser')
key = ""
print("CENSUS KEY:", key)

#Below are different of augmenting a shapefile with census information. Uncomment your preferred method to test.

#Method 1: given an input and output filepath
#cdf.add_census_to_geojson(in_path,my_output_path, key)


#Method 2:  given an existing geodataframe

df = gpd.read_file(in_path)
df = cdf.add_census_to_geojson_df(df, key)

for col in df.columns: #print the columns in the augmented dataframe
    print(col)

print(df)

#Method 3: given an existing geodataframe AND custom census variables
"""
df = gpd.read_file(in_path)
census_variables = ("NAME","B01001_001E")
df = cdf.add_census_to_geojson_df(df, key, census_variables)

for col in df.columns: #print the columns in the augmented dataframe
    print(col)
"""
