"""
Title: CensusDataFunctions - Retrieving Census Data for a given city's geojson file

Description: This file has helper functions to output an augmented geojson file
containing census information at the US census tract block level 
given a geojson file.

Author: Zoe De Simone, Github: @zoedesimone
"""

import pandas as pd
import geopandas as gpd
import censusgeocode as cg
import urllib.request 
from os.path import exists
import random


def remap_coord(file):
    """Remap the coordinates of the Shapefile to the Global Lat/Long coordinate system"""
    
    va_shp = gpd.read_file(file) # Access shapefile

    # Reproject shapefile to Lat/Long
    va_shp = va_shp.to_crs(epsg = 4326) # Converts any coordinate system in the shapefile to a Latitude/Longitude coordinate system: "EPSG:4326" https://geopandas.org/en/v0.8.2/projections.html
    return va_shp

def remap_coord_df(gdf: gpd.GeoDataFrame):
    """Remap geodataframe to lat/log coordinate system."""
    gdf = gdf.to_crs(epsg = 4326) # Converts any coordinate system in the shapefile to a Latitude/Longitude coordinate system: "EPSG:4326" https://geopandas.org/en/v0.8.2/projections.html
    return gdf
   


def get_lat_long(geodataframe):
    """Get latitude and longitude for all the buildings in a geodataframe"""
    c_lat = []
    c_long = []
    
    for p in geodataframe.geometry:
        centroid =   list(p.centroid.coords)
        coords = centroid[0]
        lat = coords[0]
        lng = coords[1]

    c_lat.append(lat)
    c_long.append(lng)

    return c_lat,c_long


def get_census_df(la, lo, key, census_variables = None):
    """Create a dataframe with censusdata of all the tracts of the county, given a
buildings county and state"""

    default_variables = ('NAME','B01003_001E','B25002_002E','B25003_003E','B19013_001E','B19013_001M','B25121_001E','B25121_002E','B25121_017E','B25121_032E','B25121_047E','B25121_062E','B25121_077E','B25121_092E' )
    
    if census_variables != None:
       default_variables = census_variables
    else:
       default_variables = default_variables

    getgeoinfo = cg.coordinates(x=la, y=lo)

    censusblock = getgeoinfo['2020 Census Blocks']
    block =censusblock[0] #unwrap the dictionary from the list

    geoID = block['GEOID']
    stateID = block['STATE']
    countyID = block['COUNTY']
    tractID = block['TRACT']
    blockID = block['BLOCK']
    objID = block['OBJECTID']

    #B19013_001E: Median Household income last 12 months
    va_census = key.acs5.state_county_tract(fields = default_variables,
                                        state_fips = stateID,
                                        county_fips = '*',
                                        tract = '*',
                                        year = 2020)
    va_df = pd.DataFrame(va_census)
    
    # Combine state, county, and tract columns together to create a new string and assign to new column
    va_df["GEOID"] = va_df["state"] + va_df["county"] + va_df["tract"]
    
    #get objectID
    va_df["OID"] = objID

    #remove useless columns
    va_df = va_df.drop(columns = ["state", "county", "tract"])

    return va_df

def rename_default_columns(df):
    """
    Rename default census variables with intelligible names.
    """
    df.rename(columns = {'B19013_001E':'MedIncome',
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
     inplace = True)

    df["OwnedPerc"] = df['OwnOcc'] / (df['RentOcc']+ df['OwnOcc'])
    df["RentPerc"] = df['RentOcc'] / (df['RentOcc']+ df['OwnOcc'])

    #Convert count to percentage across income groups
    df['total_pop'] = df['less10k']+ df['10to20k']+ df['20to35k']+ df['35to50k'] +  df['50to75k']+ df['75to100k'] + df['more100k']

    df['less10k'] = df['less10k']/ df['total_pop']
    df['10to20k'] = df['10to20k'] / df['total_pop']
    df['20to35k'] = df['20to35k'] / df['total_pop']
    df['35to50k']  = df['35to50k'] / df['total_pop']
    df['50to75k'] = df['50to75k'] / df['total_pop']
    df['75to100k'] = df['75to100k'] / df['total_pop']
    df['more100k'] = df['more100k'] / df['total_pop']
    
    return df

def make_income(c1,c2,c3,c4,c5,c6,c7):
      #Approximation of AMI bins for Oshkosh
    """va_df["<80AMI"] = va_df['less10k']+ va_df['10to20k']+ va_df['20to35k']+ va_df['35to50k']
    va_df["<150AMI"] = va_df['50to75k']+ va_df['75to100k']
    va_df[">150AMI"] = va_df['more100k']

    va_df["total_pop"] = va_df["<80AMI"] + va_df["<150AMI"] + va_df[">150AMI"]

    va_df["<80AMI"] = va_df["<80AMI"]/va_df["total_pop"] 
    va_df["<150AMI"] = va_df["<150AMI"] / va_df["total_pop"]
    va_df[">150AMI"] = va_df[">150AMI"] / va_df["total_pop"]"""

    if c1 == 1: #less10k
      inc = random.randint(5000, 10000)
    elif c2 == 1: #'10to20k'
      inc = random.randint(10000, 20000)
    elif c3 ==1 : #'20to35k'
      inc = random.randint(20000, 35000)
    elif c4 == 1: #'35to50k'
      inc = random.randint(35000, 50000)
    elif c5 == 1: #'50to75k'
      inc = random.randint(50000, 75000)
    elif c6 ==1 : #'75to100k'
      inc = random.randint(75000, 100000)
    elif c7== 1: #'more100k'
      inc = random.randint(100000, 400000)

    return inc
  


def get_census_df_DP(la, lo, key):
    """Create a dataframe with censusdata of all the tracts of the county, given a
  buildings county and state
  from: https://api.census.gov/data/2019/acs/acs5/profile/groups/DP03.json"""
    
    getgeoinfo = cg.coordinates(x=la, y=lo)

    censusblock = getgeoinfo['2019 Census Blocks']
    block =censusblock[0] #unwrap the dictionary from the list

    geoID = block['GEOID']
    stateID = block['STATE']
    countyID = block['COUNTY']
    tractID = block['TRACT']
    blockID = block['BLOCK']
    objID = block['OBJECTID']

    #B19013_001E: Median Household income last 12 months
    va_census = key.acs5.profile.state_county_tract(fields = ('NAME','DP03_0052E','DP03_0053E','DP03_0054E','DP03_0055E'),
                                        state_fips = stateID,
                                        county_fips = '*',
                                        tract = '*',
                                        year = 2020)
    va_df = pd.DataFrame(va_census)
    
    # Combine state, county, and tract columns together to create a new string and assign to new column
    va_df["GEOID"] = va_df["state"] + va_df["county"] + va_df["tract"]
    
    #get objectID
    va_df["OID"] = objID

    va_df.rename(columns = {'DP03_0052E':'under10','DP03_0053E':'10to15','DP03_0054E':'15to25','DP03_0055E':'25to35'}, inplace = True)

    va_df["OwnedPerc"] = va_df['OwnOcc'] / (va_df['RentOcc']+ va_df['OwnOcc'])

    #remove useless columns
    va_df = va_df.drop(columns = ["state", "county", "tract"])

    return va_df

def get_stateID(lat,lng):
    """Get the State ID givent the latitude and longitude of one geometry."""
    getgeoinfo = cg.coordinates(x=lat, y=lng)

    censusblock = getgeoinfo['2020 Census Blocks']
    block =censusblock[0] #unwrap the dictionary from the list

    stateID = block['STATE']
    return stateID


def get_census(df, key):
  """Get census data for an entire COUNTY, given it's latitude and longitude
1 GENERAL API CALL FOR ALL THE TRACTS"""

  #f_remap = remap_coord(file)
  lat_long = get_lat_long(df)
  lat = lat_long[0][0]
  lng = lat_long[1][0]

  df = get_census_df(lat,lng,key)

  return df

def get_state(df, key) -> str:
  """Get the StateID for an entire COUNTY, given the latitude and longitude of 
  one building in the file."""

  #f_remap = remap_coord(file)
  lat_long = get_lat_long(df)
  lat = lat_long[0][0]
  lng = lat_long[1][0]
  
  state = get_stateID(lat,lng)
  return state


def get_tract_shp(stateID:str, tract_file_path:str):
  """Access shapefile of US States Census Tracts."""
  page = "https://www2.census.gov/geo/tiger/TIGER2020/TRACT/tl_2020_" + stateID +"_tract.zip"
  file_exists = exists(tract_file_path)
  if file_exists== False:
    page = "https://www2.census.gov/geo/tiger/TIGER2020/TRACT/tl_2020_" + str(stateID) +"_tract.zip"
    urllib.request.urlretrieve(page, tract_file_path)

  va_tract = gpd.read_file(tract_file_path)
  return va_tract


def merge_dataframes(census,shape):
  """Merge dataframes. Join the attributes of the dataframes together
 Source: https://geopandas.org/docs/user_guide/mergingdata.html"""
  merged = shape.merge(census, on = "GEOID")
  return merged


def get_geoID_2(lat,lng,key):
  """Get the GEOID, given a latitude and longitude coordinate."""
  getgeoinfo = cg.coordinates(x=lat, y=lng)

  censusblock = getgeoinfo['2020 Census Blocks']
  block =censusblock[0] #unwrap the dictionary from the list

  geoID = block['GEOID']
  stateID = block['STATE']
  countyID = block['COUNTY']
  tractID = block['TRACT']
  #blockID = block['BLOCK']
  #objID = block['OBJECTID']

  Geoid = str(stateID) + str(countyID) + str(tractID)

  return Geoid





