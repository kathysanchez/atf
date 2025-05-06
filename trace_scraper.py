
from bs4 import BeautifulSoup
import pandas as pd
import time  # Add delays between requests
import requests
import os
import re
import numpy as np


def remove_characters(text, states_title_case, words):
    for state in states_title_case:
        text = text.replace(f'with an {state} Recovery', '').strip()
        text = text.replace(f'with a {state} Recovery', '').strip()
        text = text.replace('Firearm Traces', '').strip()
        text = text.replace(state, '').strip()


    for word in words:
        #text = text.replace(' ' + word.lower() + ' ', ' ').strip()
        text = re.sub(r'\b' + re.escape(word.strip()) + r'\b', '', text, flags=re.IGNORECASE)
    
    text = re.sub(r'\u200b', '', text)
    
    #return ' '.join(text.split())
    return re.sub(r'\s+', ' ', text).strip()



# Set working directory

print(os.getcwd())
os.chdir('/Volumes/Mac_Passport/projects/personal/atf')

# Assign states and years

states = ["alabama", "alabama", "arizona", "california", "colorado", 
          "connecticut", "delaware", "district-columbia", "florida", "georgia",
          "hawaii", "idaho", "illinois", "indiana", "iowa",
          "kansas", "kentucky", "louisiana", "maine", "maryland", 
          "massaschusetts", "michigan", "minnesota", "mississippi", "missouri",
          "montana", "nebraska", "nevada", "new-hampshire", "new-jersey", 
          "new-mexico", "new-york", "north-carolina", "north-dakota", "ohio", 
          "oklahoma", "oregon", "pennsylvania", "rhode-island", "south-carolina",
          "south-dakota", "tennessee", "texas", "utah", "vermont",
          "virginia", "washington", "west-virginia", "wisconsin", "wyoming",
          "puerto-rico"]

years = ["2020", "2021", "2022", "2023", "2024"]

'''
states = ["district-columbia", "oklahoma"]
years = ["2023"]
'''

# Assign strings for cleaning

words = ['Calendar', 'Year', '2023', '2022', '2021', '2020', 'on', 'with', 'a', 'an','for', 'in', 'the', 'with']

states_title_case = ["Alabama", "Alabama", "Arizona", "California", "Colorado", 
          "Connecticut", "Delaware", "District of Columbia", "Florida", "Georgia",
          "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa",
          "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", 
          "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri",
          "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", 
          "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", 
          "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina",
          "South Dakota", "Tennessee", "Texas", "Utah", "Vermont",
          "West Virginia", "Virginia", "Washington", "Wisconsin", "Wyoming",
          "Puerto Rico"]


# Define the webpage URL

base_url = "https://www.atf.gov/resource-center/firearms-trace-data-{}-{}"


# Get data for each state and year

all_data = [] # Empty list to store scraped data

for state in states:
    for year in years:
        url = base_url.format(state, year)
        print(f"Begin scraping: {url}")
        
        '''
        # Review fetched content
        with open("temp.html", "w+") as file:
            file.write(response.text)
        '''       
        
        response = requests.get(url)
        
        # Assign fetched text to soup
        soup = BeautifulSoup(response.text, "html.parser")
                        
        # Find all h4 elements
        h4_elements = soup.find_all("h4")
        #print(f"{state} {year} h4 found: {h4_elements}")

        # Loop through each h4 and find the following table            
        for h4 in h4_elements:
            section_title = h4.text.strip()  # Extract only the text (no html tags) and no leading/trailing spaces
            table = h4.find_next("table")  # Find the next table after h4

            if table:
                print(f"Found table: {section_title}")
                print(table.prettify())  
                rows = table.find_all('tr')
                
                # Loop through table rows
                for row in rows:  
                    th_element = row.find("th")  # Find th inside the row
                    td_element = row.find("td") 
                
                    if th_element and td_element:  # Ensure both elements exist
                        print(f"Found th: {th_element}, td: {td_element}")                        
                        category = th_element.text.strip() # Extract the text only
                        value = td_element.text.strip().replace(",", "")  # Extract and clean the text from td
                
                        state = state.replace("-", " ").title()
                        row_dict = {
                            "State": state,
                            "Year": year,
                            #"State": url.split("/")[-1].split("-")[0].capitalize(),  # Extract state from URL
                            #"Year": url.split("/")[-1].split("-")[1],  # Extract year from URL
                            "Section_raw": section_title,  
                            "Category_or_Location": category,  # Header 
                            "Value": value  # Count or other value
                            }
                        print(f"Appending data: {row_dict}")
                        all_data.append(row_dict)  # Append to the data list
                    else:
                        print("No valid <th> or <td> in this row.")
            else:
                print(f"{state} {year}: No table found for {section_title}.")
            
            # Find the paragraph that is immediately after the table
            note = table.find_next_sibling("p") if table else None 
            
            if note:
                print(f'{state} {year} found note: {note}')
                row_dict["Note"] = note.text.strip() 
            else:
                print(f"{state} {year}: No note found under {section_title}.")
                row_dict["Note"] = np.nan

            note2 = note.find_next_sibling("p") if table else None 
            
            if note2:
                print(f'{state} {year} found note: {note2}')
                row_dict["Note2"] = note2.text.strip() 
            else:
                print(f"{state} {year}: No note found under {section_title}.")
                row_dict["Note2"] = np.nan
    
        time.sleep(1)  # Avoid overwhelming the server

# Convert list of dictionaries to Pandas DataFrame
df = pd.DataFrame(all_data)


# Clean data
    
    # Remove Section characters 

df['Section'] = df['Section_raw'].apply(lambda x: remove_characters(x, states_title_case, words))
    
    # Rename Section categories
    
exact_replacements = {
    'Top Source States Firearms': 'Top States Where Firearms Came From',
    'Top 15 Source States': 'Top States Where Firearms Came From',
    'Top 15 Source States Firearms': 'Top States Where Firearms Came From',
    'Top 15 Source States Firearm': 'Top States Where Firearms Came From',
    'Top¬†Source States Firearms': 'Top States Where Firearms Came From',
    'Source States Firearms': 'Top States Where Firearms Came From',
    'Recovery City Firearms': 'Top Recovery Cities in State',
    'Top Recovery Cities Firearms': 'Top Recovery Cities in State',
    'Categories Reported': 'Top Crimes Reported',
    'Top Categories Reported': 'Top Crimes Reported',
    'Firearm Types': 'Firearms Types Recovered in State',
    'Time-To-Crime Rates Firearms': 'Time-to-Crime for Firearms Recovered in State',
    'Age of Possessors Firearms': 'Age of Possessors',
    '': 'Top Calibers Reported' # Delaware had an empty header
}
    
df['Section'] = df['Section'].replace(exact_replacements)

    # Replace empty note cells with missing
    
note_cols = ['Note', 'Note2']
for note_col in note_cols:
    df[note_col] = df[note_col].replace("", np.nan)

    # Replace notes with missing (for notes that belong to other tables)

df.loc[df["Note"].isna(), "Note2"] = np.nan 

    # Drop section headers that had no data

values_to_remove = ["Contents", "ATF Firearms Trace Data Disclaimer", "Total Number of Firearms Recovered and Traced"] 
df = df[~df["Section"].isin(values_to_remove)]


# Review categories and locations

df_category_values = pd.DataFrame(df['Category_or_Location'].value_counts())

# Remove weird characters from Category/Location

df['Category_or_Place'] = df['Category_or_Location'].str.replace('¬†', '', regex=False)

# Display the first few rows
print(df.head())

# Save to CSV
df.to_csv("./output/scraped_data.csv", index=False)

print("Scraping complete. Data saved to csv.")























