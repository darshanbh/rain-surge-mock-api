# API Endpoints Guide - Rain Surge Mock API

This document lists all available endpoints, their requests, responses, and supported mock scenarios for the Rain Surge Mock API service.

---

## 1. Welcome / Health Check
Check if the service is online.
* **Endpoint**: `GET /`
* **Response**:
  ```json
  {
      "service": "Rain Surge Mock API Service",
      "version": "1.0",
      "status": "online"
  }
  ```

---

## 2. Weather Simulation
* **GET `/api/weather`**
  * **Description**: Returns the currently active weather scenario data.
  * **Response**:
    ```json
    {
        "scenario": "Clear Weather",
        "precip_mm": 0.0,
        "visibility": 10.0,
        "gust_speed": 5.0,
        "severity_score": 0.0,
        "rain_surge_level": 0
    }
    ```
* **POST `/api/weather/scenario`**
  * **Description**: Updates the currently active simulated weather scenario.
  * **Request**:
    ```json
    {
        "scenario": "Heavy Rain"
    }
    ```
  * **Response**:
    ```json
    {
        "status": "success",
        "message": "Active weather scenario updated to Heavy Rain",
        "current_weather": {
            "scenario": "Heavy Rain",
            "precip_mm": 15.0,
            "visibility": 2.0,
            "gust_speed": 25.0,
            "severity_score": 4.0,
            "rain_surge_level": 3
        }
    }
    ```
  * **Supported Scenarios**: `Clear Weather`, `Drizzle`, `Light Rain`, `Moderate Rain`, `Heavy Rain`, `Extreme Rain`.

---

## 3. Failure Simulation
Trigger client-side errors, timeouts, or bad API responses by supplying the `fail` query parameter on any endpoint (demonstrated below using `/api/weather`).
* **Endpoints**: `GET /api/...`
* **Query Parameters**: `?fail=<type>`
* **Supported Failure Types**:
  * `?fail=timeout`: Returns status `408 Request Timeout`
  * `?fail=http500`: Returns status `500 Internal Server Error`
  * `?fail=http429`: Returns status `429 Too Many Requests`
  * `?fail=malformed`: Returns status `400 Bad Request` with an invalid JSON string (`malformed json string: {invalid:}`)
  * `?fail=null`: Returns status `500 Internal Server Error` with a null value object (`{"current": null}`)
  * `?fail=invalidApiKey`: Returns status `401 Unauthorized`
  * `?fail=missingApiKey`: Returns status `403 Forbidden`

---

## 4. Cache Simulation
* **GET `/api/cache`**
  * **Description**: Retrieves current cache age status, TTL and weather state.
  * **Response**:
    ```json
    {
        "scenario": "Valid Cache",
        "ttl": 15,
        "weather_state": "Light Rain",
        "cache_created_time": "2026-06-17T14:00:00Z"
    }
    ```
* **POST `/api/cache/age`**
  * **Description**: Updates the cache TTL or changes the cache scenario directly.
  * **Request Options**:
    * Option A (by age):
      ```json
      {
          "age_minutes": 29
      }
      ```
    * Option B (by scenario name):
      ```json
      {
          "scenario": "Expired Cache"
      }
      ```
  * **Response**:
    ```json
    {
        "status": "success",
        "message": "Active cache scenario updated to Cache TTL = 29",
        "current_cache": {
            "scenario": "Cache TTL = 29",
            "ttl": 29,
            "weather_state": "Moderate Rain",
            "cache_created_time": "2026-06-17T13:56:46Z"
        }
    }
    ```
  * **Supported Scenarios**: `Valid Cache`, `Expired Cache`, `Cache TTL = 29`, `Cache TTL = 30`, `Cache TTL = 31`.

---

## 5. Scheduler Simulation
* **POST `/api/scheduler/tick`**
  * **Description**: Simulates the background check scheduler running. Increases the active cache TTL by 1 minute.
  * **Response**:
    ```json
    {
        "status": "success",
        "message": "Scheduler execution tick simulated successfully",
        "timestamp": "2026-06-17T14:48:00Z",
        "logs": [
            "Incremented cache age from 15 to 16 minutes"
        ],
        "current_cache_ttl": 16
    }
    ```

---

## 6. Quotation Endpoint
* **POST `/api/quotation`**
  * **Description**: Computes a dynamic fare quotation taking active weather, zone status, and business rule overrides into consideration.
  * **Request**:
    ```json
    {
        "base_fare": 100.0,
        "zone_name": "Zone A"
    }
    ```
  * **Response**:
    ```json
    {
        "base_fare": 100.0,
        "rain_surge": 30.0,
        "total": 130.0,
        "reason": "Default behavior: Weather: Heavy Rain (Severity: 4.0) -> Surge applied",
        "active_weather": "Heavy Rain",
        "active_business_rule_scenario": null
    }
    ```

---

## 7. Orders Endpoint
* **POST `/api/orders`**
  * **Description**: Creates a mock order snapshot in memory.
  * **Request**:
    ```json
    {
        "order_id": "ORD_9999",
        "status": "Created",
        "rain_surge": 15.0
    }
    ```
* **GET `/api/orders/<order_id>`**
  * **Description**: Fetches order snapshot details.
  * **Response**:
    ```json
    {
        "order_id": "ORD_9999",
        "weather_state": "Light Rain",
        "rain_surge": 15.0,
        "order_status": "Created",
        "earnings_locked": true
    }
    ```
* **PUT `/api/orders/<order_id>/status`**
  * **Description**: Updates order status. Lock checks are performed if transitioned to `Completed`.
  * **Request**:
    ```json
    {
        "status": "Completed"
    }
    ```

---

## 8. Earnings & Reports Scenarios
* **GET `/api/earnings`**
  * **Description**: Returns agent earnings records. Support filter by `?scenario=Single Rain Order`.
* **GET `/api/reports`**
  * **Description**: Returns mock reconciliation data. Support filter by `?scenario=Rain Surge Discrepancy Check`.

---

## 9. Agent App UI Status
* **GET `/api/app-status`**
  * **Description**: Retrieves visual UI cues and state mappings for the Agent App.
  * **Response**:
    ```json
    {
        "show_rain_icon": true,
        "show_raining_carousel": true,
        "weather_state": "Heavy Rain"
    }
    ```

---

## 10. Business Rules Controller
* **GET `/api/business-rules`**
  * **Description**: Retrieves all configured business rule overrides.
* **POST `/api/business-rules/scenario`**
  * **Description**: Activates a business rule override scenario to check edge cases.
  * **Request**:
    ```json
    {
        "scenario_id": "Scenario 1"
    }
    ```

---

## 11. Scenario Reset
* **POST `/api/scenario/reset`**
  * **Description**: Resets all state values back to original defaults.
  * **Response**:
    ```json
    {
        "status": "success",
        "message": "All active mock states reset to default"
    }
    ```
