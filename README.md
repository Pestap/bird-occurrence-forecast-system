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
4. **/api/birds/<specie_name>/models/<model>**  
    Get information about model identified by <model> for specie identified by <specie_name>  
    Example request:
    ```http request
    GET http://127.0.0.1:5000/api/birds/ardea_alba/models/autoregression
    ```
    Example response: 
    TODO
5. **/birds/<specie_name>/models/<model>/predict?from=YYYY-MM-DD&to=YYYY-MM-DD**  
    Get observation data prediction (or historical data) for specie identified by <specie_name>.  
    If specified date range contains actual data, it is returned for that period. Predictions are made for dates with no observation data.  
    Example request:
    ```http request
    GET http://127.0.0.1:5000/api/birds/ardea_alba/models/autoregression/predict?from=2011-10-25&to=2013-10-25
    ```
    Example response:  
    TODO
