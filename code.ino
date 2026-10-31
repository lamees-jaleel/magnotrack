
#include <WiFi.h>
#include <WebServer.h>

// Sensor pin
#define HALL_PIN 27

// iQOO Neo9 Pro hotspot
const char* ssid = "iQOO Neo9 Pro";
const char* password = "12345678";

// Web server
WebServer server(80);

// Event counter
volatile unsigned long eventCount = 0;
volatile unsigned long lastPulseTime = 0;

// Interrupt function
void IRAM_ATTR detectMagnet() {
  unsigned long now = micros();

  if (now - lastPulseTime >= 50000) {
    eventCount++;
    lastPulseTime = now;
  }
}

// Dashboard webpage
const char webpage[] PROGMEM = R"rawliteral(
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>MagnoTrack</title>

<style>
body {
  font-family: Arial;
  background: #edf2f7;
  text-align: center;
  padding: 15px;
}
.header {
  background: #173b70;
  color: white;
  padding: 20px;
  border-radius: 15px;
}
.card {
  background: white;
  padding: 25px;
  margin: 20px auto;
  max-width: 420px;
  border-radius: 15px;
  box-shadow: 0 3px 12px #ccc;
}
.count {
  font-size: 55px;
  font-weight: bold;
  color: #1674d1;
}
.status {
  font-size: 22px;
  font-weight: bold;
}
</style>
</head>

<body>

<div class="header">
<h1>MagnoTrack</h1>
<p>IoT Magnetic Event Monitoring System</p>
</div>

<div class="card">
<h3>Total Magnetic Events</h3>
<div class="count" id="count">0</div>
<p>Detected events</p>
</div>

<div class="card">
<h3>Sensor Status</h3>
<div class="status" id="status">Checking...</div>
<p>A3144 Hall Effect Sensor</p>
</div>

<div class="card">
<h3>ESP32 Connection</h3>
<div class="status" id="connection" style="color:green">
Connected
</div>
</div>

<div class="card">
<h3>Last Updated</h3>
<p id="updated">Waiting...</p>
</div>

<script>
async function updateDashboard() {
  try {
    const response = await fetch('/data');
    if (!response.ok) throw new Error("Server error");

    const data = await response.json();

    document.getElementById('count').innerText =
      data.count;

    const status = document.getElementById('status');

    if (data.detected) {
      status.innerText = "MAGNET DETECTED";
      status.style.color = "red";
    } else {
      status.innerText = "NO MAGNET";
      status.style.color = "green";
    }

    document.getElementById('connection').innerText =
      "Connected";

    document.getElementById('connection').style.color =
      "green";

    document.getElementById('updated').innerText =
      new Date().toLocaleTimeString();

  } catch(error) {
    document.getElementById('connection').innerText =
      "Disconnected";

    document.getElementById('connection').style.color =
      "red";
  }
}

setInterval(updateDashboard, 500);
updateDashboard();
</script>

</body>
</html>
)rawliteral";

// Main webpage
void handleRoot() {
  server.send_P(200, "text/html", webpage);
}

// Sensor data API
void handleData() {
  noInterrupts();
  unsigned long count = eventCount;
  interrupts();

  bool detected = (digitalRead(HALL_PIN) == LOW);

  String json = "{";
  json += "\"count\":" + String(count) + ",";
  json += "\"detected\":";
  json += detected ? "true" : "false";
  json += "}";

  server.send(200, "application/json", json);
}

// Wi-Fi connection
void connectWiFi() {
  WiFi.mode(WIFI_STA);
  WiFi.setSleep(false);
  WiFi.begin(ssid, password);

  Serial.println();
  Serial.println("Connecting to iQOO Neo9 Pro hotspot...");

  unsigned long start = millis();

  while (WiFi.status() != WL_CONNECTED &&
         millis() - start < 30000) {
    delay(500);
    Serial.print(".");
  }

  Serial.println();

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("WiFi Connected!");
    Serial.print("Hotspot: ");
    Serial.println(ssid);
    Serial.print("ESP32 IP Address: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("WiFi connection failed!");
    Serial.println("Check hotspot name and password.");
  }
}

// Setup
void setup() {
  Serial.begin(115200);

  pinMode(HALL_PIN, INPUT_PULLUP);

  attachInterrupt(
    digitalPinToInterrupt(HALL_PIN),
    detectMagnet,
    FALLING
  );

  Serial.println("MAGNOTRACK STARTING");

  connectWiFi();

  server.on("/", handleRoot);
  server.on("/data", handleData);

  server.begin();

  Serial.println("Web Server Started!");
}

// Main loop
void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    WiFi.reconnect();
    delay(1000);
  }

  server.handleClient();
}
