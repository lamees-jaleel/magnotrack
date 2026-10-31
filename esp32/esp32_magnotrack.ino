/*
 * ======================================================================================
 * MagnoTrack: IoT-Based Magnetic Event Logging & Activity Monitoring System
 * ======================================================================================
 * Hardware:
 *   - ESP32 Development Board (e.g., ESP32 DevKit V1)
 *   - A3144 Hall-Effect Sensor Module (HW-477 with onboard LM393 comparator)
 *   - Two Small Permanent Magnets (Neodymium or Ferrite)
 *
 * Pin Connections:
 *   - HW-477 VCC  -> ESP32 3.3V (or 5V; 3.3V recommended for logic level safety)
 *   - HW-477 GND  -> ESP32 GND
 *   - HW-477 DO   -> ESP32 GPIO 27 (configured with INPUT_PULLUP)
 *   - HW-477 AO   -> Not Connected (A3144 is a digital switch, not an analog sensor)
 *
 * Sensor Behavior:
 *   - A3144 is active LOW: DO = LOW when South magnetic pole is present.
 *   - DO = HIGH when no magnetic field is detected.
 *   - Interrupt triggered on FALLING edge increments cumulative event count.
 *   - 50ms software debounce suppresses mechanical/magnetic bounce.
 * ======================================================================================
 */

#include <WiFi.h>
#include <HTTPClient.h>
#include <WiFiClientSecure.h>

// ======================================================================================
// 1. CONFIGURATION PARAMETERS (EDIT THESE FOR YOUR SETUP)
// ======================================================================================

// Wi-Fi or Mobile Hotspot Credentials
// (e.g. Android Mobile Hotspot)
const char* WIFI_SSID     = "YOUR_WIFI_OR_HOTSPOT_NAME";
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";

/*
 * Backend API Endpoint:
 * 
 * FOR RENDER PRODUCTION DEPLOYMENT:
 * Enter your Render Web Service URL with "/api/sensor-data" appended.
 * Example: "https://magnotrack.onrender.com/api/sensor-data"
 *
 * FOR LOCAL DEVELOPMENT:
 * Enter your computer's local LAN IP address and port 8000.
 * Example: "http://192.168.1.105:8000/api/sensor-data"
 * (Note: Do NOT use "localhost" or "127.0.0.1" here, as that points to the ESP32 itself)
 */
const char* API_URL = "https://YOUR-APP-NAME.onrender.com/api/sensor-data";

// Device & Sensor Hardware Pins
const char* DEVICE_ID            = "magnotrack-01";
const int   SENSOR_PIN           = 27;    // GPIO 27 connected to HW-477 DO pin
const unsigned long TRANSMIT_INTERVAL_MS = 2000;  // Send telemetry every 2 seconds
const unsigned long DEBOUNCE_DELAY_US    = 50000; // 50ms debounce window

// ======================================================================================
// 2. GLOBAL VARIABLES & INTERRUPT SERVICE ROUTINE (ISR)
// ======================================================================================

volatile unsigned long cumulativeEvents = 0;
volatile unsigned long lastDebounceMicros = 0;
portMUX_TYPE isrMux = portMUX_INITIALIZER_UNLOCKED;

unsigned long lastTransmitMillis = 0;

// Interrupt Service Routine: increments cumulative event count on magnetic field trigger
void IRAM_ATTR onMagnetDetectedISR() {
  unsigned long currentMicros = micros();
  // 50,000 microseconds = 50ms software debounce
  if (currentMicros - lastDebounceMicros >= DEBOUNCE_DELAY_US) {
    portENTER_CRITICAL_ISR(&isrMux);
    cumulativeEvents++;
    lastDebounceMicros = currentMicros;
    portEXIT_CRITICAL_ISR(&isrMux);
  }
}

// Safely read cumulative event count from ISR variable
unsigned long getEventCountSafe() {
  unsigned long count;
  portENTER_CRITICAL(&isrMux);
  count = cumulativeEvents;
  portEXIT_CRITICAL(&isrMux);
  return count;
}

// ======================================================================================
// 3. WI-FI MANAGEMENT
// ======================================================================================

void connectWiFi() {
  if (WiFi.status() == WL_CONNECTED) return;

  Serial.println();
  Serial.println("==================================================");
  Serial.print("Connecting to Wi-Fi: ");
  Serial.println(WIFI_SSID);

  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  unsigned long startAttempt = millis();
  int dots = 0;

  // Timeout after 25 seconds of connection attempts
  while (WiFi.status() != WL_CONNECTED && millis() - startAttempt < 25000) {
    delay(500);
    Serial.print(".");
    dots++;
    if (dots % 40 == 0) Serial.println();
  }

  Serial.println();
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println(">>> Wi-Fi Connected Successfully!");
    Serial.print(">>> IP Assigned: ");
    Serial.println(WiFi.localIP());
    Serial.print(">>> Signal Strength (RSSI): ");
    Serial.print(WiFi.RSSI());
    Serial.println(" dBm");
  } else {
    Serial.println(">>> [WARNING] Wi-Fi connection timed out!");
    Serial.println(">>> Please verify SSID and password, and ensure 2.4 GHz band is enabled.");
  }
  Serial.println("==================================================");
}

// ======================================================================================
// 4. HTTP TELEMETRY TRANSMISSION
// ======================================================================================

void sendTelemetry() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("[HTTP] Wi-Fi not connected. Attempting reconnection...");
    connectWiFi();
    if (WiFi.status() != WL_CONNECTED) {
      Serial.println("[HTTP] Skipping transmission: No network connection.");
      return;
    }
  }

  // 1. Snapshot current hardware states
  unsigned long countSnapshot = getEventCountSafe();
  // HW-477 DO goes LOW when magnetic field is detected
  bool magnetDetected = (digitalRead(SENSOR_PIN) == LOW);
  unsigned long uptimeMs = millis();

  // 2. Build JSON payload string
  // Format: {"device_id":"magnotrack-01","event_count":12,"magnet_detected":true,"uptime_ms":120000}
  String payload = "{";
  payload += "\"device_id\":\"" + String(DEVICE_ID) + "\",";
  payload += "\"event_count\":" + String(countSnapshot) + ",";
  payload += "\"magnet_detected\":" + String(magnetDetected ? "true" : "false") + ",";
  payload += "\"uptime_ms\":" + String(uptimeMs);
  payload += "}";

  // 3. Initialize HTTP / HTTPS client
  HTTPClient http;
  bool isHttps = String(API_URL).startsWith("https://");

  if (isHttps) {
    // For Render HTTPS deployment: use WiFiClientSecure with certificate validation bypassed
    WiFiClientSecure secureClient;
    secureClient.setInsecure(); // Allows connection to Render's Let's Encrypt SSL
    http.begin(secureClient, API_URL);
  } else {
    // For local HTTP development
    WiFiClient plainClient;
    http.begin(plainClient, API_URL);
  }

  http.addHeader("Content-Type", "application/json");
  http.setTimeout(8000); // 8 second network timeout

  Serial.print("[HTTP POST] Sending payload: ");
  Serial.println(payload);

  int httpResponseCode = http.POST(payload);

  if (httpResponseCode > 0) {
    Serial.printf("[HTTP] Response Status: %d\n", httpResponseCode);
    if (httpResponseCode == 200 || httpResponseCode == 201) {
      Serial.println("[HTTP] Telemetry recorded successfully by MagnoTrack backend.");
    } else {
      String responseBody = http.getString();
      Serial.printf("[HTTP] Server Message: %s\n", responseBody.c_str());
    }
  } else {
    Serial.printf("[HTTP ERROR] POST failed: %s (code %d)\n",
      http.errorToString(httpResponseCode).c_str(), httpResponseCode);
    Serial.println("  -> Check if API_URL is reachable and server is running.");
  }

  http.end();
}

// ======================================================================================
// 5. SETUP & MAIN LOOP
// ======================================================================================

void setup() {
  Serial.begin(115200);
  delay(1000);

  Serial.println("\n");
  Serial.println("##################################################");
  Serial.println("# MagnoTrack: ESP32 IoT Magnetic Event Monitor   #");
  Serial.println("##################################################");

  // Configure A3144 Hall-Effect Sensor Pin
  // Internal pullup ensures HIGH state when magnet is away
  pinMode(SENSOR_PIN, INPUT_PULLUP);

  // Attach interrupt for real-time edge counting
  attachInterrupt(digitalPinToInterrupt(SENSOR_PIN), onMagnetDetectedISR, FALLING);
  Serial.printf("[HARDWARE] Sensor configured on GPIO %d (FALLING interrupt attached)\n", SENSOR_PIN);

  // Initial Wi-Fi connection
  connectWiFi();

  Serial.println("[SYSTEM] Setup completed. Entering telemetry loop...\n");
}

void loop() {
  // Check Wi-Fi connection and reconnect if lost
  if (WiFi.status() != WL_CONNECTED) {
    connectWiFi();
  }

  // Periodic telemetry transmission
  unsigned long now = millis();
  if (now - lastTransmitMillis >= TRANSMIT_INTERVAL_MS) {
    lastTransmitMillis = now;
    sendTelemetry();
  }

  // Small delay to yield to ESP32 RTOS background tasks
  delay(10);
}
