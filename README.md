# COVID-19 PH Tracker

## API Endpoints

**Base URL**: https://ncovenience.herokuapp.com/api

**Format**: JSON/GeoJSON

---

- `GET /`

    Returns the name of the API.
    ```
    > curl -X https://ncovenience.herokuapp.com/api
    ```
---
- `GET /health`

    Check the health/uptime of the API.
    ```
    > curl -X https://ncovenience.herokuapp.com/api/health
    ```
---
- `GET /cases`

    Returns data for all PH cases.
    ```
    > curl -X https://ncovenience.herokuapp.com/api/cases
    ```
---
- `GET /hospitals`

    Returns cases for hospitals/medical facilities.
    ```
    > curl -X https://ncovenience.herokuapp.com/api/hospitals
    ```
