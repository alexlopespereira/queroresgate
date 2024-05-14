import base64
import requests
import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

GOOGLE_GEOCODING_API_KEY = os.getenv('GOOGLE_GEOCODING_API_KEY')
GOOGLE_SHEETS_KEY = os.getenv('GOOGLE_SHEETS_KEY')



def get_geocode_from_zipcode(input_addr):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={input_addr}&key={GOOGLE_GEOCODING_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'OK':
            results = data['results'][0]
            full_address = results['formatted_address']
            latitude = results['geometry']['location']['lat']
            longitude = results['geometry']['location']['lng']
            city = list(filter(lambda d: 'administrative_area_level_2' in d['types'], results['address_components']))[0]['long_name']
            uf = list(filter(lambda d: 'administrative_area_level_1' in d['types'], results['address_components']))[0]['short_name']
            sublocality_level_1 = list(filter(lambda d: 'sublocality_level_1' in d['types'], results['address_components']))
            sublocality_level_1 = sublocality_level_1[0]['long_name'] if len(sublocality_level_1) > 0 else ""
            sublocality_level_2 = list(filter(lambda d: 'sublocality_level_2' in d['types'], results['address_components']))
            sublocality_level_2 = sublocality_level_2[0]['long_name'] if len(sublocality_level_2) > 0 else ""
            sublocality_level_3 = list(filter(lambda d: 'sublocality_level_3' in d['types'], results['address_components']))
            sublocality_level_3 = sublocality_level_3[0]['long_name'] if len(sublocality_level_3) > 0 else ""
            sublocality_level_4 = list(filter(lambda d: 'sublocality_level_4' in d['types'], results['address_components']))
            sublocality_level_4 = sublocality_level_4[0]['long_name'] if len(sublocality_level_4) > 0 else ""
            address = sublocality_level_1 + " " + sublocality_level_2 + " " + sublocality_level_3 + " " + sublocality_level_4
            return {"full_address": full_address, "address": address, "city": city, "uf": uf, "latitude": latitude, "longitude": longitude}
        else:
            return {"full_address": "", "address": "", "city": "", "uf": "", "latitude": "", "longitude": ""}
    else:
        print("Failed to connect to the API:", response.status_code)
        return {"full_address": "", "address": "", "city": "", "uf": "", "latitude": "", "longitude": ""}



def add_line_to_sheet(data, sheet_key):
    # Define the scope
    scope = ['https://www.googleapis.com/auth/spreadsheets']

    # Authenticate using the service account
    # credentials = ServiceAccountCredentials.from_json_keyfile_name(creds_file, scope)
    creds_json = base64.b64decode(GOOGLE_SHEETS_KEY).decode('utf-8')
    creds_dict = json.loads(creds_json)
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(credentials)

    # Open the sheet
    sheet = client.open_by_key(sheet_key).sheet1  # Assuming you're using the first sheet

    # Append a new line
    sheet.append_row(data, table_range='A1')

# Example usage:
# data = ["Name", "Email", "Phone"]  # Data to add
#   # Name of your Google Sheet
# add_line_to_sheet(data, sheet_key)