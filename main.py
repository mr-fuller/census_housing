import os
from housingunitdata import housingunitdata
from housingunitchangedecennial import housingunitchange
from movedatatoexcel import movedatatoexcel

year_int = 2016
print('  Building directory structure on Z:\...'),  # add a line to handle exceptions?
#acs_year = str(year_int - 4) + 'to' + str(year_int)[-2:]
base_dir = "Z:/fullerm/LRP/Housing/" + str(year_int)
# Create base directory if it doesn't exist
if not os.path.exists(base_dir):
    os.makedirs(base_dir)
df = housingunitdata()
movedatatoexcel(base_dir,df)
housingunitchange(base_dir)