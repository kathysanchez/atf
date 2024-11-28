import pandas as pd
import glob
import os
import openpyxl
newdir = "/Volumes/Mac_Passport/projects/personal/atf/"
os.chdir(newdir)
from utils import concat_dfs



# Import downloaded dataframes

    # Set file locations for dictionary of dfs

myfolderpath  = newdir + 'data_source/inspection_results/'
myxlsxfiles = glob.glob(os.path.join(myfolderpath, "*.xlsx")) # make list of files

mydataframes = {} # empty dictionary to store dataframes with filenames as keys

all_dataframes = []

for filename in os.listdir(myfolderpath):
    if filename.endswith('.xlsx'):
        myfilepath = os.path.join(myfolderpath, filename)
        try:
            mydf = pd.read_excel(myfilepath, skiprows=2, engine='openpyxl')
            all_dataframes.append(mydf)
        except Exception as e:
            print(f"Skipping file {filename} due to error: {e}")

    
    # Loop through folder files
for filename in os.listdir(myfolderpath):
    year = None
    month = None
    if filename.endswith('.xlsx'):
        myfilepath = os.path.join(myfolderpath, filename)
        mydf = pd.read_excel(myfilepath, skiprows=2, engine='openpyxl')
        if '2024' in filename:
            year = '2024'
        elif '2023' in filename:
            year = '2023'
        elif '2022' in filename:
            year = '2022'
        elif '2021' in filename:
            year = '2021'
        mydf['Year'] = year
    if filename.endswith('.xlsx'):
        myfilepath = os.path.join(myfolderpath, filename)
        mydf = pd.read_excel(myfilepath, skiprows=2)
        # Create a new key based on some conditions
        if 'january' in filename:
            month = '01'
        elif 'february' in filename:
            month = '02'
        elif 'march' in filename:
            month = '03'
        elif 'april' in filename:
            month = '04'        
        elif 'may' in filename:
            month = '05'
        elif 'june' in filename:
            month = '06'
        elif 'july' in filename:
            month = '07'  
        elif 'august' in filename:
            month = '08'
        elif 'september' in filename:
            month = '09'
        elif 'october' in filename:
            month = '10'  
        elif 'november' in filename:
            month = '11'
        elif 'december' in filename:
            month = '12'
        mydf['Month'] = month    
    #new_key = year + month
    #mydataframes[new_key] = mydf
    
    new_key = mydf['Year'] + mydf['Month']
    mydataframes[new_key] = mydf
    
    # Check some dfs

mydataframes['202206'].head()

mydataframes['202403'].columns.tolist()

# Append dfs

    # First, drop messy rows

for key, df in mydataframes.items():
    print(f"Proccessing DataFrame: {key}")
    df_cleaned = df[~df["Field Division"].str.contains("closed")]
    df_cleaned = df_cleaned[~df_cleaned["Field Division"].isna()]
    mydataframes[key] = df_cleaned

newdf = pd.concat(mydataframes.values(), ignore_index=False) # append

# Clean df

newdf = newdf.rename(columns={
    "Field Division": "Office",
    "Total FFL Compliance Inspections Completed*": "Inspections",
    "Total Inspections Resulting in Warning Conference": "Result_Warnings",
    "Total Number of Inspections Resulting in Revocation": "Result_License_Revocations"
})

newdf.columns.tolist()
newdf.Office.value_counts()
newdf["Office"] = newdf["Office"].str.strip()

    # New Columns

newdf['Pct_Warnings'] = newdf['Result_Warnings'] / newdf['Inspections']
newdf['Pct_Revocations'] = newdf['Result_License_Revocations'] / newdf['Inspections']

    # Format month and year to datetime

newdf["Month_Date"] = pd.to_datetime(newdf["Month"], format="%m")
newdf["Month_Name"] = newdf["Month_Date"].dt.month_name()


# National Figs

    # Line graph w each year as a line - for seasonality
    


# Region Figs

    # Make region var

northeast = ['Baltimore', 'Boston', 'Newark', 'New York', 'Philadelphia', 'Washington']
southeast = ['Atlanta', 'Charlotte', 'Louisville', 'Miami', 'Nashville', 'New Orleans', 'Tampa']
midwest = ['Chicago', 'Columbus', 'Detroit', 'Kansas City', 'St. Paul']
southwest = ['Dallas', 'Houston', 'Phoenix']
west = ['Denver', 'Los Angeles', 'San Francisco', 'Seattle']
  
regions = {
    'Baltimore': 'Northeast', 'Boston': 'Northeast', 'Newark': 'Northeast', 'New York': 'Northeast', 'Philadelphia': 'Northeast',
    'Atlanta': 'South', 'Charlotte': 'South', 'Louisville': 'South', 'Miami': 'South', 'Nashville': 'South', 'New Orleans': 'South', 'Tampa': 'South',
    'Chicago': 'Midwest', 'Columbus': 'Midwest', 'Detroit': 'Midwest', 'Kansas City': 'Midwest', 'St. Paul': 'Midwest',
    'Denver': 'West', 'Los Angeles': 'West', 'Phoenix': 'West' , 'San Francisco': 'West', 'Seattle': 'West', 'Washington': 'West'
} 

regions = {
    'Northeast': northeast,
    'Southeast': southeast,
    'Midwest': midwest,
    'Southwest': southwest,
    'West': west    
}  

newdf['Region'] = newdf['Office'].map(regions)

    
    
    # Line graph by region

    
    
    
    