import re
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta

# Main page URL
main_url = 'https://nieuwestroomprices.nieuwestroom.nl/'

# Get today's date and tomorrow's date
today = datetime.now().date()
tomorrow = today + timedelta(days=1)

# API URL with dynamic date variables
api_url = f'https://nieuwestroomprices.nieuwestroom.nl/api/prices/apx?IntervalStart={today}&IntervalEnd={tomorrow}'

# Visit the main page and find the script element with main.*.js
response = requests.get(main_url)
soup = BeautifulSoup(response.text, 'html.parser')
script_element = soup.find('script', src=re.compile('main.*.js'))

if script_element:
    script_src = script_element['src']

    # Open the JavaScript file
    script_url = main_url + script_src
    script_response = requests.get(script_url)
    script_content = script_response.text

    # Search for the x-api-key and extract the value
    api_key_pattern = re.compile(r'"x-api-key":"(.*?)"')
    api_key_match = api_key_pattern.search(script_content)

    if api_key_match:
        api_key = api_key_match.group(1)

        # Set the headers for the API request
        headers = {
            'x-api-key': api_key
        }

        # Send the API request and receive the JSON response
        response = requests.get(api_url, headers=headers)
        data = response.json()

        # Print the JSON data
        print(json.dumps(data, indent=4))
    else:
        print("Could not find the x-api-key in the JavaScript file.")

else:
    print("Could not find the script element with main.*.js.")
