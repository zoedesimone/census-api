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

#Do once
df = gpd.read_file(in_path)
df = cdf.add_census_to_geojson_df(df, key)


for i in range(0,10) :

    res = hp.stochastic_ownership_income(df, n_trials =1)
    print(res)

    for col in res.columns: #print the columns in the augmented dataframe
        print(col)

    gpd.GeoDataFrame.to_file(res, my_output_path, driver='GeoJSON')


