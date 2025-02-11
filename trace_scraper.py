
from bs4 import BeautifulSoup
import pandas as pd
import time  # Add delays between requests
import requests

'''from selenium import webdriver # Need to install 
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Path to chromedriver 
service = Service('/Applications/geckodriver')
options = Options()

# Initialize the WebDriver
driver = webdriver.Firefox(service=service, options=options)
wait = WebDriverWait(driver, 10) 
'''

'''
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

#years = ["2020", "2021", "2022", "2023", "2024"]
'''

states = ["district-columbia", "oklahoma"]
years = ["2023"]


# Define the webpage URL
base_url = "https://www.atf.gov/resource-center/firearms-trace-data-{}-{}"



all_data = []

# Loop through each state and year
for state in states:
    for year in years:
        url = base_url.format(state, year)
        print(f"Begin scraping: {url}")

        # Send request to fetch content
        #driver.get(url)
        #response = requests.get(url)
        
        # Wait for the body to load
        #wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        '''
        # Review fetched content
        with open("temp.html", "w+") as file:
            file.write(response.text)
        '''       
        '''
        # Review fetched content
        with open("temp.html", "w", encoding="utf-8") as file:
            file.write(driver.page_source)
        '''
        
        # Get page source
        #page_source = driver.page_source
        
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
                        category = th_element.text.strip().replace(" ", "_")  # Extract the text only
                        value = td_element.text.strip().replace(",", "")  # Extract and clean the text from td
                
                        row_dict = {
                            "State": state,
                            "Year": year,
                            #"State": url.split("/")[-1].split("-")[0].capitalize(),  # Extract state from URL
                            #"Year": url.split("/")[-1].split("-")[1],  # Extract year from URL
                            "Section": section_title,  
                            "Category_or_Location": category,  # Header 
                            "Value": value  # Count or other value
                            }
                        print(f"Appending data: {row_dict}")
                        all_data.append(row_dict)  # Append to the data list
                    else:
                        print("No valid <th> or <td> in this row.")
            else:
                print(f"{state} {year}: No table found for {section_title}.")
    
        time.sleep(1)  # Avoid overwhelming the server

# Convert list of dictionaries to Pandas DataFrame
df = pd.DataFrame(all_data)

# Display the first few rows
print(df.head())

# Save to CSV
df.to_csv("output/scraped_data.csv", index=False)

print("Scraping complete. Data saved to csv.")























