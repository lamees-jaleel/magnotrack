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
 *   - HW-477 VCC  -> ESP32 3.3V (protects ESP32 GPIO logic level)
 *   - HW-477 GND  -> ESP32 GND
 *   - HW-477 DO   -> ESP32 GPIO 27 (configured with INPUT_PULLUP)
 *   - HW-477 AO   -> Not Connected (A3144 is a digital threshold switch)
 *
 * Sensor Behavior:
 *   - A3144 is active LOW: DO = LOW when South magnetic pole is present.
 *   - DO = HIGH when no magnetic field is detected.
 *   - Interrupt triggered on FALLING edge increments cumulative event count.
 *   - 50ms software debounce suppresses mechanical/magnetic bounce.
 * ======================================================================================
 */

#include <WiFi.h>
#include <WiFiClientSecure.h>

// ======================================================================================
// 1. CONFIGURATION PARAMETERS
// ======================================================================================

// Wi-Fi or Mobile Hotspot Credentials
const char* WIFI_SSID     = "Al-Haji";       // Your Wi-Fi or Mobile Hotspot Name
const char* WIFI_PASSWORD = "94971148";      // Enter your Wi-Fi or Hotspot password

// Backend API Endpoint on Render
const char* API_URL       = "https://magnotrack.onrender.com/api/sensor-data";

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
// 4. HTTP / HTTPS TELEMETRY TRANSMISSION (DIRECT SECURE SOCKET)
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
  String payload = "{";
  payload += "\"device_id\":\"" + String(DEVICE_ID) + "\",";
  payload += "\"event_count\":" + String(countSnapshot) + ",";
  payload += "\"magnet_detected\":" + String(magnetDetected ? "true" : "false") + ",";
  payload += "\"uptime_ms\":" + String(uptimeMs);
  payload += "}";

  // 3. Parse host and path from API_URL
  String urlStr = String(API_URL);
  bool isHttps = urlStr.startsWith("https://");
  String temp = isHttps ? urlStr.substring(8) : (urlStr.startsWith("http://") ? urlStr.substring(7) : urlStr);

  int slashIdx = temp.indexOf('/');
  String host = (slashIdx >= 0) ? temp.substring(0, slashIdx) : temp;
  String path = (slashIdx >= 0) ? temp.substring(slashIdx) : "/";

  int port = isHttps ? 443 : 80;
  int colonIdx = host.indexOf(':');
  if (colonIdx >= 0) {
    port = host.substring(colonIdx + 1).toInt();
    host = host.substring(0, colonIdx);
  }

  Serial.printf("[HTTP POST] Sending payload to %s:%d%s\n", host.c_str(), port, path.c_str());
  Serial.print("[HTTP POST] Payload: ");
  Serial.println(payload);

  if (isHttps) {
    // Direct TLS/SSL connection with SNI support to prevent Cloudflare 400 errors
    WiFiClientSecure secureClient;
    secureClient.setInsecure(); // Skip certificate bundle validation on ESP32
    secureClient.setTimeout(10); // 10 second socket timeout

    if (!secureClient.connect(host.c_str(), port)) {
      Serial.println("[HTTP ERROR] Secure TLS handshake failed! Check network/host.");
      return;
    }

    // Send HTTP POST over encrypted TLS tunnel
    secureClient.print("POST " + path + " HTTP/1.1\r\n");
    secureClient.print("Host: " + host + "\r\n");
    secureClient.print("User-Agent: ESP32-MagnoTrack\r\n");
    secureClient.print("Content-Type: application/json\r\n");
    secureClient.print("Connection: close\r\n");
    secureClient.print("Content-Length: " + String(payload.length()) + "\r\n");
    secureClient.print("\r\n");
    secureClient.print(payload);

    // Wait for server response
    unsigned long timeout = millis();
    while (secureClient.available() == 0) {
      if (millis() - timeout > 8000) {
        Serial.println("[HTTP ERROR] Timeout waiting for Render response.");
        secureClient.stop();
        return;
      }
      delay(10);
    }

    String statusLine = secureClient.readStringUntil('\n');
    statusLine.trim();
    Serial.printf("[HTTP] Response: %s\n", statusLine.c_str());

    if (statusLine.indexOf("200") > 0 || statusLine.indexOf("201") > 0) {
      Serial.println("[HTTP] Telemetry recorded successfully by MagnoTrack backend.");
    } else {
      Serial.println("[HTTP] Notice: Non-200 status response.");
    }

    secureClient.stop();

  } else {
    // Plain HTTP for local development
    WiFiClient client;
    client.setTimeout(10);

    if (!client.connect(host.c_str(), port)) {
      Serial.println("[HTTP ERROR] Connection to host failed.");
      return;
    }

    client.print("POST " + path + " HTTP/1.1\r\n");
    client.print("Host: " + host + "\r\n");
    client.print("User-Agent: ESP32-MagnoTrack\r\n");
    client.print("Content-Type: application/json\r\n");
    client.print("Connection: close\r\n");
    client.print("Content-Length: " + String(payload.length()) + "\r\n");
    client.print("\r\n");
    client.print(payload);

    unsigned long timeout = millis();
    while (client.available() == 0) {
      if (millis() - timeout > 8000) {
        Serial.println("[HTTP ERROR] Timeout waiting for local server response.");
        client.stop();
        return;
      }
      delay(10);
    }

    String statusLine = client.readStringUntil('\n');
    statusLine.trim();
    Serial.printf("[HTTP] Response: %s\n", statusLine.c_str());

    if (statusLine.indexOf("200") > 0 || statusLine.indexOf("201") > 0) {
      Serial.println("[HTTP] Telemetry recorded successfully by MagnoTrack backend.");
    }

    client.stop();
  }
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
