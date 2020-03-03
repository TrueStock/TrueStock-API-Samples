package com.truestock;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.google.gson.*;
import org.apache.http.HttpEntity;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.ContentType;
import org.apache.http.entity.mime.MultipartEntityBuilder;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClientBuilder;
import org.apache.http.util.EntityUtils;

import java.io.*;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.*;


public class Main {


    private static String url = "https://janus-api.truestock.io/";
    //update to match your token key
    private static String token = " ";
    //update to match your csv file
    private static String csv = " ";



    public static void main(String[] args) throws IOException, InterruptedException {

        getStoreOptions();

        //store locations can be managed from https://app.truestock.io/locations/all
        //Does not accept duplicates. eg. if longitude and latitude of a store address already exists.
        String newLocationObject = createStoreLocation("Northern", "UnitedKingdom", "GB",
                "57 Main St, Ballymena, BT42 4JP");

        System.out.println(newLocationObject);
        JsonElement element = new JsonParser().parse(newLocationObject);
        JsonObject json = element.getAsJsonObject();
        String newLocationObjectId = json.get("id").getAsString();
        String storeLocationDetails = getStoreLocation(newLocationObjectId);
        String forecastDistance = "3";

        JsonElement jsonElement1 = new JsonParser().parse(storeLocationDetails);
        JsonObject jsonObject2 = jsonElement1.getAsJsonObject();
        String storeLocationDetailsId = jsonObject2.get("id").getAsString();
        JsonObject temp = jsonElement1.getAsJsonObject();

       String forecastDetails = createRetailForecast(forecastDistance, "aqua t-shirt", storeLocationDetailsId);

        String csvData = getForecastResultCSV(storeLocationDetailsId);
        System.out.println(csvData);

    }


    private static String createStoreLocation(String hemisphere, String country, String storeTimeZone, String storeAddress) throws IOException, InterruptedException {
        var values = new HashMap<String, String>() {{
            put("hemisphere", hemisphere);
            put("country", country);
            put("storeTimeZone", storeTimeZone);
            put("storeAddress", storeAddress);

        }};
        var objectMapper = new ObjectMapper();
        String requestBody = objectMapper.writeValueAsString(values);
        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("https://janus-api-preprod.truestock.io/user/store-location"))
                .header("Content-Type", "application/json")
                .header("Authorization", "Bearer " + token)
                .POST(HttpRequest.BodyPublishers.ofString(requestBody))
                .build();

        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        if (response.statusCode() == 500) {
            System.out.println("Already exists. Enter new address");
            try {
                throw new Exception("Longtitude and Latitude Already exists!");
            } catch (Exception e) {
                e.printStackTrace();
            }
        }

        return response.body();

    }

    private static void getStoreOptions() {
        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("https://janus-api-preprod.truestock.io/user/store-location/options"))
                .header("Content-Type", "application/json")
                .header("Authorization", "Bearer " + token)
                .GET()
                .build();

        sendRequest(client, request);

    }


    private static void getAllStoreLocation(int pageNumber) {
        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(url + "/user/store-location/all?page=" + pageNumber))
                .header("Content-Type", "application/json")
                .header("Authorization", "Bearer " + token)
                .GET()
                .build();

        sendRequest(client, request);
    }

    private static void getAllForecasts(int pageNumber) {
        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(url + "/forecast/all?page=" + pageNumber))
                .header("Content-Type", "application/json")
                .header("Authorization", "Bearer " + token)
                .GET()
                .build();

        client.sendAsync(request, HttpResponse.BodyHandlers.ofString())
                .thenApply(HttpResponse::body)
                .thenAccept(System.out::println)
                .join();
    }

    private static String getForecastResultCSV(String forecastId) throws IOException, InterruptedException {
        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(url + "forecast/download/result/" + forecastId + "/"))
                .header("Content-Type", "application/csv")
                .header("Authorization", "Bearer " + token)
                .GET()
                .build();

        sendRequest(client, request);
        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());

        return response.body();
    }

    private static String getStoreLocation(String endpoint) throws IOException, InterruptedException {
        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(url + "user/store-location/" + endpoint + "/"))
                .header("Content-Type", "application/json")
                .header("Authorization", "Bearer " + token)
                .GET()
                .build();

        sendRequest(client, request);
        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());

        return response.body();
    }

    private static void sendRequest(HttpClient client, HttpRequest request) {
        client.sendAsync(request, HttpResponse.BodyHandlers.ofString())
                .thenApply(HttpResponse::body)
                .thenAccept(System.out::println)
                .join();
    }

    private static void getForecastInput(int forecastId) {
        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(url + "forecast/get/input/" + forecastId + "/"))
                .header("Content-Type", "application/json")
                .header("Authorization", "Bearer " + token)
                .GET()
                .build();

        sendRequest(client, request);
    }

    private static void getForecastResultJSON(int forecastId) {
        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(url + "forecast/get/result/" + forecastId + "/"))
                .header("Content-Type", "application/json")
                .header("Authorization", "Bearer " + token)
                .GET()
                .build();

        sendRequest(client, request);
    }

    private static String createRetailForecast(String forecastHorizon, String stockName, String storeLocation) throws IOException, InterruptedException {

        HttpEntity entity = MultipartEntityBuilder
                .create()
                .addTextBody("forecastHorizon", forecastHorizon)
                .addTextBody("stockName", stockName)
                .addTextBody("storeLocation", storeLocation)
                .addBinaryBody("file",
                        new File(csv),
                        ContentType.create("application/csv"), "Retail-Input.csv")
                .build();
        HttpPost request = new HttpPost(url + "forecast/retail/create");
        request.setEntity(entity);
        request.setHeader("Authorization", "Bearer " + token);
        CloseableHttpClient client = HttpClientBuilder.create().build();

        CloseableHttpResponse response = client.execute(request);

        String jsonString = EntityUtils.toString(response.getEntity());
        JsonElement jsonElement = new JsonParser().parse(jsonString);

        JsonObject jsonObject = jsonElement.getAsJsonObject();
        String forecastID = jsonObject.get("id").getAsString();
        boolean completed = jsonObject.get("forecastStatus").getAsString().equals("Complete.");

        while (!completed) {

            String tempDetails = viewForecast(forecastID);
            JsonElement tempJsonElement = new JsonParser().parse(tempDetails);
            JsonObject tempJsonObject = tempJsonElement.getAsJsonObject();
            completed = tempJsonObject.get("forecastStatus").getAsString().equals("Complete.");

            Thread.sleep(5000);
            System.out.println(tempJsonObject.get("forecastStatus"));

        }

        return viewForecast(forecastID);

    }

    private static String viewForecast(String forecastId) throws IOException, InterruptedException {

        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(url + "forecast/view/" + forecastId + "/"))
                .header("Content-Type", "application/json")
                .header("Authorization", "Bearer " + token)
                .GET()
                .build();

        sendRequest(client, request);
        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());

        return response.body();

    }


}
