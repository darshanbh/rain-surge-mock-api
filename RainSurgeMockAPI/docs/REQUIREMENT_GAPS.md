# Requirement Gaps & Product Confirmations

This document tracks all unresolved business rules and pending product confirmations for the Rain Surge feature. In the mock API service, we have implemented reasonable default assumptions to allow testing to continue, but these require final approval from the Product team.

---

## Gap 1: TS_RS_E2E_011 (Scenario 1)
* **Condition**: Active Agents in Zone = 0, Cache Expired
* **Pending Product Confirmation**: What should the system fallback behavior be when there is no fresh weather data (cache expired) and there are no active agents to fetch weather updates?
  * **Option A**: Use last known weather (stale data).
  * **Option B**: Use fallback default weather.
  * **Option C**: Do not apply any Rain Surge.
* **Mock Service Implementation**: Currently defaults to **Option C** (Rain Surge = 0), but supports configuring/testing other scenarios dynamically via the API.

---

## Gap 2: TS_RS_E2E_012 (Scenario 2)
* **Condition**: New Zone, No Cache, No Agents
* **Pending Product Confirmation**: When a zone is brand new (no cache exists yet) and has no agents active:
  * **Option A**: Generate quotation and set Rain Surge = 0.
  * **Option B**: Block quotation generation entirely.
* **Mock Service Implementation**: Currently defaults to **Option A** (Generate quotation, Rain Surge = 0).

---

## Gap 3: TS_RS_E2E_013 (Scenario 3)
* **Condition**: Rain exists at the time of quotation, but weather clears up before order completion.
* **Pending Product Confirmation**: Which rain surge pricing policy should apply to the agent's earnings?
  * **Option A**: Locked earnings (retains the rain surge computed at quotation time).
  * **Option B**: Recalculated earnings (surge removed/recalculated based on completion time weather).
* **Mock Service Implementation**: Currently defaults to **Option A** (Earnings locked at quotation time).

---

## Gap 4: TS_RS_E2E_016 (Scenario 4)
* **Condition**: Cell becomes inactive, Cache is expired, and no refresh is possible.
* **Pending Product Confirmation**: What weather state should be served when a cell goes inactive and the cache is expired?
  * **Option A**: Use fallback default weather.
  * **Option B**: Use last known weather.
* **Mock Service Implementation**: Currently defaults to **Option A** (Use fallback weather / Rain Surge = 0).

---

## Gap 5: TS_RS_APP_DEEP_011 (Scenario 5)
* **Condition**: Cache age boundaries (29 min, 30 min, 31 min)
* **Pending Product Confirmation**: Verify exact cache age transition limits:
  * 29 min = Valid (Apply Rain Surge)
  * 30 min = Boundary limit (Confirm if it counts as valid or expired)
  * 31 min = Expired (Do not apply Rain Surge)
* **Mock Service Implementation**:
  * 29 min -> Valid (Surge applied)
  * 30 min -> Boundary limit (Surge applied)
  * >= 31 min -> Expired (No surge applied)
