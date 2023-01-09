"""
Title: Add Census Data to Geodataframe

Description: This file allows you to output an augmented geojson file
containing census information at the US census tract block level 
given a geojson file.

Requirement: City's geojson file

Author: Zoe De Simone, Github: @zoedesimone
"""


#from IPython.display import display
import HelperFunctions as cdf
import geopandas as gpd
import os


def AddCensustoGeojsonFile(file: str, key: str):
    """
    Returns a geojson file "GeojsonWithCensus.geojson" with additional columns 
    containing Census Tract Level Data regarding building tract level ownership, population and income.
    Variable Legend:
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
    'B25121_092E':'more100k'},
    """

    folder = os.path.dirname(file)

    # Read the geojson file and convert coordinate system
    df = gpd.read_file(file)
    starting_file = cdf.remap_coord(file)

    # Set API key.
    # A key can be obtained from (http://api.census.gov/data/key_signup.html). 
    #It will provide you with a unique 40 digit text string. Please keep track of this number. Store it in a safe place.
    k = cdf.Census(key)

    #FUNCTION CALLS

    # get the census dataframe for all the tracts in the given county
    va_census = cdf.get_census(file,k)
    state = cdf.get_state(file,k)

    #get the tract shape file
    tract_pth = folder + "tract.zip"
    va_tract = cdf.get_tract_shp(state,tract_pth)
    # Reproject tractfile to lat/long
    va_tract = va_tract.to_crs(epsg = 4326)

    #Merge tractfile and census dataframe 
    va_census_tract = cdf.merge_dataframes(va_census,va_tract)

    print("Merged file")
    # Join the building dataframe and the census information
    building_census_df : gpd.GeoDataFrame = gpd.sjoin(starting_file,va_census_tract, how="inner")
    #print(building_census_df.head())

    # get Column names
    for col in building_census_df.columns:
        print(col)

    #rename columns such that names are less than 10 characters long
    #building_census_df.rename(columns = {"OBJECTID_left":"OID_l","OBJECTID_right":"OID_r" } )

    #save joined file to local path
    joined_pth = folder + "GeojsonWithCensus.geojson"
    merged_geojson = gpd.GeoDataFrame.to_file(building_census_df, joined_pth )

    return merged_geojson

