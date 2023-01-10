# Census API key.
# A key can be obtained from (http://api.census.gov/data/key_signup.html). 
# It will provide you with a unique 40 digit text string. Please keep track of this number. Store it in a safe place.
key: str =  ""

#File path of geojson
in_f : str = "C:\\temp\\fileName.geojson"
out_f : str = "C:\\temp\\CensusAugmented.geojson"

import censusapi.censusgdf as cdf
cdf.addCensustoGeojsonFile(in_f,out_f, key)