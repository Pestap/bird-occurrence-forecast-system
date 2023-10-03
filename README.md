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
    Get information about specified specie  
    Example request:
    ```http request
    GET http://localhost:5000/api/birds/ardea_alba
    ```

