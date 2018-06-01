

import census,os, pandas, requests, json


from datetime import datetime
start_time = datetime.now()
api_key = 'b7da053b9e664586b9e559dba9e73780602f0aab'  # CGR's API key

def housingunitdata():
    year_int = int(datetime.now().year) - 2
    print(year_int)
    ##
    # BUILD DIRECTORIES ON Z TO HOLD CSV FILES
    ##

    # Create subdirectories if they don't exist
    '''for geo in api_pull:
        directory = base_dir + '\\' + geo
        if not os.path.exists(directory):
            os.makedirs(directory)
    print('\bDone')'''
    tables = ['B25001',  # total housing units
              'B25003',  # housing tenure
              'B25034'  # year structure built--histogram?
               ]
    c = census.Census(api_key, year = 2016)
    fields = ("GEO_ID", "NAME",
              'B25001_001E', 'B25001_001M',  # total housing units
              'B25003_002E', 'B25003_002M',  # owner occupied housing units
              'B25003_003E', 'B25003_003M',  # renter occupied housing units
              'B25034_001E', 'B25034_001M',  # total housing units
              'B25034_002E', 'B25034_002M',  # built 2010 or later
              'B25034_003E', 'B25034_003M',  # built 2000-2009
              'B25034_004E', 'B25034_004M',  # built 1990-1999
              'B25034_005E', 'B25034_005M',  # built 1980-1989
              'B25034_006E', 'B25034_006M',  # built 1970-1979
              'B25034_007E', 'B25034_007M',  # built 1960-1969
              'B25034_008E', 'B25034_008M',  # built 1950-1959
              'B25034_009E', 'B25034_009M',  # built 1940-1949
              'B25034_010E', 'B25034_010M')  # built 1939 or earlier

    fips = {'Lucas':'39095','Wood':'39173','Monroe':'26115'}
    df = pandas.DataFrame()
    for county in fips:
        if county == 'Monroe':
            temp_df = pandas.DataFrame(c.acs5.state_county_subdivision(fields,fips[county][:2],fips[county][2:],'*'))
            temp_df = temp_df.loc[temp_df['county subdivision'].isin(['49700', # Luna Pier
                                 '06740', # Bedford
                                   '26320', # Erie
                                   '86740' # Whiteford
                                    ])]
            df = df.append(temp_df)
        else:
            temp_df = pandas.DataFrame(c.acs5.state_county_subdivision(fields,fips[county][:2],fips[county][2:],'*'))
            df = df.append(temp_df)

    # scrape this web page to get api metadata, i.e., 'label' :https://api.census.gov/data/2016/acs/acs5/variables.json
    res = requests.get('https://api.census.gov/data/2016/acs/acs5/variables.json')
    metadata = pandas.DataFrame(res.json()['variables']).transpose()
    # print(metadata[['label','concept']])

    print(df)
    print("Program Complete in " + str(datetime.now()-start_time))
    return df

if __name__ == "__main__":
    housingunitdata()