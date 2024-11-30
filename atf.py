import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.dates import DateFormatter
import glob
import os
import openpyxl
from typing import Optional
import squarify 
import numpy as np
newdir = "/Volumes/Mac_Passport/projects/personal/atf/"
os.chdir(newdir)
#from utils import concat_dfs

######################################################
# Importing and Cleaning #

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
    "Total Inspections Resulting in Warning Conference": "Warnings",
    "Total Number of Inspections Resulting in Revocation": "Revoked_Licenses"
})

newdf['Office'] = newdf['Office'].replace({'Totals:': 'Total'})

newdf.columns.tolist()
newdf.Office.value_counts(dropna=False)
newdf["Office"] = newdf["Office"].str.strip()

    # New columns

newdf['Pct_Warnings'] = newdf['Warnings'] / newdf['Inspections']
newdf['Pct_Revocations'] = newdf['Revoked_Licenses'] / newdf['Inspections']

    # Format month and year to datetime

newdf['Date'] = pd.to_datetime(newdf['Year'] + '-' + newdf['Month'] + '-01')
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


    # Int

mycolumns = ['Inspections', 'Warnings', 'Revoked_Licenses']

for col in mycolumns: 
    newdf[col] = newdf[col].astype(int)

######################################################
# Descriptives #

df_descriptives = newdf.groupby(['Office', 'Year'])[mycolumns].agg(['sum', 'mean', 'median', 'min', 'max']) # TODO examine future warning

######################################################
# Figures #

    # Manual color palette for seasonal figs
 
year_colors = {
    '2021': '#4b5276', 
    '2022': '#8ea4bd',  
    '2023': '#b8dbd6',  
    '2024': '#296248'
}
   


    
dftotal = newdf[newdf['Office'] == 'Total'].copy()
dftotal = dftotal.sort_values(by='Year', ascending=False)


def make_seasonal_line_plot (df:pd.DataFrame, yval: str, ylabel: str,  save_path: str = None):
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df, x='Month_cat', y=yval, hue='Year', palette=year_colors, linewidth=2.5, errorbar=None)
    plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'{x:,.0f}'))
    plt.ylabel(ylabel, fontsize=14)
    plt.xlabel(None) 
    plt.legend(title='Year', fontsize=14)
    if save_path:
       plt.savefig(save_path, bbox_inches='tight', dpi=300)
    plt.show()
    
    
def make_series_line_plot (df:pd.DataFrame, yval: str, ylabel: str, group_by: Optional[str] = None):
    '''
    Create a time-series line plot with optional grouping by a column.
    Optional parameter:
    group_by (Optional[str]): The column name to use for grouping (i.e., 'Region' or 'Office').
    '''
    plt.figure(figsize=(10, 6))
    
    if group_by:
        sns.lineplot(data=df, x='Date', y=yval, hue=group_by, linewidth=2.5, errorbar=None)
    else:
        sns.lineplot(data=df, x='Date', y=yval, linewidth=2.5, errorbar=None)
    
    # Format y axis tick labels with commas
    plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'{x:,.0f}'))
    
    # Format x axis tick labels in Jan 2021 format
    date_format = DateFormatter('%b %Y')
    plt.gca().xaxis.set_major_formatter(date_format)
    
    plt.ylabel(ylabel, fontsize=14)
    plt.xlabel(None) 
    plt.xticks(rotation=45) 
    plt.show()



# National Figs

for column in mycolumns:
    # Seasonality line fig (one line per year)
    make_seasonal_line_plot (df = dftotal, yval = column, ylabel = f'{column}')
    # Chronological full period line fig (one line)
    make_series_line_plot(df = dftotal, yval = column, ylabel = f'{column}')

make_seasonal_line_plot(df=dftotal, yval='Inspections', ylabel='Inspections', save_path="./output/plots/National_Inspection_Seasonality.png")





# Field Office Figs
'''
dfoffice_annual = newdf.groupby(['Office', 'Year'])[mycolumns].agg('sum').reset_index()
dfoffice_annual['Region'] = dfoffice_annual['Office'].map(regions)
'''

dfoffice = newdf.groupby(['Office'])[mycolumns].agg('sum').reset_index()

dfoffice['Region'] = dfoffice['Office'].map(regions)
dfoffice = dfoffice.dropna(subset=['Region']) # I tried dropping the Total row but could not completely get rid of remnants. value_counts() shows Total has 0 values.
dfoffice = dfoffice.sort_values(by='Inspections', ascending=False)

    # Treemap with office segments

def make_office_treemap (officecol: str, save_path: str = None):
    cmap = plt.cm.Blues  
    colors = cmap(np.linspace(0.3, 0.8, len(dfoffice)))
    label_colors = ['white' if np.mean(color[:3]) < 0.5 else 'black' for color in colors]    
    
    labels_with_values = [f"{office}\n{officecol}" for office, officecol in zip(dfoffice['Office'], dfoffice[officecol])]
    plt.figure(figsize=(12, 11))
    ax = squarify.plot(sizes=dfoffice[officecol], label=labels_with_values, color=colors, alpha=0.8)
    
    for i, label in enumerate(ax.texts):
        label.set_fontsize(12)
        label.set_color(label_colors[i]) 
    
    plt.axis('off')  
    formatted_column_name = f"{officecol.replace('_', ' ').title()}" # Remove underscore from Revoked_Licenses
    plt.title(f"ATF {formatted_column_name} by Field Office, Oct 2021 – Oct 2024", fontsize=16)
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()
    
for column in mycolumns:
    make_office_treemap(column, save_path = f"./output/plots/FieldOffice_Treemap_{column}.png")

'''
cmap = plt.cm.Blues  # Base colormap
colors = cmap(np.linspace(0.3, 0.8, len(dfoffice)))
label_colors = ['white' if np.mean(color[:3]) < 0.5 else 'black' for color in colors]
labels_with_values = [f"{office}\n{inspections}" for office, inspections in zip(dfoffice['Office'], dfoffice['Inspections'])]
plt.figure(figsize=(12, 11))
ax = squarify.plot(sizes=dfoffice['Inspections'], label=labels_with_values, color=colors, alpha=0.8)

for i, label in enumerate(ax.texts):
    label.set_fontsize(12)
    label.set_color(label_colors[i]) 
    
plt.axis('off')  
plt.title("ATF Inspections by Field Office, Oct 2021 – Oct 2024", fontsize=16)
plt.show()
'''


    # TODO Inspections bar chart with bar per Field Office. Full administration time period.




    
# Region Figs    

dfregion = newdf.groupby(['Region', 'Date'])[mycolumns].agg('sum').reset_index()
myregions = ['South', 'West', 'Northeast', 'Midwest']

for column in mycolumns:
    for region in myregions:
    # TODO add the time series! 
        
    # Chronological full period line fig (one line)
        filtered_df = dfregion[dfregion['Region'] == region]
        make_series_line_plot(
            df=filtered_df, yval=column, ylabel=f'{column} in {region}', group_by=None
        )
        # Too messy to overlay all region lines on a single chrono time series fig (e.g., one fig for inspections, etc.)
    
    
    