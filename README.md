# Truestock 

Truestock predicts the future sales demand for retailers and manufacturers.  We use the latest machine learning technology and take into consideration a huge amount of factors such as weather, events, seasonality, holiday periods and many more! Explore our easy to use forecasting API so you too can predict the future accurately.

# TrueStock-API-Samples
This contains samples on how to use the TrueStock API for accurate forecasting.

## Python Code Samples Installation
To get started, follow these instructions:
1. If you haven't done it already, make a fork of this repo.
2. Clone to your local computer using git.
3. Make sure you have python 2.7 or later installed.
4. Find the settings.py file within the project and input your API key.
5. In the settings.py file you can also input the csv file to which you would like TrueStock to forecast. If you don't have one then we have provided an example one for you called "Retail_Mock_Data".csv
6. If you would like to create your own CSV file then we recommend using a random data generator like https://mockaroo.com/ to generate your own mock data and provide you with a csv.
7. Once done, simply execute and run the quickstart.py file to see a demonstration of using several of the Truestock endpoints. 
This will include getting a store location, creating a store location, generating a forecast and finally outputting the result.

## Java Code Samples Installation
To get started, follow these instructions:
1. If you haven't done it already, make a fork of this repo.
2. Clone to your local computer using git.
3. Make sure you have Java 13 or later installed.
4. Review the pom.xml and install the required dependencies using maven.
5. Find the src/main/java/com/truestock/main.java file within the project and input your API key along with the csv file you would like to upload.
6. We have also provided an example one for you csv called "Retail_Mock_Data".csv which you can use to demo how the truestock API predicts demand.
7. If you would like to create your own CSV file then we recommend using a random data generator like https://mockaroo.com/ to generate your own mock data and provide you with a csv.
8. Once done, simply execute and one-click run the main.java file to see a demonstration of using several of the Truestock endpoints. 

This will include getting a store location, creating a store location, generating a forecast and finally outputting the result.
## Tips:
- store locations can be managed from https://app.truestock.io/locations/all
- You may get an error with creating the store location.  If this happens, this may be because the address being inputted is already within our system, therefore we don't allow for duplicates so try adding another address.
 
## Documentation  
The TrueStock API is organised around REST. Our API has predictable resource-oriented URLs, accepts form-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication and verbs.
https://api.truestock.io/