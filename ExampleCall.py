# Census API key.
# A key can be obtained from (http://api.census.gov/data/key_signup.html). 
# It will provide you with a unique 40 digit text string. Please keep track of this number. Store it in a safe place.
key: str =  ""

#File path of geojson
f : str = "C:\\temp\\UBEMTemp\\Oshkosh\\oshkoshData.geojson"

import CensusGdfAPI as cd
cd.AddCensustoGeojsonFile(f, key)