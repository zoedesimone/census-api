"""
Title: CensusDataFunctions - Retrieving Census Data for a given city's geojson file

Description: This file has helper functions to output an augmented geojson file
containing census information at the US census tract block level 
given a geojson file.

Author: Zoe De Simone, Github: @zoedesimone
"""

import pandas as pd
import numpy as np
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

import pandas as pd

def rename_columns(df, column_mapping):
    """
    Rename the columns of the DataFrame based on the provided column mapping.

    Parameters:
        df (pd.DataFrame): Input DataFrame.
        column_mapping (dict): Dictionary containing old column names as keys and new column names as values.

    Returns:
        pd.DataFrame: DataFrame with renamed columns.

    Example usage:
      Assuming you have a DataFrame called 'data'.
      We want to rename the columns based on the mapping.

      data = pd.DataFrame({
          'old_col1': [10, 20, 30],
          'old_col2': [5, 15, 25],
          'old_col3': [7, 14, 21]
      })

      column_mapping = {
          'old_col1': 'new_col1',
          'old_col2': 'new_col2',
          'old_col3': 'new_col3'
      }

      data_new = rename_columns(data, column_mapping)
      print(data_new)

    """

    if not isinstance(column_mapping, dict):
        raise ValueError("Column mapping should be provided as a dictionary.")

    old_column_names = list(column_mapping.keys())
    new_column_names = list(column_mapping.values())

    if len(old_column_names) != len(new_column_names):
        raise ValueError("Number of old column names should match the number of new column names.")

    for old_col in old_column_names:
        if old_col not in df.columns:
            raise ValueError(f"Column '{old_col}' not found in the DataFrame.")

    df_new = df.rename(columns=column_mapping)

    return df_new


def compute_percentage_from_columns(df, columns_to_sum):
    """
    Compute the percentage of each column in the DataFrame based on the sum of specified columns.

    Parameters:
        df (pd.DataFrame): Input DataFrame.
        columns_to_sum (list): List of column names to be used for computing the sum.

    Returns:
        pd.DataFrame: DataFrame with additional percentage columns.

    Example usage:
      Assuming you have a DataFrame called 'data'.
      We want to compute the percentages based on the sum of columns 'A', 'B', and 'C'.

      data = pd.DataFrame({
          'A': [10, 20, 30],
          'B': [5, 15, 25],
          'C': [7, 14, 21]
      })

      columns_to_sum = ['A', 'B', 'C']

      data_new = compute_percentage_from_columns(data, columns_to_sum)
      print(data_new)

    """

    if not isinstance(columns_to_sum, list):
        raise ValueError("Columns to sum should be provided as a list.")

    for col in columns_to_sum:
        if col not in df.columns:
            raise ValueError(f"Column '{col}' not found in the DataFrame.")

    df_new = df.copy()

    # Compute sum of specified columns
    df_new['total_sum'] = df_new[columns_to_sum].sum(axis=1)

    # Compute percentages based on the sum
    for col in columns_to_sum:
        df_new[col + '_perc'] = df_new[col] / df_new['total_sum']

    df_new.drop(columns=['total_sum'], inplace=True)

    return df_new


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

import pandas as pd
import numpy as np

def stochastic_column(df, percentage_columns, new_column_name):
    """
    Create a new column in the DataFrame based on stochastic values from percentage columns.

    Parameters:
        df (pd.DataFrame): Input DataFrame.
        percentage_columns (list): List of column names containing percentages.
        new_column_name (str): Name of the new column to be created.

    Returns:
        pd.DataFrame: DataFrame with the new column added.
    """

    def generate_stochastic_value(percentage):
        return np.random.random() <= percentage

    if new_column_name in df.columns:
        raise ValueError("New column name already exists in the DataFrame.")

    if not isinstance(percentage_columns, list):
        raise ValueError("Percentage columns should be provided as a list.")

    for col in percentage_columns:
        if col not in df.columns:
            raise ValueError(f"Column '{col}' not found in the DataFrame.")

    df[new_column_name] = np.nan

    for index, row in df.iterrows():
        for col in percentage_columns:
            probability = row[col]
            if not pd.isna(probability):
                df.at[index, new_column_name] = 1 if generate_stochastic_value(probability) else np.nan

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


def stochastic_ownership_income(df, n_trials: int):

  df = rename_default_columns(df)

  #STEP 1: Assign Ownership/Rentership to buildings
  print("Stochastic Ownership Assignment")
  df['Owned'] = np.random.binomial(n_trials,df["OwnedPerc"] ) #probability of ownership

  # STEP 2: Delete Rented Buildings

  #Get the names of the indexes for which the building is Rented (value is 0)
  index_names = df[ (df['Owned'] == 0)].index
  df.drop(index_names, inplace = True) # drop Rented row indexes from dataFrame

  #STOCHASTIC INCOME ASSINGMENT - 7 INCOMES
  print("Stochastic Income Assignment")
  myArray = []
  for ind in df.index:
      tup = np.random.multinomial(n_trials, [df['less10k'][ind], df['10to20k'][ind], df['20to35k'][ind],df['35to50k'][ind],df['50to75k'][ind],df['75to100k'][ind],df['more100k'][ind]] )
      lst = list(tup) #convert tuple to list - ex. output [5, 8, 15, 12, 27, 13, 20]

      #the item of the list with the highest number of hits from the stochastic assignment is changed for a 1 and the rest get a 0.
      m = max(lst)
      index = lst.index(m)
      emptylst = [0,0,0,0,0,0,0]
      #change highest position with 1
      emptylst[index] = 1

      myArray.append(emptylst)

  df1 = pd.DataFrame(myArray, columns = ['Sto_10-','Sto_10-20','Sto_20-35','Sto_35-50','Sto_50-75','Sto_75-100','Sto_100+']) # new dataframe with stochastic income

  for col in df1.columns:
      print(col)


  df1['Sto_Income'] = df1.apply(lambda row : make_income(row['Sto_10-'], row['Sto_10-20'], row['Sto_20-35'],row['Sto_35-50'],row['Sto_50-75'],row['Sto_75-100'],row['Sto_100+']), axis = 1 )

  result = pd.concat([df,df1], axis = 1, join= 'inner') #join new dataframe with original one

  return result



