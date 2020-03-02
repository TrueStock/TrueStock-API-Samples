import requests
import json
from requests import Request
from settings import URL, API_KEY
from forecasts import create_retail_forecast, get_forecast_result_csv

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer {token}'.format(token=API_KEY),

}


def create_store_location(hemisphere, country, store_time_zone, store_address):
    append_url = URL + 'user/store-location'
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
    append_url = URL + endpoint
    response = requests.get(append_url, headers=headers)
    print(str(json.loads(response.content.decode())))
    return json.loads(response.content.decode())


def delete_store_location(location_id):
    append_url = URL + 'user/store-location/' + str(location_id) + '/'
    response = requests.delete(append_url, headers=headers)

    if response.status_code != 204:
        raise ValueError("Failed to delete store location")
    return response


def get_all_store_location(page_number):
    append_url = URL + 'user/store-location/all?page=' + str(page_number)
    response = requests.get(append_url, headers=headers)
    print(str(json.loads(response.content.decode())))
    return json.loads(response.content.decode())


def get_store_options():
    append_url = URL + 'user/store-location/options'
    response = requests.get(append_url, headers=headers)
    print(str(json.loads(response.content.decode())))
    return json.loads(response.content.decode())


if __name__ == '__main__':
    get_store_options()

    # store locations can be managed from https://app.truestock.io/locations/all
    # Does not accept duplicates. eg. if longitude and latitude of a store address already exists.
    location_id = create_store_location('Northern', 'UnitedKingdom', 'GB',
                                        'Unit 1, Ratio Point, St. Richards Rd, Evesham, WR11 1ZG')

    storeLocationDetails = get_store_location('user/store-location/' + str(location_id.get('id')))

    forecastDistance = 3

    forecastDetails = create_retail_forecast(forecastDistance, 'aqua t-shirt',
                                             storeLocationDetails.get('id'))

    csvData = get_forecast_result_csv(forecastDetails.get("id"))
    print(csvData)
