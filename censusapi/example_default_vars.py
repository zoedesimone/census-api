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
key = os.environ.get('secretUser')
#key = "" #or specify allphanumeric key directly


df = gpd.read_file(in_path)
census_variables = ("NAME","B01001_001E")
df = cdf.add_census_to_geojson_df(df, key, census_variables)

for col in df.columns: #print the columns in the augmented dataframe
    print(col)

print(df)

df = hp.rename_columns(df, column_mapping = 
    {'B19013_001E':'MedIncome',
    'B19013_001M':'IncMarErr',
    'B01003_001E':'TotPop',
    'B25003_003E':'RentOcc',
    'B25002_002E':'OwnOcc',
    'B25121_001E':'Income',
    'B25121_002E':"less10k",
    'B25121_017E':'10to20k',
    'B25121_032E':'20to35k',
    'B25121_047E':'35to50k',
    'B25121_062E':'50to75k',
    'B25121_077E':'75to100k',
    'B25121_092E':'more100k'})

df = hp.compute_percentage_from_columns(df, 
    columns_to_sum = ['less10k', '10to20k', '20to35k', '35to50k', '50to75k', '75to100k', 'more100k'])

df = hp.stochastic_column(df, ['less10k_perc', '10to20k_perc', '20to35k_perc', '35to50k_perc', '50to75k_perc', '75to100k_perc', 'more100k_perc'], new_column_name = "stochastic_outp")

for col in df.columns: #print the columns in the augmented dataframe
    print(col)

print(df)
