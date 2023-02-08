"""
Title: Add Census Data to Geodataframe

Description: This module allows you to augment an existing geojson
with census information at the US census tract block level.

Requirement: City's geojson

Author: Zoe De Simone, Github: @zoedesimone
"""


#from IPython.display import display
import censusapi.helperfunctions as chf
import geopandas as gpd
import os
from census import Census

def add_census_to_geojson(in_pth : str, out_pth : str, key : str):
    """
    Returns a geojson at out_pth with additional columns containing Census 
    Tract Level Data regarding building tract level ownership, population and income.

    Parameters
    ----------
    in_pth : str
        The file location of the (.geojson) file.
    out_pth : str
        The file location in which to save the ().geojson) augmented file.
    key : str
        The 40 digit text string. Can be obtained from (http://api.census.gov/data/key_signup.html)

    Returns
    -------
    geojson
        a geojson with additional columns appended containing Cenus Tract Level information.

    Column Legend - Census ACS 5
    -------
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

    folder = os.path.dirname(out_pth)

    try:
        with open(in_pth) as f:
            print(f)
        f.close

    except FileNotFoundError:
        print('The input folder path does not exist. Check your filepath.')

    else:
        # Convert gojson to universal coordinate system
        starting_in_pth = chf.remap_coord(in_pth)

        # Set API key.
        k = Census(key)

        #FUNCTION CALLS

        # get the census dataframe for all the tracts in the given county
        va_census = chf.get_census(in_pth,k)
        state = chf.get_state(in_pth,k)

        #get the tract shape in_pth
        tract_pth = folder + "tract.zip"
        va_tract = chf.get_tract_shp(state,tract_pth)
        # Reproject tractin_pth to lat/long
        va_tract = va_tract.to_crs(epsg = 4326)

        #Merge tractin_pth and census dataframe 
        va_census_tract = chf.merge_dataframes(va_census,va_tract)

        # Join the building dataframe and the census information
        building_census_df : gpd.GeoDataFrame = gpd.sjoin(starting_in_pth,va_census_tract, how="inner")
        #print(building_census_df.head())

        merged_geojson = gpd.GeoDataFrame.to_file(building_census_df, out_pth, driver='GeoJSON')

        return merged_geojson


def add_census_to_geojson(df: gpd.GeoDataFrame, key : str, *census_variables):
    """
    Returns a geojson with additional columns containing Census 
    Tract Level Data regarding building tract level ownership, population and income.

    Parameters
    ----------
    df : GeoDataFrame
        A geodataframe.
    key : str
        The 40 digit text string. Can be obtained from (http://api.census.gov/data/key_signup.html)

    Returns
    -------
    geojson
        a geojson with additional columns appended containing Cenus Tract Level information.

    Column Legend - Census ACS 5
    -------
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


    df = chf.remap_coord(df) #Convert gojson to universal coordinate system
    k = Census(key)#Set API key.

    # get the census dataframe for all the tracts in the given county
    va_census = chf.get_census(df,k)
    state = chf.get_state(df)

    tract_pth = "C://temp//" + "tract.zip" #create a temporary folder with the tract file
    va_tract = chf.get_tract_shp(state,tract_pth)
    va_tract = va_tract.to_crs(epsg = 4326) #Reproject tract file to lat/long

    #Merge tract and census dataframe 
    va_census_tract = chf.merge_dataframes(va_census,va_tract)

    # Join the building dataframe and the census information
    census_df : gpd.GeoDataFrame = gpd.sjoin(df,va_census_tract, how="inner")

    return census_df