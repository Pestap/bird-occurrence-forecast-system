# Bird Occurrence Forecast System

The project is a part of Bachelor of Science thesis at Faculty of  Electronics, Telecommunications and Informatics at Gdańsk University of Technology

---
### Authors
- Bartłomiej Szczepaniec
- Piotr Pesta
---
## REST API documentation

### Available endpoints:
1. **/api/birds**  
    Get list of supported species  
    Example request:
    ```http request
    GET http://localhost:5000/api/birds
    ```
    Example response:
    ```json
    {
      "species": [
        "ardea_alba",
        "ciconia_ciconia"
      ]
    }
    ```

2. **/api/birds/<specie_name>**  
    Get information about desired specie identified by <specie_name>   
    Example request:
    ```http request
    GET http://localhost:5000/api/birds/ardea_alba
    ```
    Example response:  
    ```json
    {
      "common_name": "Great egret",
      "description": "Ardea Alba sample description",
      "habitat": "Ardea Alba sample habititat",
      "scientific_name": "Ardea alba"
    }
    ```
3. **/api/birds/<specie_name>/models**  
    Get list of models supported for specie identified by <specie_name>  
    Example request:
    ```http request
    GET http://127.0.0.1:5000/api/birds/ardea_alba/models
    ```  
    Example response:
    ```json
    {
      "supported_models": [
        "autoregression"
        ]
    }
    ```
4. **/api/birds/<specie_name>/models/<model_name>**  
    Get information about model identified by <model_name> for specie identified by <specie_name>  
    Example request:
    ```http request
    GET http://127.0.0.1:5000/api/birds/ardea_alba/models/autoregression
    ```
    Example response: 
    TODO
5. **/birds/<specie_name>/models/<model_name>/predict?from=YYYY-MM-DD&to=YYYY-MM-DD**  
    Get observation data prediction (or historical data) for specie identified by <specie_name>.  
    If specified date range contains actual data, it is returned for that period. Predictions are made for dates with no observation data.

    Request query parameters:
    - from: date in format YYYY-MM_DD - date from which data will be presented
    - to: date in format YYYY-MM-DD - date to which data will be presented
    - edge: artificial boundry date between predictions and observations
    - autoregression_order: order of autoregression used
   
    Example request:
    ```http request
    GET http://127.0.0.1:5000/api/birds/ciconia_ciconia/models/autoregression/predict?from=2020-10-25&to=2022-12-01&autoregression_order=24&edge=2022-01-01
    ```
    Example response:  
    ```json
    {
      "mae_errors": {
        "dolnośląskie": 1.54,
        "kujawsko-pomorskie": 0.77,
        "lubelskie": 2.51,
        "lubuskie": 0.74,
        "mazowieckie": 2.1,
        "małopolskie": 1.2,
        "opolskie": 2.12,
        "podkarpackie": 1.55,
        "podlaskie": 1.17,
        "pomorskie": 0.51,
        "warmińsko-mazurskie": 0.94,
        "wielkopolskie": 0.66,
        "zachodniopomorskie": 0.15,
        "łódzkie": 1.23,
        "śląskie": 0.67,
        "świętokrzyskie": 1.08
      },
      "predictions": {
        "2022-01": {
          "dolnośląskie": 0.0,
          "kujawsko-pomorskie": 0.0,
          "lubelskie": 1.0,
          "lubuskie": 0.0,
          "mazowieckie": 0.0,
          "małopolskie": 1.0,
          "opolskie": 0.0,
          "podkarpackie": 0.0,
          "podlaskie": 0.0,
          "pomorskie": 0.0,
          "warmińsko-mazurskie": 0.0,
          "wielkopolskie": 0.0,
          "zachodniopomorskie": 0.0,
          "łódzkie": 0.0,
          "śląskie": 0.0,
          "świętokrzyskie": 0.0
        },
        "2022-02": {
          "dolnośląskie": 0.43,
          "kujawsko-pomorskie": 0.09,
          "lubelskie": 0.22,
          "lubuskie": 0.35,
          "mazowieckie": 1.02,
          "małopolskie": 0.18,
          "opolskie": 0.12,
          "podkarpackie": 0.2,
          "podlaskie": 0.3,
          "pomorskie": 0.23,
          "warmińsko-mazurskie": 0.03,
          "wielkopolskie": 0.3,
          "zachodniopomorskie": 0.09,
          "łódzkie": 0.32,
          "śląskie": 0,
          "świętokrzyskie": 0.29
        },
        "2022-03": {
          "dolnośląskie": 0.65,
          "kujawsko-pomorskie": 0.01,
          "lubelskie": 0,
          "lubuskie": 0.39,
          "mazowieckie": 0.62,
          "małopolskie": 0.15,
          "opolskie": 0,
          "podkarpackie": 0.25,
          "podlaskie": 0,
          "pomorskie": 0.22,
          "warmińsko-mazurskie": 0.33,
          "wielkopolskie": 0.19,
          "zachodniopomorskie": 0.7,
          "łódzkie": 0.99,
          "śląskie": 0,
          "świętokrzyskie": 0.43
        },
        "2022-04": {
          "dolnośląskie": 1.25,
          "kujawsko-pomorskie": 0.47,
          "lubelskie": 0.78,
          "lubuskie": 0.8,
          "mazowieckie": 0.63,
          "małopolskie": 0.35,
          "opolskie": 0.32,
          "podkarpackie": 1.06,
          "podlaskie": 0.91,
          "pomorskie": 0.43,
          "warmińsko-mazurskie": 0.41,
          "wielkopolskie": 1.13,
          "zachodniopomorskie": 1.4,
          "łódzkie": 1.19,
          "śląskie": 0,
          "świętokrzyskie": 1.0
        }
      },
      "tests": {
        "2022-02": {
          "dolnośląskie": 0.0,
          "kujawsko-pomorskie": 0.0,
          "lubelskie": 0.0,
          "lubuskie": 0.0,
          "mazowieckie": 0.0,
          "małopolskie": 0.0,
          "opolskie": 0.0,
          "podkarpackie": 0.0,
          "podlaskie": 0.0,
          "pomorskie": 0.0,
          "warmińsko-mazurskie": 0.0,
          "wielkopolskie": 0.0,
          "zachodniopomorskie": 0.0,
          "łódzkie": 1.0,
          "śląskie": 0.0,
          "świętokrzyskie": 0.0
        },
        "2022-03": {
          "dolnośląskie": 3.0,
          "kujawsko-pomorskie": 1.0,
          "lubelskie": 2.25,
          "lubuskie": 1.0,
          "mazowieckie": 3.5,
          "małopolskie": 1.75,
          "opolskie": 0.0,
          "podkarpackie": 1.5,
          "podlaskie": 0.0,
          "pomorskie": 0.0,
          "warmińsko-mazurskie": 1.0,
          "wielkopolskie": 1.0,
          "zachodniopomorskie": 1.0,
          "łódzkie": 0.0,
          "śląskie": 0.0,
          "świętokrzyskie": 1.0
        },
        "2022-04": {
          "dolnośląskie": 3.08,
          "kujawsko-pomorskie": 1.7,
          "lubelskie": 5.83,
          "lubuskie": 2.07,
          "mazowieckie": 3.04,
          "małopolskie": 2.17,
          "opolskie": 6.56,
          "podkarpackie": 4.27,
          "podlaskie": 4.12,
          "pomorskie": 1.5,
          "warmińsko-mazurskie": 2.55,
          "wielkopolskie": 2.0,
          "zachodniopomorskie": 1.33,
          "łódzkie": 3.2,
          "śląskie": 2.0,
          "świętokrzyskie": 3.38
        }
      }
    }
    ```
