import os, pandas
from census import Census
from datetime import datetime
start_time = datetime.now()
api_key = 'b7da053b9e664586b9e559dba9e73780602f0aab'  # CGR's API key

def housingunitchange(base_dir):
    # year_int = int(datetime.now().year) - 2
    # print(year_int)
    df0 = pandas.DataFrame()
    c = Census('b7da053b9e664586b9e559dba9e73780602f0aab')
    fields = ("NAME",
              "H001001",  # total housing units
              "H003003"   # total vacant units
    )
    df2010 = pandas.DataFrame()              
    df2000 = pandas.DataFrame()              
                    
    fips = {'Lucas':'39095','Wood':'39173','Monroe':'26115'}
    for vintage in [2010,2000]:
        df = pandas.DataFrame()
        print(vintage)
        for county in fips.keys():
            if county == 'Monroe':
                for cousub in ['06740', '26320','49700', '86740']:
                    temp_df = pandas.DataFrame(c.sf1.state_county_subdivision(fields,
                                                                              fips[county][:2],
                                                                              fips[county][2:],
                                                                              cousub, 
                                                                              year = vintage))
                    df = df.append(temp_df,sort=False,ignore_index=True)
                
                
            elif county == 'Lucas':
                for place in ['05732','76022','84770']:
                    temp_place_df = c.sf1.state_place(("NAME","H001001","H003003"),'39',place,year=vintage)
                    df = df.append(temp_place_df,sort=False,ignore_index=True)
                
                temp_cousub_df = pandas.DataFrame(c.sf1.state_county_subdivision(fields,
                                                                                 fips[county][:2],
                                                                                 fips[county][2:],
                                                                                 '*', 
                                                                                 year = vintage))
                df = df.append(temp_cousub_df, sort=False,ignore_index=True)
                # df = pandas.concat([temp_df,df],sort=False, ignore_index=True)
            elif county == 'Wood':
                temp_df = pandas.DataFrame(c.sf1.state_county_subdivision(fields,fips[county][:2],fips[county][2:],'*', year = vintage))
                # df = df.append(temp_df)
                df = df.append(temp_df,sort=False,ignore_index=True)
        df.rename(columns={"H001001":"Total Housing Units "+ str(vintage),"H003003":"Vacant Housing Units "+str(vintage)},
                inplace=True)
        df['joinid'] = ''        
        df['joinid'].loc[df['county'].isnull() == True] = df['place']        
        df['joinid'].loc[df['place'].isnull() == True] = df['county subdivision']
        # df['joinid'] = df['place'].loc[df['county'].isnull() == True] 
        print(df)    
        if vintage == 2010:
            df2010 = df
        else:
            df2000 = df 
        # print(df,df.columns.names)               
    # df0 = pandas.concat([df2010,df2000],axis=1,sort=False)
    df0 = pandas.merge(df2010,df2000,on='joinid')
    print(df0)
    df0['Total Housing Units 2010'] = pandas.to_numeric(df0['Total Housing Units 2010'])
    df0['Vacant Housing Units 2010'] = pandas.to_numeric(df0['Vacant Housing Units 2010'])
    df0['Total Housing Units 2000'] = pandas.to_numeric(df0['Total Housing Units 2000'])
    df0['Vacant Housing Units 2000'] = pandas.to_numeric(df0['Vacant Housing Units 2000'])
    
    # print(df0)    
    df0['% Change in Units from 2000-2010'] = (df0['Total Housing Units 2010'] -df0['Total Housing Units 2000'])/df0['Total Housing Units 2000']*100
    # df0['% Change in Vacant Units from 2000-2010'] = round((int(df0['Vacant Housing Units 2010']) - int(df0['Vacant Housing Units 2000']))/int(df0['Vacant Housing Units 2000']*100,1))

    # scrape this web page to get api metadata, i.e., 'label' :https://api.census.gov/data/2016/acs/acs5/variables.json
    # res = requests.get('https://api.census.gov/data/2016/acs/acs5/variables.json')
    # metadata = pandas.DataFrame(res.json()['variables']).transpose()
    # print(metadata[['label','concept']])

    # print(df0)
    writer = pandas.ExcelWriter(os.path.join(base_dir, 'housingdiff.xlsx'), engine= 'xlsxwriter')
    # housingchange = housingunitchange()
    # wrkbk = writer.book
    df0.to_excel(writer, 'housingchange')
    writer.save()
    print("Program Complete in " + str(datetime.now()-start_time))
    return df0

if __name__ == "__main__":
    housingunitchange('C:/Users/fullerm/Desktop')