# COVID-19 PH Tracker
![GitHub](https://img.shields.io/github/license/kvdomingo/covid19-ph-web?style=flat-square)
![GitHub last commit](https://img.shields.io/github/last-commit/kvdomingo/covid19-ph-web?style=flat-square)

## API Endpoints

**Base URL**: https://ncovenience.herokuapp.com/api

**Format**: JSON/GeoJSON



- `GET` /

    Returns the name of the API.
    ```
    > curl -X GET https://ncovenience.herokuapp.com/api
    ```

- `GET` /cases

    Returns data for all PH cases.
    ```
    > curl -X GET https://ncovenience.herokuapp.com/api/cases
    ```

- `GET` /numbers

    Returns numbers of confirmed, recovered, and deceased cases.
    ```
    > curl -X GET https://ncovenience.herokuapp.com/api/numbers
    ```