# Rain Surge Mock API Service

This is a QA/Test Mock Service designed to support Admin, Backend API, E2E, and Agent App testing for the **Rain Surge** feature. It simulates weather transitions, boundary values, API failures, cache lifetimes, and product business rule scenarios.

---

## 1. Quick Start / Running Locally

### Prerequisites
* Python 3.10+ installed

### Installation & Execution
1. Navigate to the project root directory:
   ```bash
   cd RainSurgeMockAPI
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the mock API service:
   ```bash
   python app.py
   ```
   The service will start running on **`http://127.0.0.1:5000`**.

---

## 2. Sample API Requests & Scenarios

### Reset Mock State (E2E Scenario Reset)
Reset all in-memory states (weather, cache, zones, business rules, active orders) to defaults.
* **Endpoint**: `POST /api/scenario/reset`
* **cURL Command**:
  ```bash
  curl -X POST http://127.0.0.1:5000/api/scenario/reset
  ```

### Switch Weather Scenario (Moderate Rain)
* **Endpoint**: `POST /api/weather/scenario`
* **cURL Command**:
  ```bash
  curl -X POST http://127.0.0.1:5000/api/weather/scenario \
       -H "Content-Type: application/json" \
       -d '{"scenario": "Moderate Rain"}'
  ```

### Simulate Cache Invalidation (Set TTL = 31 Minutes)
* **Endpoint**: `POST /api/cache/age`
* **cURL Command**:
  ```bash
  curl -X POST http://127.0.0.1:5000/api/cache/age \
       -H "Content-Type: application/json" \
       -d '{"age_minutes": 31}'
  ```

### Trigger Failure Simulation (Internal Server Error)
Append the `fail` query parameter to simulate API exceptions.
* **Endpoint**: `GET /api/weather?fail=http500`
* **cURL Command**:
  ```bash
  curl http://127.0.0.1:5000/api/weather?fail=http500
  ```

### Generate Quotation (With Heavy Rain Surge)
1. Set active weather to Heavy Rain:
   ```bash
   curl -X POST http://127.0.0.1:5000/api/weather/scenario \
        -H "Content-Type: application/json" \
        -d '{"scenario": "Heavy Rain"}'
   ```
2. Get Fare Quotation:
   ```bash
   curl -X POST http://127.0.0.1:5000/api/quotation \
        -H "Content-Type: application/json" \
        -d '{"base_fare": 100.0, "zone_name": "Zone A"}'
   ```

---

## 3. Documentation Reference
Refer to the following files in the `docs/` folder for comprehensive documentation:
* [API Endpoints Guide](docs/API_ENDPOINTS.md): Listing of all available methods, shapes, and responses.
* [Test Case Mapping](docs/TESTCASE_MAPPING.md): Exact cross-reference table mapping the workbook's 76 testcase IDs to API calls.
* [Coverage Report](docs/COVERAGE_REPORT.md): Summary of test coverage across categories.
* [Requirement Gaps & Confirmations](docs/REQUIREMENT_GAPS.md): Track list of pending confirmations from Product.
