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
    Example request:
    ```http request
    GET http://127.0.0.1:5000/api/birds/ardea_alba/models/autoregression/predict?from=2013-08-25&to=2013-10-25
    ```
    Example response:  
    ```json
    {
      "2013-10": {
        "DOLNOSLASKIE": 0.0,
        "KUJAWSKO_POMORSKIE": 0.0,
        "LODZKIE": 0.0,
        "LUBELSKIE": 0.0,
        "LUBUSKIE": 60.0,
        "MALOPOLSKIE": 0.0,
        "MAZOWIECKIE": 1.0,
        "OPOLSKIE": 0.0,
        "PODKARPACKIE": 0.0,
        "PODLASKIE": 0.0,
        "POMORSKIE": 0.0,
        "SLASKIE": 56.666666666666664,
        "SWIETOKRZYSKIE": 0.0,
        "WARMINSKO_MAZURSKIE": 0.0,
        "WIELKOPOLSKIE": 81.0,
        "ZACHODNIOPOMORSKIE": 0.0
      },
      "2013-8": {
        "DOLNOSLASKIE": 2.6666666666666665,
        "KUJAWSKO_POMORSKIE": 3.0,
        "LODZKIE": 0.0,
        "LUBELSKIE": 0.0,
        "LUBUSKIE": 11.333333333333334,
        "MALOPOLSKIE": 0.0,
        "MAZOWIECKIE": 0.0,
        "OPOLSKIE": 0.0,
        "PODKARPACKIE": 0.0,
        "PODLASKIE": 1.0,
        "POMORSKIE": 1.0,
        "SLASKIE": 2.0,
        "SWIETOKRZYSKIE": 0.0,
        "WARMINSKO_MAZURSKIE": 0.0,
        "WIELKOPOLSKIE": 5.0,
        "ZACHODNIOPOMORSKIE": 14.5
      },
      "2013-9": {
        "DOLNOSLASKIE": 0.0,
        "KUJAWSKO_POMORSKIE": 0.0,
        "LODZKIE": 0.0,
        "LUBELSKIE": 1.0,
        "LUBUSKIE": 5.0,
        "MALOPOLSKIE": 2.0,
        "MAZOWIECKIE": 2.0,
        "OPOLSKIE": 0.0,
        "PODKARPACKIE": 0.0,
        "PODLASKIE": 1.0,
        "POMORSKIE": 0.0,
        "SLASKIE": 5.0,
        "SWIETOKRZYSKIE": 0.0,
        "WARMINSKO_MAZURSKIE": 0.0,
        "WIELKOPOLSKIE": 1.0,
        "ZACHODNIOPOMORSKIE": 8.666666666666666
      }
    }
    ```
