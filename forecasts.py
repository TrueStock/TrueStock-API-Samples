import json

import requests
import time


from requests import Request

# Update to match your API token
API_KEY = ''

url = 'https://janus-api-preprod.truestock.io/'

headers = {
    'Authorization': 'Bearer {token}'.format(token=API_KEY)
}


def create_retail_forecast(endpoint, forecast_horizon, stock_name, store_location):
    append_url = url + endpoint
    payload = {
        'forecastHorizon': forecast_horizon,
        'stockName': stock_name,
        'storeLocation': store_location
    }
    data_req = Request('POST', append_url, data=payload, files={'file': open('Retail_Mock_Data.csv', 'rb')},
                       headers=headers).prepare()
    s = requests.session()
    response = s.send(data_req)
    response_object = json.loads(response.content.decode())

    forecast_status = response_object.get("forecastStatus")
    forecastID = response_object.get("id")

    while forecast_status != "Complete.":
        temp_details = view_forecast(forecastID)
        forecast_status = temp_details.get("forecastStatus")
        time.sleep(5)
        print(forecast_status)

    return view_forecast(forecastID)


def get_all_forecasts(endpoint):
    append_url = url + endpoint
    response = requests.get(append_url, headers=headers)
    print("Status code: {code}".format(code=response.status_code))
    print(append_url)
    print(response.text)


def get_forecast_input_json(endpoint):
    append_url = url + endpoint
    response = requests.get(append_url, headers=headers)
    print('Status code: {code}'.format(code=response.status_code))
    print(response.text)


def get_forecast_result_csv(forecastID):
    append_url = url + 'forecast/download/result/' + str(forecastID)
    response = requests.get(append_url, headers=headers)
    return response.content.decode()


def get_forecast_result_json(endpoint):
    append_url = url + endpoint
    response = requests.get(append_url, headers=headers)
    print('Status code: {code}'.format(code=response.status_code))
    print(response.text)


def view_forecast(forecastID):
    append_url = url + 'forecast/view/' + str(forecastID)
    response = requests.get(append_url, headers=headers)
    return json.loads(response.content.decode())


if __name__ == '__main__':
    get_all_forecasts('forecast/all?page=1')
    get_forecast_input_json('forecast/get/input/78')
    get_forecast_result_csv('78')
    get_forecast_result_json('forecast/get/result/78')
    create_retail_forecast('forecast/retail/create', 3, 'aqua t-shirt', 6)
    view_forecast('78')
