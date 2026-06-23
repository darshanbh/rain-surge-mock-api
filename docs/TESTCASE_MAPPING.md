# Test Case Mapping - Rain Surge Mock API

This document maps every single test case ID from the workbook `Rain_Surge_Testcases-Web-App.xlsx` to its corresponding JSON data source, scenario name, and test endpoint for the Rain Surge Mock API.

---

## Mapped Test Cases

### Admin Test Cases (TS_RS_001 to TS_RS_029)

| Test Case ID | JSON Data Source | Scenario Name / Input | Endpoint / Method |
| :--- | :--- | :--- | :--- |
| **TS_RS_001** | `weather.json` | Clear Weather | `GET /api/weather` |
| **TS_RS_002** | `weather.json` | Clear Weather | `GET /api/weather` |
| **TS_RS_003** | `weather.json` | Drizzle | `GET /api/weather` |
| **TS_RS_004** | `weather.json` | Light Rain | `GET /api/weather` |
| **TS_RS_005** | `zones.json` | Zone A | `POST /api/quotation` |
| **TS_RS_006** | `zones.json` | Zone A | `POST /api/quotation` |
| **TS_RS_007** | `quotations.json` | Rain Enabled Quote | `POST /api/quotation` |
| **TS_RS_008** | `quotations.json` | Rain Enabled Quote | `POST /api/quotation` |
| **TS_RS_009** | `quotations.json` | Rain Enabled Quote | `POST /api/quotation` |
| **TS_RS_010** | `quotations.json` | Rain Disabled Quote | `POST /api/quotation` |
| **TS_RS_011** | `orders.json` | Created Order | `GET /api/orders/<id>` |
| **TS_RS_012** | `zones.json` | Zone B | `POST /api/quotation` |
| **TS_RS_013** | `orders.json` | Accepted Order | `GET /api/orders/<id>` |
| **TS_RS_014** | `orders.json` | Completed Order | `GET /api/orders/<id>` |
| **TS_RS_015** | `boundaries.json` | 0.49 | `POST /api/quotation` |
| **TS_RS_016** | `boundaries.json` | 0.50 | `POST /api/quotation` |
| **TS_RS_017** | `boundaries.json` | 0.51 | `POST /api/quotation` |
| **TS_RS_018** | `boundaries.json` | 2.49 | `POST /api/quotation` |
| **TS_RS_019** | `boundaries.json` | 2.50 | `POST /api/quotation` |
| **TS_RS_020** | `boundaries.json` | 2.51 | `POST /api/quotation` |
| **TS_RS_021** | `cache.json` | Valid Cache | `GET /api/cache` |
| **TS_RS_022** | `cache.json` | Expired Cache | `GET /api/cache` |
| **TS_RS_023** | `cache.json` | Valid Cache | `GET /api/cache` |
| **TS_RS_024** | `quotations.json` | Rain Disabled Quote | `POST /api/quotation` |
| **TS_RS_025** | `reports.json` | Rain Surge Discrepancy Check | `GET /api/reports` |
| **TS_RS_026** | `settlements.json` | Standard Rain Surge Settlement | `GET /api/reports` |
| **TS_RS_027** | `earnings.json` | Single Rain Order | `GET /api/earnings` |
| **TS_RS_028** | `zones.json` | Cell A | `POST /api/quotation` |
| **TS_RS_029** | `settlements.json` | Multiple Rain Orders | `GET /api/reports` |

---

### Backend API Test Cases (TS_RS_API_001 to TS_RS_API_015)

| Test Case ID | JSON Data Source | Scenario Name / Input | Endpoint / Method |
| :--- | :--- | :--- | :--- |
| **TS_RS_API_001** | `failures.json` | API Timeout | `GET /api/weather?fail=timeout` |
| **TS_RS_API_002** | `failures.json` | HTTP 500 | `GET /api/weather?fail=http500` |
| **TS_RS_API_003** | `failures.json` | HTTP 429 | `GET /api/weather?fail=http429` |
| **TS_RS_API_004** | `failures.json` | Malformed JSON | `GET /api/weather?fail=malformed` |
| **TS_RS_API_005** | `failures.json` | Null Current Object | `GET /api/weather?fail=null` |
| **TS_RS_API_006** | `weather.json` | Clear Weather | `POST /api/weather/scenario` |
| **TS_RS_API_007** | `weather.json` | Drizzle | `POST /api/weather/scenario` |
| **TS_RS_API_008** | `weather.json` | Heavy Rain | `POST /api/weather/scenario` |
| **TS_RS_API_009** | `zones.json` | Zone A | `POST /api/quotation` |
| **TS_RS_API_010** | `cache.json` | Valid Cache | `GET /api/cache` |
| **TS_RS_API_011** | `cache.json` | Expired Cache | `GET /api/cache` |
| **TS_RS_API_012** | `weather.json` | Heavy Rain | `GET /api/weather` |
| **TS_RS_API_013** | `weather.json` | Extreme Rain | `GET /api/weather` |
| **TS_RS_API_014** | `failures.json` | Invalid API Key | `GET /api/weather?fail=invalidApiKey` |
| **TS_RS_API_015** | `failures.json` | Missing API Key | `GET /api/weather?fail=missingApiKey` |

---

### End-to-End (E2E) Test Cases (TS_RS_E2E_001 to TS_RS_E2E_016)

| Test Case ID | JSON Data Source | Scenario Name / Input | Endpoint / Method |
| :--- | :--- | :--- | :--- |
| **TS_RS_E2E_001** | `weather.json` | Clear Weather | `GET /api/weather` |
| **TS_RS_E2E_002** | `weather.json` | Heavy Rain | `GET /api/weather` |
| **TS_RS_E2E_003** | `cache.json` | Expired Cache | `GET /api/cache` |
| **TS_RS_E2E_004** | `orders.json` | Created Order | `POST /api/orders` |
| **TS_RS_E2E_005** | `cache.json` | Valid Cache | `GET /api/cache` |
| **TS_RS_E2E_006** | `failures.json` | HTTP 500 | `GET /api/weather?fail=http500` |
| **TS_RS_E2E_007** | `business_rules.json` | Scenario Reset | `POST /api/scenario/reset` |
| **TS_RS_E2E_008** | `reports.json` | Rain Surge Discrepancy Check | `GET /api/reports` |
| **TS_RS_E2E_009** | `cache.json` | Valid Cache | `POST /api/cache/age` |
| **TS_RS_E2E_010** | `cache.json` | Valid Cache | `POST /api/scheduler/tick` |
| **TS_RS_E2E_011** | `business_rules.json` | Scenario 1 | `POST /api/business-rules/scenario` |
| **TS_RS_E2E_012** | `business_rules.json` | Scenario 2 | `POST /api/business-rules/scenario` |
| **TS_RS_E2E_013** | `business_rules.json` | Scenario 3 | `POST /api/business-rules/scenario` |
| **TS_RS_E2E_014** | `zones.json` | Zone A | `POST /api/quotation` |
| **TS_RS_E2E_015** | `zones.json` | Zone B | `POST /api/quotation` |
| **TS_RS_E2E_016** | `business_rules.json` | Scenario 4 | `POST /api/business-rules/scenario` |

---

### Agent App UI & Logic Test Cases (TS_RS_APP_001 to TS_RS_APP_014)

| Test Case ID | JSON Data Source | Scenario Name / Input | Endpoint / Method |
| :--- | :--- | :--- | :--- |
| **TS_RS_APP_001** | `app_ui.json` | Rain Zone | `GET /api/app-status` |
| **TS_RS_APP_002** | `app_ui.json` | Clear Zone | `GET /api/app-status` |
| **TS_RS_APP_003** | `app_ui.json` | Rain Zone | `GET /api/app-status` |
| **TS_RS_APP_004** | `app_ui.json` | Rain Zone | `GET /api/app-status` |
| **TS_RS_APP_005** | `app_ui.json` | Clear Zone | `GET /api/app-status` |
| **TS_RS_APP_006** | `app_earnings.json` | Single Order Earning | `GET /api/earnings` |
| **TS_RS_APP_007** | `app_ui.json` | Clear Zone | `GET /api/app-status` |
| **TS_RS_APP_008** | `app_ui.json` | Clear Zone | `GET /api/app-status` |
| **TS_RS_APP_009** | `app_ui.json` | Rain Zone | `GET /api/app-status` |
| **TS_RS_APP_010** | `app_earnings.json` | High Surge Order Earning | `GET /api/earnings` |
| **TS_RS_APP_011** | `app_business_logic.json` | Agent in Rain Zone, Pickup in Rain Zone | `POST /api/quotation` |
| **TS_RS_APP_012** | `app_business_logic.json` | Agent in Clear Zone, Pickup in Clear Zone | `POST /api/quotation` |
| **TS_RS_APP_013** | `app_business_logic.json` | Agent in Clear Zone, Pickup in Rain Zone | `POST /api/quotation` |
| **TS_RS_APP_014** | `app_business_logic.json` | Agent in Rain Zone, Pickup in Clear Zone | `POST /api/quotation` |

---

### Agent App Deep Test Cases (TS_RS_APP_DEEP_011, TS_RS_APP_DEEP_012)

| Test Case ID | JSON Data Source | Scenario Name / Input | Endpoint / Method |
| :--- | :--- | :--- | :--- |
| **TS_RS_APP_DEEP_011**| `business_rules.json` | Scenario 5 | `POST /api/business-rules/scenario` |
| **TS_RS_APP_DEEP_012**| `app_earnings.json` | High Surge Order Earning | `GET /api/earnings` |
