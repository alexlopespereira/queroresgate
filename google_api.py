import requests
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

GOOGLE_GEOCODING_API_KEY = os.getenv('GOOGLE_GEOCODING_API_KEY')




def get_geocode_from_zipcode(zipcode):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={zipcode}&key={GOOGLE_GEOCODING_API_KEY}"
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
            return None, None, None
    else:
        print("Failed to connect to the API:", response.status_code)
        return None, None, None

# Replace 'YOUR_API_KEY' with your actual Google Cloud API key
# api_key = GOOGLE_GEOCODING_API_KEY
# zipcode = '70200004'  # Example ZIP code
# full_address, address, city, uf, latitude, longitude = get_geocode_from_zipcode(api_key, zipcode)
#
# if address:
#     print("Address:", address)
#     print("Latitude:", latitude)
#     print("Longitude:", longitude)
# else:
#     print("No data found for the provided ZIP code.")