import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

def add_part2(doc, ctx):
    add_h1 = ctx["add_h1"]
    add_h2 = ctx["add_h2"]
    add_h3 = ctx["add_h3"]
    add_p = ctx["add_p"]
    add_bullet = ctx["add_bullet"]
    add_callout = ctx["add_callout"]
    add_figure = ctx["add_figure"]
    COLOR_NAVY = ctx["COLOR_NAVY"]
    COLOR_BLUE = ctx["COLOR_BLUE"]
    COLOR_BODY = ctx["COLOR_BODY"]
    COLOR_SLATE = ctx["COLOR_SLATE"]
    set_cell_shading = ctx["set_cell_shading"]
    set_cell_margins = ctx["set_cell_margins"]
    set_table_borders = ctx["set_table_borders"]
    HEX_NAVY = ctx["HEX_NAVY"]
    HEX_LIGHT_ROW = ctx["HEX_LIGHT_ROW"]
    HEX_BORDER = ctx["HEX_BORDER"]

    # =========================================================================
    # 6. SYSTEM ARCHITECTURE
    # =========================================================================
    add_h1("6. SYSTEM ARCHITECTURE")

    add_h2("6.1 High-Level Multi-Tier System Architecture")
    add_p("The MagnoTrack system architecture is structured according to a modern, decoupled, multi-tier cyber-physical model comprising five distinct operational layers: the Perception Layer, the Embedded Edge Layer, the Network & Ingestion Layer, the Cloud Backend & Persistence Layer, and the Presentation & Dashboard Layer. This hierarchical partitioning guarantees modularity, maintainability, low edge latency, and horizontal scalability.")
    
    add_figure("diagrams/system_architecture.png", 1, 
               "High-Level Five-Tier System Architecture of MagnoTrack Monitoring Platform", width_inches=6.2)

    add_h2("6.2 Hardware Architecture Overview")
    add_p("The hardware architecture embodies an ultra-lean, low-power edge sensing topology engineered around the Espressif ESP32 DevKit microcontroller. The physical setup requires zero external operational amplifiers or analog-to-digital converters, as signal conditioning is executed directly on the A3144 HW-477 module via an integrated LM393 voltage comparator. Power is supplied through a regulated 5V USB interface, which is stepped down to 3.3V DC by the ESP32 board's low-dropout (LDO) regulator to power both the microcontroller and the Hall sensor module.")

    add_h2("6.3 Software Architecture Overview")
    add_p("The software architecture leverages an asynchronous, event-driven reactive paradigm spanning both edge firmware and cloud services. The ESP32 executes bare-metal C++ firmware built upon the FreeRTOS framework, dedicating hardware interrupt lines to microsecond-level edge capture while running network tasks asynchronously. On the cloud server, Python FastAPI delivers an Asynchronous Server Gateway Interface (ASGI) runtime on Uvicorn, parsing and verifying inbound HTTP POST JSON streams with sub-millisecond execution times.")

    add_h2("6.4 Perception & Device Layer")
    add_p("The Perception Layer is situated at the physical boundary. It consists of the permanent magnet and the A3144 Hall-effect sensor module. The transducer continuously monitors localized magnetic flux density perpendicular to the semiconductor plate. When the South pole of a magnet approaches within the 5–10 mm activation threshold, the internal Hall plate creates a transverse potential difference that triggers the internal Schmitt trigger, switching on the output transistor and pulling the DO pin to 0V (active-LOW).")

    add_h2("6.5 Network & Communication Layer")
    add_p("The Communication Layer bridges the physical edge with the cloud infrastructure. The ESP32's integrated 2.4 GHz radio associates with a standard IEEE 802.11 b/g/n Wi-Fi local area network or mobile hotspot. Telemetry packets are serialized into lightweight JSON structures and dispatched via standard HTTP/1.1 POST requests. When targeting production cloud instances (such as Render), the firmware seamlessly switches to TLS/SSL encryption via WiFiClientSecure.")

    add_h2("6.6 Cloud Backend & API Ingestion Layer")
    add_p("The Ingestion Layer is hosted on Render or within Docker containers. Running FastAPI 0.110+ and Uvicorn, this layer exposes structured RESTful endpoints (/api/sensor-data, /api/latest, /api/stats, /api/history, /api/chart-data, /api/health). Inbound requests are validated against strict Pydantic schemas that enforce field presence and mathematical boundary constraints (e.g., event_count >= 0, uptime_ms >= 0).")

    add_h2("6.7 Relational Database Layer")
    add_p("The Database Layer manages persistent, audit-ready data storage. Built upon PostgreSQL 16, telemetry records are inserted into the sensor_readings table through SQLAlchemy 2.0 ORM. The database engine employs connection pooling with pre-ping validation to ensure resilient connectivity across transient network lapses, while a composite B-tree index on (device_id, created_at) provides instantaneous retrieval for chronological and rate-based queries.")

    add_h2("6.8 Presentation & Visualization Dashboard Layer")
    add_p("The Presentation Layer provides operators with an interactive, responsive single-page web interface built with modern HTML5, CSS3, and ES6 JavaScript. The dashboard polls the backend REST APIs at regular intervals (default 2.5 seconds), dynamically updating five KPI metric cards, refreshing Chart.js time-series plots, managing pagination across historical logs, and offering one-click CSV telemetry export.")

    # =========================================================================
    # 7. HARDWARE COMPONENTS
    # =========================================================================
    add_h1("7. HARDWARE COMPONENTS")
    add_p("In strict accordance with the physical implementation of the prototype, MagnoTrack incorporates only the actual hardware components detailed below. No auxiliary load cells, analog amplifier ICs, or peripheral screens are used.")

    add_figure("diagrams/hardware_components.png", 4, 
               "MagnoTrack Prototype Hardware Components, Sensors, and Specifications", width_inches=6.2)

    add_h2("7.1 ESP32 Development Board (ESP-WROOM-32)")
    add_p("The central processing and communications hub of the MagnoTrack edge node is the ESP32 DevKit V1 development board, powered by the Espressif ESP-WROOM-32 system-on-chip (SoC). Key architectural specifications include:")
    add_bullet("Xtensa dual-core 32-bit LX6 microprocessor operating at a configurable clock frequency up to 240 MHz, delivering computational power of up to 600 DMIPS.", bold_prefix="Processor Core: ")
    add_bullet("520 KB internal SRAM, 448 KB ROM, and 4 MB external SPI flash memory for persistent firmware program storage.", bold_prefix="Memory Architecture: ")
    add_bullet("Integrated 802.11 b/g/n Wi-Fi baseband and RF transceiver operating in the 2.4 GHz ISM band, supporting transmission speeds up to 150 Mbps and WPA/WPA2-Personal security.", bold_prefix="Wireless Radio: ")
    add_bullet("34 programmable GPIO pins supporting edge-triggered hardware interrupts, internal pull-up and pull-down resistors, and capacitive touch sensing.", bold_prefix="Peripherals & Interrupts: ")
    add_bullet("Onboard AMS1117-3.3 low-dropout linear voltage regulator converting 5V USB input into a stable 3.3V DC system rail.", bold_prefix="Power Management: ")

    add_h2("7.2 A3144 Hall-Effect Sensor Module (HW-477 PCB)")
    add_p("Physical magnetic detection is performed by an A3144 Hall-effect digital switch module (commercial breakout model HW-477). The module incorporates an A3144 integrated circuit paired with an LM393 dual differential voltage comparator and an adjustable multiturn potentiometer.")
    add_bullet("The A3144 is a monolithic Hall-effect switch containing a Hall voltage generator, small-signal amplifier, Schmitt trigger, and open-collector output transistor in a 3-pin SIP package.", bold_prefix="A3144 Integrated Circuit: ")
    add_bullet("The module includes an LM393 comparator that squares off the sensor's analog output against a reference voltage set by the onboard potentiometer, providing a clean digital switching threshold with high noise margin.", bold_prefix="LM393 Comparator: ")
    add_bullet("Two onboard surface-mount LEDs indicate operational status: a red power LED illuminates upon DC energization, and a green detection LED illuminates whenever a magnetic field pulls the digital output LOW.", bold_prefix="Status Indicators: ")
    add_bullet("The module exposes four pins: VCC (power), GND (ground), DO (digital output), and AO (analog output, unpopulated/unused).", bold_prefix="Pin Configuration: ")

    add_h2("7.3 Permanent Magnets and Polarity Characteristics")
    add_p("Two small permanent magnets (neodymium NdFeB disc magnets) are utilized to actuate the A3144 sensor. Neodymium magnets exhibit high remanence (Br) and high energy product, producing a localized magnetic flux density sufficient to exceed the A3144 magnetic operating point (Bop) at distances of 5 to 10 mm.")
    add_callout("CRITICAL POLARITY REQUIREMENT", 
                "The A3144 Hall-effect switch IC is unipolar and responds exclusively to the SOUTH magnetic pole perpendicular to the branded face of the sensor package. Exposure to the North magnetic pole produces zero transition. If detection fails during assembly, the permanent magnet must simply be flipped 180 degrees to present its South pole.", 
                is_warning=True)

    add_h2("7.4 Solderless Breadboard and Interconnect Jumper Wires")
    add_p("The prototype circuit is assembled on a high-grade 400 tie-point solderless breadboard. High-conductivity DuPont jumper wires (female-to-male and male-to-male) establish low-resistance electrical connections between the ESP32 development board and the HW-477 sensor module.")

    add_h2("7.5 Power Supply and USB Programming Interface")
    add_p("The prototype node is powered and programmed via a standard shielded micro-USB cable connected to a 5V DC USB power supply (or host computer USB port). The USB line also provides a 115200 baud UART serial diagnostic interface via the ESP32's onboard CP2102/CH340 USB-to-UART bridge.")

    add_h2("7.6 Prototype Bill of Materials (BOM) Table")
    add_p("Table 2 outlines the complete Bill of Materials (BOM) for the implemented MagnoTrack hardware node, confirming component models, electrical ratings, and quantities.")

    # Table 2: BOM Table
    t2_data = [
        ["Item #", "Component Description", "Part / Model Number", "Key Specifications", "Qty", "Role in Prototype"],
        ["1", "ESP32 DevKit Board", "ESP32 Dev Module (30-pin)", "Dual-Core 240MHz, 520KB SRAM, 2.4GHz Wi-Fi", "1", "Main edge controller & telemetry bridge"],
        ["2", "Hall-Effect Sensor Module", "HW-477 (A3144 IC)", "Active-LOW Digital Switch, LM393, Potentiometer", "1", "Magnetic proximity perception transducer"],
        ["3", "Permanent Test Magnets", "Neodymium NdFeB Discs", "High-coercivity, South-pole active, 10mm dia", "2", "Magnetic flux source for actuation testing"],
        ["4", "Solderless Breadboard", "Standard 400 Tie-Point", "0.1-inch standard pitch, nickel contacts", "1", "Circuit mounting & prototyping platform"],
        ["5", "Dupont Jumper Wires", "Premium Flexible Wires", "24 AWG Copper core, M-M / M-F headers", "3", "3.3V, GND, and GPIO 27 signal lines"],
        ["6", "Micro-USB Power Cable", "Shielded USB-A to Micro-B", "5V DC, 1.0A rating, data sync enabled", "1", "Firmware flashing & primary power source"]
    ]

    t2 = doc.add_table(rows=len(t2_data), cols=6)
    t2.alignment = WD_TABLE_ALIGNMENT.CENTER
    t2.autofit = False
    set_table_borders(t2, HEX_BORDER)

    col_widths2 = [Inches(0.6), Inches(1.5), Inches(1.3), Inches(1.5), Inches(0.4), Inches(0.97)]

    for row_idx, row in enumerate(t2.rows):
        is_header = (row_idx == 0)
        for col_idx, cell in enumerate(row.cells):
            cell.width = col_widths2[col_idx]
            set_cell_margins(cell, top=100, bottom=100, left=100, right=100)
            if is_header:
                set_cell_shading(cell, HEX_NAVY)
            elif row_idx % 2 == 1:
                set_cell_shading(cell, HEX_LIGHT_ROW)
            
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.05
            run = p.add_run(t2_data[row_idx][col_idx])
            run.font.name = "Calibri"
            run.font.size = Pt(8.5 if not is_header else 9.0)
            if is_header:
                run.font.bold = True
                run.font.color.rgb = RGBColor(255, 255, 255)
            else:
                run.font.color.rgb = COLOR_BODY

    # Table Caption
    cp = doc.add_paragraph()
    cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cp.paragraph_format.space_before = Pt(4)
    cp.paragraph_format.space_after = Pt(12)
    c1 = cp.add_run("Table 2: ")
    c1.font.bold = True
    c1.font.size = Pt(9.5)
    c1.font.color.rgb = COLOR_NAVY
    c2 = cp.add_run("Prototype Hardware Bill of Materials (BOM) & Electrical Specifications")
    c2.font.italic = True
    c2.font.size = Pt(9.5)
    c2.font.color.rgb = COLOR_SLATE

    # =========================================================================
    # 8. SOFTWARE COMPONENTS
    # =========================================================================
    add_h1("8. SOFTWARE COMPONENTS")
    add_p("The MagnoTrack software architecture incorporates modern open-source languages, containerized frameworks, and cloud services to achieve enterprise-grade reliability and low latency.")

    add_h2("8.1 Arduino IDE 2.3.10 and ESP32 Arduino Core")
    add_p("The edge microcontroller firmware was developed using Arduino IDE version 2.3.10 running on the official Espressif esp32 board support package (v3.x). The development environment provides integrated compiling, C++17 optimization, serial plotting tools, and automated binary flashing over USB UART. The firmware utilizes core Espressif libraries including WiFi.h, HTTPClient.h, and WiFiClientSecure.h.")

    add_h2("8.2 Python FastAPI Asynchronous Web Framework")
    add_p("The cloud backend server is engineered in Python 3.11+ using the FastAPI web framework. FastAPI is chosen for its superior execution speed (comparable to NodeJS and Go), native asynchronous coroutine support via ASGI (Uvicorn), and automatic OpenAPI (Swagger) documentation generation. FastAPI enables high-throughput handling of simultaneous telemetry POST requests without I/O blocking.")

    add_h2("8.3 PostgreSQL 16 Relational Database Engine")
    add_p("For mission-critical data persistence, MagnoTrack implements PostgreSQL 16—an advanced open-source object-relational database management system (ORDBMS). PostgreSQL provides strict ACID compliance, robust write-ahead logging (WAL), strong data typing, and native support for timezone-aware UTC timestamps. High-speed querying is ensured through B-tree composite indexing.")

    add_h2("8.4 Frontend Technologies: HTML5, Modern CSS3, and ES6 JavaScript")
    add_p("The web monitoring dashboard is developed as an ultra-responsive single-page application (SPA) without the heavyweight dependencies of third-party frontend frameworks. The user interface utilizes semantic HTML5, modern CSS3 employing an industrial dark navy/charcoal slate aesthetic with glowing accents, and vanilla asynchronous ES6 JavaScript managing real-time REST polling, DOM reconciliation, and pagination.")

    add_h2("8.5 Chart.js Dynamic Data Visualization Engine")
    add_p("Real-time data visualization is powered by Chart.js (v4.4.2)—a high-performance, HTML5 Canvas-based JavaScript plotting library. Chart.js renders smooth, interactive line and bar charts tracking cumulative event progression and activity rate deltas over time with hardware-accelerated canvas rendering.")

    add_h2("8.6 Docker Containerization and Docker Compose")
    add_p("To eliminate environment configuration drift and ensure 100% reproducible deployments, MagnoTrack is containerized using Docker. A multi-stage production Dockerfile compiles dependencies and executes the FastAPI server under python:3.11-slim. For local development, Docker Compose coordinates a two-node cluster consisting of the FastAPI application container and an official postgres:16-alpine container with automated healthcheck validation.")

    add_h2("8.7 Render Cloud Platform as a Service (PaaS)")
    add_p("For cloud hosting and public internet accessibility, MagnoTrack is architected for deployment on Render (render.com). Render provides fully managed containerized web services with continuous integration from Git repositories, automated Let's Encrypt SSL/TLS certificates, and managed cloud PostgreSQL instances with automated backups.")

    # =========================================================================
    # 9. WORKING PRINCIPLE
    # =========================================================================
    add_h1("9. WORKING PRINCIPLE")

    add_h2("9.1 Comprehensive Step-by-Step Operational Sequence")
    add_p("The complete operational lifecycle of the MagnoTrack system unfolds across ten rigorously orchestrated stages, tracing the physical emergence of a magnetic field to the real-time visual representation of telemetry on the operator's dashboard.")

    add_figure("diagrams/project_workflow.png", 6, 
               "MagnoTrack Dual-Sided Operational Flowchart (Firmware ISR vs. Cloud Analytics)", width_inches=6.2)

    add_h2("9.2 Detailed Breakdown of the 10-Stage Lifecycle")
    add_p("The 10 operational stages execute sequentially as follows:")
    
    add_p("Stage 1: ESP32 Bootstrapping & Hardware Initialization", bold_prefix="1. ")
    add_p("Upon 5V power-up, the ESP32 boots and executes the setup() function. Serial communication initializes at 115200 baud. GPIO 27 is configured as a digital input with an internal pull-up resistor (pinMode(27, INPUT_PULLUP)), establishing an idle default voltage of 3.3V DC.")

    add_p("Stage 2: Wi-Fi Station Association & Network Handshake", bold_prefix="2. ")
    add_p("The ESP32 radio initializes in Station Mode (WIFI_STA) and initiates association with the configured 2.4 GHz Wi-Fi access point (WIFI_SSID, WIFI_PASSWORD). The firmware polls connection status with a 25-second timeout, printing assigned IP and RSSI signal strength to the serial console upon successful link.")

    add_p("Stage 3: Magnetic Proximity & Hall-Effect Transduction", bold_prefix="3. ")
    add_p("When a permanent magnet moves toward the A3144 Hall-effect sensor and breaches the 5–10 mm threshold, the South magnetic pole induces a transverse Lorentz deflection of charge carriers within the semiconductor plate, generating a Hall voltage.")

    add_p("Stage 4: Digital Signal Conditioning & Active-LOW Transition", bold_prefix="4. ")
    add_p("The onboard LM393 voltage comparator compares the internal Hall voltage against the sensitivity potentiometer threshold. As the threshold is crossed, the comparator switches on the output transistor, immediately pulling the Digital Output (DO) line from 3.3V (HIGH) down to 0V (LOW). The onboard green detection LED illuminates simultaneously.")

    add_p("Stage 5: Hardware Interrupt ISR & Microsecond Debouncing", bold_prefix="5. ")
    add_p("The sudden voltage drop from 3.3V to 0V triggers a hardware interrupt on ESP32 GPIO 27 (configured with FALLING edge sensitivity). The processor immediately halts background execution and vectors into the IRAM-located Interrupt Service Routine (onMagnetDetectedISR). The routine queries current execution time in microseconds via micros(). If the time elapsed since the previous pulse is >= 50,000 microseconds (50 ms), the interrupt enters a critical section (portENTER_CRITICAL_ISR), atomically increments cumulativeEvents by 1, updates lastDebounceMicros, and exits.")

    add_p("Stage 6: Telemetry Packaging & HTTP POST Dispatch", bold_prefix="6. ")
    add_p("Within the main loop(), the firmware checks whether 2000 ms (2.0 seconds) have elapsed since the last transmission. When the timer expires, the firmware captures a thread-safe snapshot of cumulativeEvents, reads the instantaneous sensor pin state (digitalRead(27) == LOW), and queries uptime via millis(). It formats these values into a JSON string: {\"device_id\":\"magnotrack-01\",\"event_count\":N,\"magnet_detected\":bool,\"uptime_ms\":T}. An HTTP POST request is then dispatched via HTTPClient to /api/sensor-data.")

    add_p("Stage 7: Cloud Ingestion & Strict Pydantic Schema Validation", bold_prefix="7. ")
    add_p("The cloud FastAPI server receives the HTTP POST request. The JSON body is parsed against the SensorDataCreate Pydantic schema, validating that device_id is a non-empty string, event_count >= 0, magnet_detected is boolean, and uptime_ms >= 0. Any invalid or malformed packet is rejected with HTTP 422 Unprocessable Entity.")

    add_p("Stage 8: Relational Persistence in PostgreSQL with UTC Timestamping", bold_prefix="8. ")
    add_p("Upon successful schema validation, the FastAPI route instantiates a SensorReading SQLAlchemy ORM object, assigning an exact server-side UTC timestamp (datetime.now(timezone.utc)). The transaction is committed to the PostgreSQL sensor_readings table, auto-generating a primary key ID and returning HTTP 201 Created.")

    add_p("Stage 9: Web Dashboard Polling & KPI Metric Updating", bold_prefix="9. ")
    add_p("The operator's browser executes an asynchronous polling cycle every 2.5 seconds, querying /api/stats, /api/latest, and /api/chart-data. The frontend scripts parse the JSON responses and dynamically update the 5 KPI cards: Total Events counter, Current Sensor Status badge, Events Per Minute (EPM), Last Event time, and ESP32 Online/Offline connection status.")

    add_p("Stage 10: Dynamic Chart Visualization & Historical Log Archiving", bold_prefix="10. ")
    add_p("Chart.js dynamically shifts its time-series buffers to append the newest data points, smoothly re-rendering the Cumulative Events Line Chart and the Activity Frequency Bar Chart. Concurrently, the newest entry is prepended to the Event History table, ready for instant review or CSV download.")

    # =========================================================================
    # 10. CONNECTION DETAILS
    # =========================================================================
    add_h1("10. CONNECTION DETAILS")

    add_h2("10.1 Hardware Wiring Configuration & Pin Mapping")
    add_p("Establishing reliable electrical connections between the ESP32 microcontroller and the A3144 Hall-effect sensor module is vital for noise immunity, logic level compatibility, and reliable edge triggering. Figure 7 illustrates the exact physical wiring diagram.")

    add_figure("diagrams/hardware_wiring.png", 7, 
               "Hardware Wiring & Pinout Schematic (A3144 HW-477 to ESP32 DevKit)", width_inches=6.2)

    add_h2("10.2 Pin Connection Specification Table")
    add_p("Table 3 outlines the exact hardware connections between the HW-477 sensor module and the ESP32 DevKit board.")

    # Table 3: Pinout Table
    t3_data = [
        ["A3144 Module Pin", "ESP32 DevKit Pin", "Signal / Pin Type", "Operating Voltage", "Wire Color", "Functional Description & Design Notes"],
        ["VCC", "3.3V Pin", "DC Power In", "3.3V DC", "Red", "Powers module from ESP32 regulated 3.3V rail. Ensures output logic does not exceed 3.3V."],
        ["GND", "GND Pin", "System Ground", "0V (Common GND)", "Black", "Establishes common electrical reference ground plane across sensor and MCU."],
        ["DO (Digital Out)", "GPIO 27", "Digital Active-LOW", "3.3V Idle / 0V Active", "Blue / Yellow", "Transmits digital edge pulses to ESP32. Configured in firmware with INPUT_PULLUP."],
        ["AO (Analog Out)", "Not Connected", "Analog Output", "Unused / Open", "— (No wire)", "Unconnected. The A3144 is operated exclusively as a digital magnetic switch."]
    ]

    t3 = doc.add_table(rows=len(t3_data), cols=6)
    t3.alignment = WD_TABLE_ALIGNMENT.CENTER
    t3.autofit = False
    set_table_borders(t3, HEX_BORDER)

    col_widths3 = [Inches(1.1), Inches(1.1), Inches(1.0), Inches(0.9), Inches(0.8), Inches(1.37)]

    for row_idx, row in enumerate(t3.rows):
        is_header = (row_idx == 0)
        for col_idx, cell in enumerate(row.cells):
            cell.width = col_widths3[col_idx]
            set_cell_margins(cell, top=100, bottom=100, left=100, right=100)
            if is_header:
                set_cell_shading(cell, HEX_NAVY)
            elif row_idx % 2 == 1:
                set_cell_shading(cell, HEX_LIGHT_ROW)
            
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.05
            run = p.add_run(t3_data[row_idx][col_idx])
            run.font.name = "Calibri"
            run.font.size = Pt(8.5 if not is_header else 9.0)
            if is_header:
                run.font.bold = True
                run.font.color.rgb = RGBColor(255, 255, 255)
            else:
                run.font.color.rgb = COLOR_BODY

    # Table Caption
    cp = doc.add_paragraph()
    cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cp.paragraph_format.space_before = Pt(4)
    cp.paragraph_format.space_after = Pt(12)
    c1 = cp.add_run("Table 3: ")
    c1.font.bold = True
    c1.font.size = Pt(9.5)
    c1.font.color.rgb = COLOR_NAVY
    c2 = cp.add_run("Hardware Wiring & Electrical Pin Connection Specification")
    c2.font.italic = True
    c2.font.size = Pt(9.5)
    c2.font.color.rgb = COLOR_SLATE

    add_h2("10.3 Technical Justification of GPIO 27 & Internal Pull-Up Resistor")
    add_p("GPIO 27 is chosen for the sensor interface because it is a general-purpose digital input/output pin that is not multiplexed with boot strapping registers (unlike GPIO 0, 2, or 12) or SPI flash communication lines (GPIO 6–11). Crucially, GPIO 27 supports internal pull-up resistor activation via software (INPUT_PULLUP). The internal pull-up resistor (~45 kΩ) holds the signal line solidly at 3.3V when no magnet is present, preventing the pin from floating and generating spurious noise interrupts.")

    add_h2("10.4 Hall-Effect Sensing Distinction: Digital Switch vs. Analog Transducer")
    add_p("It is technically critical to distinguish between linear Hall-effect transducers (such as the A1302 or SS49E) and digital Hall-effect switches (such as the A3144). Linear transducers generate an analog output voltage directly proportional to magnetic flux density (measured in Gauss or milliTesla). In contrast, the A3144 is a digital threshold switch: it outputs only two discrete states—HIGH (3.3V, field absent) or LOW (0V, field present).")
    add_callout("CRITICAL SENSING CAPABILITY SPECIFICATION", 
                "The MagnoTrack prototype functions strictly as a digital magnetic event counter and state monitor. The system DOES NOT measure analog magnetic field intensity, magnetic flux density, object velocity, rotational RPM, or direction of motion. All reported metrics represent discrete binary detection events.", 
                is_warning=True)

    add_h2("10.5 Polarity Sensitivity and Magnetic Orientation Requirements")
    add_p("The A3144 Hall IC is unipolar: it switches on when the South magnetic pole of sufficient strength approaches the branded face of the device. If the North pole is presented, the Lorentz deflection occurs in the opposite direction, holding the output transistor in the OFF state. Consequently, proper physical alignment and orientation of the permanent test magnet is required for operation.")

    print("Part 2 (Sections 6 to 10) generated successfully.")

if __name__ == "__main__":
    print("sections_part2 module loaded.")
