# MagnoTrack – IoT-Based Magnetic Event Logging & Activity Monitoring System

[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![Render](https://img.shields.io/badge/Deploy-Render-46E3B7?style=flat&logo=render&logoColor=white)](https://render.com)
[![ESP32](https://img.shields.io/badge/Hardware-ESP32%20+%20A3144-E7352C?style=flat&logo=espressif&logoColor=white)](https://www.espressif.com/)

**MagnoTrack** is an industrial-grade, academic IoT monitoring system designed to log, analyze, and visualize magnetic events in real time. It pairs an **ESP32 microcontroller** and an **A3144 Hall-effect sensor module (HW-477)** with a modern **FastAPI** backend, **PostgreSQL** database, and a responsive **Chart.js** dashboard.

---

## Table of Contents

1. [Hardware Architecture & Wiring](#1-hardware-architecture--wiring)
2. [Project File Structure](#2-project-file-structure)
3. [Quick Start: Local Development with Docker Compose](#3-quick-start-local-development-with-docker-compose)
4. [Deploying to Render (Cloud Web Service & PostgreSQL)](#4-deploying-to-render-cloud-web-service--postgresql)
5. [Configuring and Flashing the ESP32](#5-configuring-and-flashing-the-esp32)
6. [API Reference & Manual Testing](#6-api-reference--manual-testing)
7. [Dashboard Features & Behavioral Rules](#7-dashboard-features--behavioral-rules)
8. [Troubleshooting & FAQ](#8-troubleshooting--faq)

---

## 1. Hardware Architecture & Wiring

The hardware consists of an ESP32 development board, an **A3144 Hall-effect sensor module (HW-477)**, and two small permanent magnets.

### Sensor Working Principle
The A3144 module is a **digital magnetic switch** (integrated with an onboard LM393 comparator and status LED).
- **Idle State:** When no magnetic field is present, the digital output (**DO**) is pulled **HIGH**.
- **Active State:** When the **South pole** of a magnet approaches within 5–10 mm, the internal transistor switches on, pulling **DO** to **LOW**.
- **Event Detection:** The ESP32 attaches an interrupt to the **FALLING** edge with a 50 ms debounce delay, incrementing a cumulative counter in memory.
- *Note:* The sensor is a digital on/off trigger, not an analog magnetic flux sensor.

### Pinout Connection Table

| A3144 Module (HW-477) Pin | ESP32 DevKit Pin | Wire Color (Recommended) | Description |
| :--- | :--- | :--- | :--- |
| **VCC** | **3.3V** | Red | 3.3V DC Power (Matches ESP32 logic level) |
| **GND** | **GND** | Black | Ground |
| **DO (Digital Out)** | **GPIO 27** | Yellow / Blue | Active-LOW digital signal (Configured with `INPUT_PULLUP`) |
| **AO (Analog Out)** | *Not Connected* | &mdash; | Unused (Module is operated as a digital switch) |

> **Wiring Tip:** Ensure VCC is connected to the ESP32's **3.3V** pin (not 5V) to ensure the sensor's output logic voltage does not exceed 3.3V, safeguarding the ESP32 GPIO.

---

## 2. Project File Structure

```text
magnotrack/
├── app/
│   ├── main.py              # FastAPI application setup, CORS, lifespan, and routing
│   ├── database.py          # SQLAlchemy engine, connection pooling, and auto table creation
│   ├── models.py            # PostgreSQL SensorReading ORM model
│   ├── schemas.py           # Pydantic validation schemas for ingest and responses
│   ├── routes.py            # REST API endpoints (/sensor-data, /latest, /stats, /history, etc.)
│   ├── templates/
│   │   └── index.html       # Modern industrial IoT dashboard markup
│   └── static/
│       ├── style.css        # Dark navy/charcoal responsive CSS with glowing accents
│       └── dashboard.js     # Live auto-refresh, Chart.js instances, and history pagination
├── esp32/
│   └── esp32_magnotrack.ino # Arduino C++ firmware for ESP32 with Wi-Fi & HTTPClient
├── tests/
│   └── test_api.py          # Pytest automated test suite (7 unit & integration tests)
├── Dockerfile               # Production multi-stage Docker build for Render
├── docker-compose.yml       # Local development setup with PostgreSQL 16 container
├── requirements.txt         # Python package dependencies
├── .env.example             # Template environment variables
├── .gitignore               # Git ignore rules for Python, Docker, and IDE files
└── README.md                # Comprehensive documentation
```

---

## 3. Quick Start: Local Development with Docker Compose

To test the complete stack locally with a real PostgreSQL database:

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.

### 1. Clone or Open the Project
Open a terminal in the project directory:
```bash
cd "C:\Users\USER\OneDrive\Desktop\IOT Project"
```

### 2. Launch the Stack
Run Docker Compose:
```bash
docker compose up --build
```
This will:
1. Spin up a **PostgreSQL 16** container (`magnotrack_postgres`) with a healthcheck.
2. Build the **FastAPI** container (`magnotrack_api`) and wait until PostgreSQL is healthy.
3. Automatically create the `sensor_readings` table.
4. Expose the web dashboard at `http://localhost:8000`.

### 3. Open the Dashboard
Open your web browser and navigate to:
```text
http://localhost:8000
```
You will see the MagnoTrack dashboard showing **"WAITING FOR DATA"** until the first sensor reading is sent.

---

## 4. Deploying to Render (Cloud Web Service & PostgreSQL)

Deploying MagnoTrack to [Render](https://render.com) takes less than 5 minutes.

### Step 1: Push Your Code to GitHub / GitLab
Create a new GitHub repository (e.g. `magnotrack`) and push your project files:
```bash
git init
git add .
git commit -m "Initial commit of MagnoTrack IoT system"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/magnotrack.git
git push -u origin main
```

### Step 2: Create a PostgreSQL Database on Render
1. Log in to your [Render Dashboard](https://dashboard.render.com/).
2. Click **New +** &rarr; Select **PostgreSQL**.
3. Fill in the database details:
   - **Name:** `magnotrack-db`
   - **Database:** `magnotrack_db`
   - **User:** `magnotrack_user`
   - **Region:** Choose the region closest to you (e.g. Oregon, Frankfurt, Singapore).
   - **Instance Type:** **Free**.
4. Click **Create Database**.
5. Once created, locate the **Internal Database URL** (e.g., `postgres://magnotrack_user:...@dpg-xxx:5432/magnotrack_db`). Copy this URL.

### Step 3: Create the FastAPI Web Service on Render
1. In the Render Dashboard, click **New +** &rarr; Select **Web Service**.
2. Connect your GitHub repository (`magnotrack`).
3. Configure the service:
   - **Name:** `magnotrack` (this gives you `https://magnotrack.onrender.com`).
   - **Language:** **Docker**.
   - **Region:** Select the **same region** as your database.
   - **Branch:** `main`.
   - **Instance Type:** **Free**.
4. Scroll down to **Environment Variables** and add:
   | Key | Value |
   | :--- | :--- |
   | `DATABASE_URL` | Paste your Render PostgreSQL Database URL copied from Step 2 |
   | `CORS_ORIGINS` | `*` |
   | `DEVICE_OFFLINE_THRESHOLD_SECONDS` | `30` |
5. Click **Create Web Service**.

> **Note on Render URLs:** Render provides database connection strings beginning with `postgres://`. The MagnoTrack backend automatically handles this and converts it to `postgresql://` so SQLAlchemy and Psycopg2 connect smoothly without errors.

### Step 4: Verify Your Deployed Service
Once the build completes and status shows **Live**:
- Visit `https://YOUR-APP-NAME.onrender.com` in your browser.
- Visit `https://YOUR-APP-NAME.onrender.com/api/health` to confirm the database returns `"Database connection active"`.
- Visit `https://YOUR-APP-NAME.onrender.com/docs` to test interactive Swagger documentation.

---

## 5. Configuring and Flashing the ESP32

The ESP32 Arduino code is located at:
[`esp32/esp32_magnotrack.ino`](esp32/esp32_magnotrack.ino)

### Step 1: Open the Code in Arduino IDE
1. Open [Arduino IDE](https://www.arduino.cc/en/software) (version 2.x recommended).
2. Ensure you have the **ESP32 board package** installed:
   - Go to **Tools** &rarr; **Board** &rarr; **Boards Manager**.
   - Search for `esp32` by Espressif Systems and install it.
3. Select your board: **Tools** &rarr; **Board** &rarr; **esp32** &rarr; **ESP32 Dev Module** (or your specific model).
4. Select the correct **COM Port** under **Tools** &rarr; **Port**.

### Step 2: Configure Your Wi-Fi & Render URL
Open `esp32/esp32_magnotrack.ino` and locate the configuration section at lines 35–56:

```cpp
// ======================================================================================
// 1. CONFIGURATION PARAMETERS (EDIT THESE FOR YOUR SETUP)
// ======================================================================================

// Wi-Fi or Mobile Hotspot Credentials
const char* WIFI_SSID     = "YOUR_HOTSPOT_NAME";     // <-- Enter your hotspot/Wi-Fi SSID
const char* WIFI_PASSWORD = "YOUR_HOTSPOT_PASSWORD"; // <-- Enter your Wi-Fi password

/*
 * Backend API Endpoint:
 * 
 * FOR RENDER PRODUCTION DEPLOYMENT:
 * Enter your Render Web Service URL with "/api/sensor-data" appended.
 * Example: "https://magnotrack.onrender.com/api/sensor-data"
 */
const char* API_URL = "https://magnotrack.onrender.com/api/sensor-data"; // <-- REPLACE WITH YOUR RENDER URL

const char* DEVICE_ID            = "magnotrack-01";
const int   SENSOR_PIN           = 27;    // GPIO 27 connected to HW-477 DO pin
const unsigned long TRANSMIT_INTERVAL_MS = 2000;  // Send telemetry every 2 seconds
```

### Step 3: Flash the Code
1. Click the **Upload** button (right arrow icon) in Arduino IDE.
2. If the upload stalls at `Connecting........_____`, press and hold the **BOOT** button on the ESP32 board until the flashing progress starts.
3. Open the **Serial Monitor** at **115200 baud** (`Ctrl + Shift + M`).

### Expected Serial Monitor Output:
```text
##################################################
# MagnoTrack: ESP32 IoT Magnetic Event Monitor   #
##################################################
[HARDWARE] Sensor configured on GPIO 27 (FALLING interrupt attached)

Connecting to Wi-Fi: iQOO Neo9 Pro
.........
>>> Wi-Fi Connected Successfully!
>>> IP Assigned: 192.168.43.150
>>> Signal Strength (RSSI): -48 dBm
==================================================
[SYSTEM] Setup completed. Entering telemetry loop...

[HTTP POST] Sending payload: {"device_id":"magnotrack-01","event_count":0,"magnet_detected":false,"uptime_ms":2150}
[HTTP] Response Status: 201
[HTTP] Telemetry recorded successfully by MagnoTrack backend.
```

---

## 6. API Reference & Manual Testing

You can simulate or test the ESP32 telemetry using `curl` or PowerShell without waiting for hardware:

### A. Test Telemetry Ingestion (Simulate Magnet Event)
**Using cURL:**
```bash
curl -X POST "http://localhost:8000/api/sensor-data" \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "magnotrack-01",
    "event_count": 1,
    "magnet_detected": true,
    "uptime_ms": 15000
  }'
```

**Using PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/sensor-data" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"device_id":"magnotrack-01","event_count":1,"magnet_detected":true,"uptime_ms":15000}'
```

**Response (HTTP 201 Created):**
```json
{
  "status": "success",
  "message": "Sensor reading recorded successfully",
  "id": 1,
  "device_id": "magnotrack-01",
  "created_at": "2026-10-31T10:55:00.123456+00:00"
}
```

### B. Summary of All REST Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/sensor-data` | Ingests `{device_id, event_count, magnet_detected, uptime_ms}` into PostgreSQL. |
| `GET` | `/api/latest` | Returns the latest recorded reading and online status. |
| `GET` | `/api/stats` | Aggregated statistics: total events, events in last 60s, device status, and latest event time. |
| `GET` | `/api/history` | Paginated records in descending chronological order (`limit`, `offset`, `device_id`). |
| `GET` | `/api/chart-data` | Formatted vectors (`labels`, `event_counts`, `activity_deltas`, `sensor_states`) for Chart.js. |
| `GET` | `/api/health` | Diagnostic health check for the web service and PostgreSQL database. |
| `GET` | `/` | Serves the single-page monitoring dashboard. |

---

## 7. Dashboard Features & Behavioral Rules

The MagnoTrack frontend is built with high-contrast industrial dark navy/charcoal styling:

1. **Total Magnetic Events:**
   - Displays cumulative hardware counts directly from the database.
   - Preserves state even if an intermediate HTTP request drops or during network reconnects.
2. **Current Sensor Status:**
   - `MAGNET DETECTED` (Glow badge with active pulse) when the sensor's DO pin is LOW.
   - `NO MAGNET` (Subtle dark badge) when idle.
3. **Events Per Minute (EPM):**
   - Automatically computes events detected within a rolling 60-second window.
   - Dynamic rating badge: `IDLE` (0), `ACTIVE` (1–15), `HIGH RATE` (>15).
4. **Device Connection:**
   - Automatically marks the ESP32 as **ONLINE** (green pulse) when data is received within 30 seconds.
   - Marks the ESP32 as **OFFLINE** (red) if no reading is received for >30 seconds.
   - Displays a warning banner indicating how long since the last heartbeat was seen.
5. **Chart.js Visualizations:**
   - **Line Chart:** Shows the cumulative progression of event counts over time.
   - **Bar & Step Chart:** Shows the activity frequency per transmission interval and active magnet states.
6. **Data Export:**
   - Includes a one-click **Export CSV** button in the Event History tab to download raw event logs.

---

## 8. Troubleshooting & FAQ

### 1. ESP32 fails to connect to Wi-Fi / Hotspot
- **Cause:** ESP32 hardware only supports **2.4 GHz Wi-Fi**.
- **Fix:** If using an Android mobile hotspot, open Hotspot Settings &rarr; **AP Band** &rarr; select **2.4 GHz Band** (not 5 GHz). Ensure SSID and password contain no unusual symbols.

### 2. ESP32 prints `[HTTP ERROR] POST failed: connection refused`
- **For Local Testing:** If running FastAPI locally, ensure the ESP32 is using your computer's LAN IP (e.g. `192.168.1.105:8000`), NOT `localhost` or `127.0.0.1`.
- **For Render:** Ensure your Render URL starts with `https://` and ends with `/api/sensor-data`. Note that Render free-tier services sleep after 15 minutes of inactivity; the first request after idle can take 30–45 seconds to wake up.

### 3. Sensor LED is always on or doesn't detect magnet
- **Hall-Effect Polarity:** The A3144 Hall-effect sensor responds specifically to the **South pole** of the magnet. If the sensor does not trigger, flip the magnet to the opposite pole.
- **Potentiometer Adjustment:** The HW-477 module has a small blue potentiometer that adjusts the LM393 comparator sensitivity threshold. Rotate it using a small screwdriver until the onboard LED turns off in the absence of a magnet and lights up when the magnet is near.

### 4. Running Automated Tests Locally
Run pytest from the project directory:
```bash
py -m pytest tests/test_api.py -v
```
All 7 unit and integration tests will verify the database operations, schema validation, calculations, and dashboard template rendering.

---

**MagnoTrack** &mdash; Developed for academic IoT project demonstration and reliable industrial magnetic event telemetry.
