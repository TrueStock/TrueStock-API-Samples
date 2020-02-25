import requests
import json
from requests import Request

# Update to match your API token
from forecasts import create_retail_forecast, get_forecast_result_csv

# Update to match your API token
API_KEY = ''

url = 'https://janus-api-preprod.truestock.io/'

headers = {'Content-Type': 'application/json',
           'Authorization': 'Bearer {token}'.format(token=API_KEY),

           }


def create_store_location(endpoint, hemisphere, country, store_time_zone, store_address):
    append_url = url + endpoint
    payload = {
        'hemisphere': hemisphere,
        'country': country,
        'storeTimeZone': store_time_zone,
        'storeAddress': store_address
    }
    data_req = Request('POST', append_url, data=json.dumps(payload), headers=headers).prepare()
    session = requests.session()
    response = session.send(data_req)
    print(response.status_code)
    print(response.reason)
    print(response.text)
    print('Status code: {code}'.format(code=response.status_code))
    if response.status_code == 500:
        print("Already exists. Enter new address")
        raise Exception("Latitude & Longitude already exists!")
    return json.loads(response.content.decode())


def get_store_location(endpoint):
    append_url = url + endpoint
    response = requests.get(append_url, headers=headers)
    print(str(json.loads(response.content.decode())))
    return json.loads(response.content.decode())


def delete_store_location(location_id):
    append_url = url + 'user/store-location/' + str(location_id) + '/'
    response = requests.delete(append_url, headers=headers)

    if response.status_code != 204:
        raise ValueError("Failed to delete store location")
    return response


def get_all_store_location(page_number):
    append_url = url + 'user/store-location/all?page=' + str(page_number)
    response = requests.get(append_url, headers=headers)
    print(str(json.loads(response.content.decode())))
    return json.loads(response.content.decode())


def delete_all_location():
    all_store_locations = get_all_store_location(1).get('results')

    for item in all_store_locations:
        temp_id = item.get('id')
        delete_store_location(temp_id)
        print('location deleted')


def get_store_options(endpoint):
    append_url = url + endpoint
    response = requests.get(append_url, headers=headers)
    print(str(json.loads(response.content.decode())))
    return json.loads(response.content.decode())


if __name__ == '__main__':
    delete_all_location()
    get_store_options('user/store-location/options')

    location_id = create_store_location('user/store-location', 'Northern', 'UnitedKingdom', 'GB',
                                        '42 Upper East St, Sudbury, CO10 1UB')

    storeLocationDetails = get_store_location('user/store-location/' + str(location_id.get('id')))

    forecastDistance = 3

    forecastDetails = create_retail_forecast('forecast/retail/create', forecastDistance, 'aqua t-shirt', storeLocationDetails.get('id'))

    csvData = get_forecast_result_csv(forecastDetails.get("id"))
    print(csvData)