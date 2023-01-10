# CensusAPI

Implementation of US Census API calls in form of a python library.

CensusAPI allows to output an augmented geojson file containing census information at the US census tract block level given a geojson file in the US.

## Usage

Defined in _censusgf.py_.

`addCensustoGeojsonFile`: Returns a geojson with columns containing Census Tract Level Data regarding building tract level ownership, population and income.

Parameters:
- `in_pth` : str. The file location of the geojson building file.
- `out_pth` : str. The file location in which to save the augmented file.
- `key` : str. The 40 digit text string. Can be obtained from (http://api.census.gov/data/key_signup.html)


## Example
Example can be found in [_example.py_](https://github.com/zoedesimone/census-api/blob/main/ExampleCall.py).
