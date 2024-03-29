"""
Title: Add Census Data to Geodataframe

Description: This module allows you to augment an existing geojson
with census information at the US census tract block level.

Requirement: City's geojson file

Author: Zoe De Simone, Github: @zoedesimone
"""

import censusapi.helperfunctions as chf
import geopandas as gpd
import os
from census import Census

def add_census_to_geojson(in_pth : str, out_pth : str, key : str, census_variables: tuple[str] = None):
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
    census_variables: tuple[str]
        A custom tuple of strings identifying ACS 5 Census variables to augment the dataframe. If custom_variables is
        not specified the function will return an augmented geojson with default columns.

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

    #folder = os.path.dirname(out_pth)

    try:
        open(in_pth)
    except FileNotFoundError as err:
        print('The input folder path does not exist. Check your input filepath.')
        raise 

    try:
        folder = os.path.dirname(out_pth)
    except FileNotFoundError as err:
        print('The output folder path does not exist. Check your output filepath.')
        raise 
        
    else:
        # Convert gojson to universal coordinate system
        remapped_df = chf.remap_coord(in_pth)

        # Set API key.
        k = Census(key)

        # get the census dataframe for all the tracts in the given county
        lat = chf.get_lat_long(remapped_df)[0][0]
        lng = chf.get_lat_long(remapped_df)[1][0]
        va_census = chf.get_census_df(lat,lng,k,census_variables)

        state = chf.get_state(remapped_df,k)

        #get the tract shape in_pth
        tract_pth = folder + "tract.zip"
        va_tract = chf.get_tract_shp(state,tract_pth)
        # Reproject tractin_pth to lat/long
        va_tract = va_tract.to_crs(epsg = 4326)

        #Merge tractin_pth and census dataframe 
        va_census_tract = chf.merge_dataframes(va_census,va_tract)

        # Join the building dataframe and the census information
        building_census_df : gpd.GeoDataFrame = gpd.sjoin(remapped_df,va_census_tract, how="inner")
        #print(building_census_df.head())

        merged_geojson = gpd.GeoDataFrame.to_file(building_census_df, out_pth, driver='GeoJSON')

        return merged_geojson


def add_census_to_geojson_df(df: gpd.GeoDataFrame, key : str, census_variables: tuple[str] = None):
    """
    Returns a geojson with additional columns containing Census 
    Tract Level Data regarding building tract level ownership, population and income.

    Parameters
    ----------
    df : GeoDataFrame
        A geodataframe.
    key : str
        The 40 digit text string. Can be obtained from (http://api.census.gov/data/key_signup.html)
    census_variables: tuple[str]
        A custom tuple of strings identifying ACS 5 Census variables to augment the dataframe. If custom_variables is
        not specified the function will return an augmented geojson with default columns.

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


    df = chf.remap_coord_df(df) #Convert gojson to universal coordinate system
    k = Census(key)#Set API key.

    # get the census dataframe for all the tracts in the given county
    lat = chf.get_lat_long(df)[0][0]
    lng = chf.get_lat_long(df)[1][0]
    va_census = chf.get_census_df(lat,lng,k,census_variables)
    state = chf.get_state(df,k)

    tract_pth = "C://temp//" + "tract.zip" #create a temporary folder with the tract file
    va_tract = chf.get_tract_shp(state,tract_pth)
    va_tract = va_tract.to_crs(epsg = 4326) #Reproject tract file to lat/long

    #Merge tract and census dataframe 
    va_census_tract = chf.merge_dataframes(va_census,va_tract)

    # Join the building dataframe and the census information
    census_df : gpd.GeoDataFrame = gpd.sjoin(df,va_census_tract, how="inner")

    os.remove(tract_pth)

    return census_df