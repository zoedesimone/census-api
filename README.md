# CensusAPI

Implementation of US Census API calls in form of a python library.

CensusAPI allows to output an augmented geojson file containing census information at the US census tract block level given a geojson file in the US.

## Install

census==0.8.19
censusgeocode==0.5.2
geopandas==0.9.0
pandas==1.5.1

## Usage

Defined in _censusgf.py_.

**`add_census_to_geojson`**: Returns a geojson with columns containing Census Tract Level Data regarding building tract level ownership, population and income.

Parameters:
- `in_pth`: str. The file location of the geojson building file.
- `out_pth`: str. The file location in which to save the augmented file.
- `key`: str. The 40 digit text string. Can be obtained from [the US Census site.](http://api.census.gov/data/key_signup.html)
- `census_variables`: tuple[str]. Default = None. 
    An optional tuple of strings identifying ACS 5 Census variables to augment the dataframe. If custom_variables is not specified the function will return an augmented geojson with default columns.

**`add_census_to_geojson_df`**:  Returns a geojson with additional columns containing Census Tract Level Data regarding building tract level ownership, population and income.

Parameters:
- `df`: GeoDataFrame. The input geodataframe.
- `key`: str. The 40 digit text string. Can be obtained from (http://api.census.gov/data/key_signup.html)
- `census_variables`: tuple[str]. Default = None. 
    An optional tuple of strings identifying ACS 5 Census variables to augment the dataframe. If custom_variables is not specified the function will return an augmented geojson with default columns.



**Default Census Variables:**

Default variables used to augment the geojson are specified below. 
They are taken from the [ACS 5, 2020](https://www.census.gov/data/developers/data-sets/acs-5year.html) dataset. Default variables can be found in the [Detailed Tables](https://api.census.gov/data/2020/acs/acs5/variables.json):

|Census Variable|Readable Column Name|                                               Variable Description                                                |
|--------------|------------------|------------------------------------------------------------------------------------------------------------------|
| B01003_001E  |      TotPop      |                                                 Total Population                                                 |
| B25003_003E  |     RentOcc      |                                                 Renter occupied                                                  |
| B25003_002E  |      OwnOcc      |                                                  Owner Occupied                                                  |
| B25121_001E  |      Income      |               Household income in the past 12 months (in 2020 inflation-adjusted dollars) by value               |
| B25121_002E  |     less10k      |          Household income the past 12 months (in 2020 inflation-adjusted dollars) --!!Less than $10,000          |
| B25121_017E  |     10to20k      |         Household income the past 12 months (in 2020 inflation-adjusted dollars) --!!$10,000 to $19,999          |
| B25121_032E  |     20to35k      |Estimate!!Total:!!Household income the past 12 months (in 2020 inflation-adjusted dollars) --!!$20,000 to $34,999 |
| B25121_047E  |     35to50k      |Estimate!!Total:!!Household income the past 12 months (in 2020 inflation-adjusted dollars) --!!$35,000 to $49,999 |
| B25121_062E  |     50to75k      |Estimate!!Total:!!Household income the past 12 months (in 2020 inflation-adjusted dollars) --!!$50,000 to $74,999 |
| B25121_077E  |     75to100k     |Estimate!!Total:!!Household income the past 12 months (in 2020 inflation-adjusted dollars) --!!$75,000 to $99,999 |
| B25121_092E  |     more100k     | Estimate!!Total:!!Household income the past 12 months (in 2020 inflation-adjusted dollars) --!!$100,000 or more  |

## Example

Example can be found in [_example.py_](https://github.com/zoedesimone/census-api/blob/main/example/example.py).
