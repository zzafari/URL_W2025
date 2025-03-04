import requests
import pandas as pd

API_KEY = '3c64d895f18a7dc61b53f1482d7c9d8b12ea4fe7'
BASE_URL = 'https://api.census.gov/data/'
variables = ['NAME', 'B19013_001E', 'B17001_002E', 'B17001_001E']
years = [2019, 2020, 2021, 2022, 2023]

for year in years:
    url = f"{BASE_URL}{year}/acs/acs5?get={','.join(variables)}&for=zip%20code%20tabulation%20area:*&key={API_KEY}"
    print(f"Requesting data from: {url}")
    
    response = requests.get(url)
    
    if response.status_code == 200:
        try:
            data = response.json()
            df = pd.DataFrame(data[1:], columns=data[0])
            df['Poverty Rate (%)'] = (df['B17001_002E'].astype(int) / df['B17001_001E'].astype(int)) * 100
            df.rename(columns={
                'NAME': 'ZCTA Name',
                'B19013_001E': 'Median Household Income',
                'B17001_002E': 'Population Below Poverty Level',
                'B17001_001E': 'Total Population for Poverty Determination',
                'zip code tabulation area': 'ZCTA'
            }, inplace=True)
            file_name = f'{year}_demographic_data.csv'
            df.to_csv(file_name, index=False)
            print(f"Data for {year} has been successfully retrieved and saved to '{file_name}'.")
        except ValueError:
            print(f"Error parsing JSON response for {year}. Response content: {response.text}")
    else:
        print(f"Failed to retrieve data for {year}. Status code: {response.status_code}. Response content: {response.text}")