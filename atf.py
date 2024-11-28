import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import glob
import os
import openpyxl
newdir = "/Volumes/Mac_Passport/projects/personal/atf/"
os.chdir(newdir)
from utils import concat_dfs



# Import downloaded dataframes 

    # Manually made an extra row at top for oct 2021. No further manual changes.

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

 
for filename in os.listdir(myfolderpath):
    if filename.endswith('.xlsx'):
        myfilepath = os.path.join(myfolderpath, filename)
        mydf = pd.read_excel(myfilepath, skiprows=2, engine='openpyxl')
        # Make empty vars in proper scope
        year = None
        month = None
        # Get year from filename
        if '2024' in filename:
            year = '2024'
        elif '2023' in filename:
            year = '2023'
        elif '2022' in filename:
            year = '2022'
        elif '2021' in filename:
            year = '2021'
        # Make year column or skip
        if year:
            mydf['Year'] = year
        else:
            print(f"Year not found in filename: {filename}")
            continue  # Skip files with no month found in filename
        # Get month from filename
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
        # Make month column or skip
        if month:
            mydf['Month'] = month
        else:
            print(f"Month not found in filename: {filename}")
            continue  # Skip files with no month found in filename
        # Create new key 
        if year and month:  
            new_key = year + month
            mydataframes[new_key] = mydf
   
    # Check some dfs

mydataframes['202206'].head()

mydataframes['202403'].columns.tolist()

# Append dfs

    # First, drop messy rows

for key, df in mydataframes.items():
    print(f"Proccessing DataFrame: {key}")
    df_cleaned = df[~df["Field Division"].str.contains("closed", na=False)]
    df_cleaned = df_cleaned.dropna(subset=['Field Division'])
    #df_cleaned = df_cleaned[~df_cleaned["Field Division"].isna()]
    mydataframes[key] = df_cleaned

newdf = pd.concat(mydataframes.values(), ignore_index=False) # append

# Clean df

newdf = newdf.rename(columns={
    "Field Division": "Office",
    "Total FFL Compliance Inspections Completed*": "Inspections",
    "Total Inspections Resulting in Warning Conference": "Result_Warnings",
    "Total Number of Inspections Resulting in Revocation": "Result_License_Revocations"
})

newdf['Office'] = newdf['Office'].replace({'Totals:': 'Total'})

newdf.columns.tolist()
newdf.Office.value_counts(dropna=False)
newdf["Office"] = newdf["Office"].str.strip()

    # New columns

newdf['Pct_Warnings'] = newdf['Result_Warnings'] / newdf['Inspections']
newdf['Pct_Revocations'] = newdf['Result_License_Revocations'] / newdf['Inspections']

    # Format month and year to datetime

newdf["Month_Date"] = pd.to_datetime(newdf["Month"], format="%m")
#newdf["Month_Name"] = newdf["Month_Date"].dt.month_name()
newdf["Month_Name"] = newdf["Month_Date"].dt.strftime('%b')

    # Make region var

regions = {
    'Baltimore': 'Northeast', 'Boston': 'Northeast', 'Newark': 'Northeast', 'New York': 'Northeast', 'Philadelphia': 'Northeast',
    'Atlanta': 'South', 'Dallas': 'South', 'Houston': 'South',  'Charlotte': 'South', 'Louisville': 'South', 'Miami': 'South', 'Nashville': 'South', 'New Orleans': 'South', 'Tampa': 'South',
    'Chicago': 'Midwest', 'Columbus': 'Midwest', 'Detroit': 'Midwest', 'Kansas City': 'Midwest', 'St. Paul': 'Midwest',
    'Denver': 'West', 'Los Angeles': 'West', 'Phoenix': 'West' , 'San Francisco': 'West', 'Seattle': 'West', 'Washington': 'West'
} 

newdf['Region'] = newdf['Office'].map(regions)

newdf.Region.value_counts(dropna=False)


    # Categorical vars

newdf['Region'] = newdf['Region'].astype('category')
newdf['Office'] = newdf['Office'].astype('category')

        # For month, I need to set the correct order

month_order = [
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
]

newdf['Month_cat'] = pd.Categorical(newdf['Month_Name'], categories=month_order, ordered=True)

######################################################

# Figures

    # Manual color palete from https://www.color-hex.com/color-palette/1037356

year_colors = {
    '2021': '#00ffcc', 
    '2022': '#00cccc',  
    '2023': '#0099cc',  
    '2024': '#0066cc'
}
    
# National Figs

    # Line graph w each year as a line - for seasonality
    
dftotal = newdf[newdf['Office'] == 'Total'].copy()
dftotal = dftotal.sort_values(by='Year', ascending=False)


# Create a line plot
plt.figure(figsize=(10, 6))
sns.lineplot(data=dftotal, x='Month_cat', y='Inspections', hue='Year', palette=year_colors, linewidth=2.5)
plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'{x:,.0f}'))
plt.title("ATF Inspection Seasonality", fontsize=16)
plt.ylabel("Inspections", fontsize=14)
plt.xlabel(None) 
plt.legend(title='Year', fontsize=14)
plt.show()



# Region Figs
    
    # Line graph by region

    
    
    
    