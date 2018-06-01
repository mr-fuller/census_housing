# from traveltimebymode import traveltimebymode
from housingunitdata import housingunitdata
import pandas as pd
import os
from datetime import datetime
import numpy as np

def movedatatoexcel(base_dir,df):

    # year_int = datetime.now().year - 2
    # ##
    # # BUILD DIRECTORIES ON Z TO HOLD CSV FILES
    # ##
    # print('  Building directory structure on Z:\...'),  # add a line to handle exceptions?
    # #acs_year = str(year_int - 4) + 'to' + str(year_int)[-2:]
    # base_dir = "Z:/fullerm/CMP/" + datetime.now().strftime('%Y%m%d%H%M') + '\\' + str(year_int)
    # # Create base directory if it doesn't exist
    # if not os.path.exists(base_dir):
    #     os.makedirs(base_dir)
    #
    # df = pd.DataFrame()
    # df = df.append(())
    # #df = df.append(mi_sd())
    # df.set_index('NAME',inplace=True)
    # #print(df)
    df = df.apply(pd.to_numeric, errors='ignore') # why this? data written as strings, so sums were just concatenations
    #df['Drive Alone Percent'] = df['B08301_001E']




    #df = df.append(df.sum(numeric_only=True), ignore_index=True)

    # row_sum = df[df.columns.values.tolist()].sum()
    # print(row_sum)
    # row_sum = row_sum.rename(columns={'0':'Number of Trips'}) # Number of Trips might actually be number of people
    # row_sum_t = pd.DataFrame(data=row_sum).T
    #row_sum_t = row_sum_t.rename(index={0: "Number of Trips"})
    # new data frame with only relevant columns for modal split data
    new_df = df[[#'B25001_001E',   # total housing units
                        # 'B25003_002E',   # owner occupied housing units
                        # 'B25003_003E',  # renter occupied housing units
                        'NAME','county',
                        'B25034_001E',   # total housing units
                        'B25034_002E',   # built 2010 or later
                        'B25034_003E',   # built 2000-2009
                        'B25034_004E',   # built 1990-1999
                        'B25034_005E',   # built 1980-1989
                        'B25034_006E',   # built 1970-1979
                        'B25034_007E',   # built 1960-1969
                        'B25034_008E',   # built 1950-1959
                        'B25034_009E',   # built 1940-1949
                        'B25034_010E'  # built before 1940
                                ]].set_index('NAME')

    # df = df.append(row_sum_t)
    #print(df)


    writer = pd.ExcelWriter(os.path.join(base_dir, 'housing.xlsx'), engine= 'xlsxwriter')
    #csv_path =
    #df.to_excel()
    new_df = new_df.rename(columns={#'B25001_001E': 'Total Housing Units',
                        # 'B25003_002E': 'Owner Occupied Housing Units',
                        # 'B25003_003E': 'Renter Occupied Housing Units',
                        'B25034_001E': 'Total Housing Units',
                        'B25034_002E': 'Built 2010 or Later',
                        'B25034_003E': 'Built 2000-2009',
                        'B25034_004E': 'Built 1990-1999',
                        'B25034_005E': 'Built 1980-1989',
                        'B25034_006E': 'Built 1970-1979',
                        'B25034_007E': 'Built 1960-1969',
                        'B25034_008E': 'Built 1950-1959',
                        'B25034_009E': 'Built 1940-1949',
                        'B25034_010E': 'Built before 1940',
                        #oldlabel: dictofnewlabels[oldlabel]
                           })
    # new_df['Percent of Total'] = new_df['Number of Trips']/new_df.loc['All Modes','Number of Trips']
    # new_df = new_df.round({'Percent of Total':2})
    new_df.index.name = 'Subdivision'
    # new_df.sort_values('Number of Trips',ascending=False,inplace=True)
    # new_df
    # df=df[['S0802_C01_090E',  # total/all modes
    #                     'S0802_C02_090E','S0802_C02_001E',  # drive alone
    #                     'S0802_C03_090E', 'S0802_C03_001E',  # carpool
    #                     'S0802_C04_090E',  'S0802_C04_001E'# public transportation
    #                     # 2015 ACS doesn't appear to have data for other modes
    #                     ]]
    # df = df.rename(columns={'S0802_C01_090E':'All Modes',
    #                         'S0802_C02_001E': 'Drove Alone People',
    #                         'S0802_C02_090E':'Drove Alone Time',
    #                         'S0802_C03_001E': 'People Carpooled',
    #                         'S0802_C03_090E':'Carpooled',
    #                         'S0802_C04_001E':'People Public Transportation',
    #                         'S0802_C04_090E':'Public Transportation',
    #                        })
    # df.index.name = "Mean Travel Time (minutes)"
    # df.to_excel(writer,'Sheet2')
    wrkbk = writer.book
    # wrksht = writer.sheets['Sheet1']
    for county in ['095','173','115']:
        df = new_df.loc[new_df['county'] == int(county)]
        df.to_excel(writer, county)
        # percent_fmt = wrkbk.add_format({'align': 'right', 'num_format': '0.00%'})
        # wrksht.set_column('C:C', 12, percent_fmt)
        chrt = wrkbk.add_chart({'type':'bar','subtype':'percent_stacked'})


        chrt.add_series({'name': [county, 0, 3],
                         'categories': [county, 1, 0, len(df), 0],
                         'values': [county, 1, 3, len(df), 3],
                         # 'data_labels': {'percentage':True},
                         })
        chrt.add_series({'name':[county,0,4],
                         'categories':[county,1,0, len(df),0],
                         'values': [county,1,4,len(df),4],
                         # 'data_labels': {'percentage':True},
                         })
        chrt.add_series({'name': [county, 0, 5],
                         'categories': [county, 1, 0, len(df), 0],
                         'values': [county, 1, 5, len(df), 5],
                         # 'data_labels': {'percentage':True},
                         })
        chrt.add_series({'name': [county, 0, 6],
                         'categories': [county, 1, 0, len(df), 0],
                         'values': [county, 1, 6, len(df), 6],
                         # 'data_labels': {'percentage':True},
                         })
        chrt.add_series({'name': [county, 0, 7],
                         'categories': [county, 1, 0, len(df), 0],
                         'values': [county, 1, 7, len(df), 7],
                         # 'data_labels': {'percentage':True},
                         })
        chrt.add_series({'name': [county, 0, 8],
                         'categories': [county, 1, 0, len(df), 0],
                         'values': [county, 1, 8, len(df), 8],
                         # 'data_labels': {'percentage':True},
                         })
        chrt.add_series({'name': [county, 0, 9],
                         'categories': [county, 1, 0, len(df), 0],
                         'values': [county, 1, 9, len(df), 9],
                         # 'data_labels': {'percentage':True},
                         })
        chrt.add_series({'name': [county, 0, 10],
                         'categories': [county, 1, 0, len(df), 0],
                         'values': [county, 1, 10, len(df), 10],
                         # 'data_labels': {'percentage':True},
                         })
        chrt.add_series({'name': [county, 0, 11],
                         'categories': [county, 1, 0, len(df), 0],
                         'values': [county, 1, 11, len(df), 11],
                         # 'data_labels': {'percentage':True},
                         })
        chrt.set_title({'name':' 5-year ACS Housing by Year Built'})
        # chrt.set_x_axis({'name':'Subdivision'})
        chrt.set_y_axis({'name':'Subdivision','interval_unit':1})
        chrtsht = wrkbk.add_chartsheet(county + ' chart')
        chrtsht.set_chart(chrt)
        # wrksht.insert_chart('O2',chrt)
    #new_df
    writer.save()

if __name__ == '__main__':
    movedatatoexcel(housingdata())