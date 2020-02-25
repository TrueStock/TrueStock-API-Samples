import json

import requests
import time

from settings import API_KEY, URL, CSV
from requests import Request

headers = {
    'Authorization': 'Bearer {token}'.format(token=API_KEY)
}


def create_retail_forecast(forecast_horizon, stock_name, store_location):
    append_url = URL + 'forecast/retail/create'
    payload = {
        'forecastHorizon': forecast_horizon,
        'stockName': stock_name,
        'storeLocation': store_location
    }
    data_req = Request('POST', append_url, data=payload, files={'file': open(CSV, 'rb')},
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


def get_forecast_result_csv(forecast_id):
    append_url = URL + 'forecast/download/result/' + str(forecast_id)
    response = requests.get(append_url, headers=headers)
    return response.content.decode()


def view_forecast(forecast_id):
    append_url = URL + 'forecast/view/' + str(forecast_id)
    response = requests.get(append_url, headers=headers)
    return json.loads(response.content.decode())
