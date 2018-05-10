import census,os, pandas


from datetime import datetime
start_time = datetime.now()
api_key = 'b7da053b9e664586b9e559dba9e73780602f0aab'  # CGR's API key

year_int = int(datetime.now().year) - 2
print(year_int)
##
# BUILD DIRECTORIES ON Z TO HOLD CSV FILES
##
print('  Building directory structure on Z:\...'),  # add a line to handle exceptions?
#acs_year = str(year_int - 4) + 'to' + str(year_int)[-2:]
base_dir = "Z:/fullerm/LRP/Housing/" + str(year_int)
# Create base directory if it doesn't exist
if not os.path.exists(base_dir):
    os.makedirs(base_dir)
# Create subdirectories if they don't exist
'''for geo in api_pull:
    directory = base_dir + '\\' + geo
    if not os.path.exists(directory):
        os.makedirs(directory)
print('\bDone')'''
tables = ['B25001',  #total housing units
          'B25003',  #housing tenure
          'B25034'  #year structure built--histogram?
           ]
c = census.Census(api_key, year = 2016)
fields = ("GEO_ID", "NAME",
          'B25001_001E', 'B25001_001M',  #total housing units
          'B25003_002E', 'B25003_002M',  # owner occupied housing units
          'B25003_003E', 'B25003_003M',  # renter occupied housing units
          'B25034_001E', 'B25034_001M')

fips = {'Lucas':'39095','Wood':'39173','Monroe':'26115'}
df = pandas.DataFrame()
for county in fips:
    temp_df = pandas.DataFrame(c.acs5.state_county_subdivision(fields,fips[county][:2],fips[county][2:],'*'))
    df = df.append(temp_df)

#scrape this web page to get api metadata, i.e., 'label' :https://api.census.gov/data/2016/acs/acs5/variables.json

print(df)
print("Program Complete in " + str(datetime.now()-start_time))

#if __name__ == "__main__":
