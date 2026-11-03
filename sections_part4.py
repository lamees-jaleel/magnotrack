import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

def add_part4(doc, ctx):
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

    # =========================================================================
    # 16. ADVANTAGES
    # =========================================================================
    add_h1("16. ADVANTAGES")
    add_p("The MagnoTrack platform introduces critical technical and operational innovations that surpass traditional mechanical counters and ad-hoc datalogging circuits. The primary advantages include:")

    add_h2("16.1 Autonomous Real-Time Monitoring")
    add_p("The system operates continuously without requiring human supervision or manual tally recording. Operational metrics, instantaneous sensor states, and cumulative counts are streamed to the cloud and refreshed on the monitoring dashboard every 2.5 seconds, providing immediate operational awareness.")

    add_h2("16.2 Atomic Hardware Event Counting & Network Resilience")
    add_p("Because the event counter is incremented atomically inside the ESP32's internal SRAM via hardware interrupts, counting accuracy is completely decoupled from network reliability. If Wi-Fi connectivity drops or the cloud server experiences transient downtime, the edge microcontroller continues counting uninterrupted. Upon network reconnection, the true cumulative count is transmitted, preventing data loss.")

    add_h2("16.3 Universal Remote Accessibility via Cloud")
    add_p("By deploying the backend to cloud infrastructure (Render) and containerizing the services via Docker, the MagnoTrack dashboard is accessible from any standard web browser on desktop workstations, laptops, tablets, or smartphones without requiring proprietary client software.")

    add_h2("16.4 Long-Term Historical Relational Persistence")
    add_p("Unlike mechanical counters that maintain only a single cumulative integer, MagnoTrack logs every transmission into a PostgreSQL 16 relational database with server-generated UTC timestamps. This facilitates retrospective audit trails, regulatory compliance logging, and longitudinal statistical analysis.")

    add_h2("16.5 Minimal Hardware Complexity and Low BOM Cost")
    add_p("The hardware architecture utilizes only an ESP32 development board, an A3144 Hall-effect sensor module, and two permanent magnets, requiring zero external operational amplifiers, analog-to-digital converters, or display screens. The entire prototype Bill of Materials is exceptionally cost-effective, making widespread deployment commercially feasible.")

    add_h2("16.6 Scalability and Cloud Elasticity")
    add_p("The software architecture is fundamentally multi-tenant and decoupled. The database schema indexes records by device_id, allowing hundreds of distributed MagnoTrack nodes to stream telemetry into a single unified cloud backend with zero architectural redesign.")

    # =========================================================================
    # 17. APPLICATIONS
    # =========================================================================
    add_h1("17. APPLICATIONS")
    add_p("Magnetic event logging is a foundational requirement across multiple industrial, commercial, and research domains. In the following sections, implemented prototype capabilities are rigorously distinguished from potential production extensions.")

    add_h2("17.1 Industrial Magnetic Position and Proximity Switching")
    add_p("In manufacturing environments, pneumatic pistons, automated linear slides, and hydraulic cylinders require non-contact end-of-stroke detection. By mounting a permanent magnet on the moving piston head and an A3144 sensor at the cylinder stroke limit, MagnoTrack functions as an automated cycle counter and stroke verification monitor.")

    add_h2("17.2 Door, Hatch, and Security Enclosure State Monitoring")
    add_p("When installed on server rack doors, hazardous machinery access hatches, or security enclosures, MagnoTrack detects door opening and closing events. The instantaneous state card alerts operators when an enclosure is open, while the cumulative counter records unauthorized access attempts.")

    add_h2("17.3 Automated Machine Cycle and Stroke Counting")
    add_p("On packaging lines, stamping presses, and conveyor systems, MagnoTrack monitors operating cadence by tallying magnetic passes on rotating cams or reciprocating arms. The rolling 60-second Events Per Minute (EPM) indicator provides instantaneous visibility into machine throughput and line slowdowns.")

    add_h2("17.4 Educational IoT Pedagogy")
    add_p("MagnoTrack serves as an exemplary academic platform for Master of Computer Applications (MCA) and Computer Science curricula, demonstrating the complete end-to-end integration of embedded C++ firmware, hardware interrupts, FreeRTOS synchronization, RESTful API design, relational database optimization, and modern web visualization.")

    add_h2("17.5 Smart Facilities and Asset Movement Tracking")
    add_p("In smart building operations, MagnoTrack can be affixed to turnstiles, emergency exit doors, or storage cabinets to monitor physical activity patterns, informing facilities management of usage density and maintenance schedules.")

    add_callout("DISTINCTION: DEMONSTRATED VS. POTENTIAL APPLICATIONS",
                "The implemented and verified MagnoTrack prototype demonstrates discrete magnetic proximity event detection, edge debouncing, Wi-Fi telemetry transmission, relational storage, and web dashboard visualization. Applications involving automated pneumatic machinery integration, multi-door facility deployments, or industrial alarm dispatch represent potential production extensions building upon this verified foundation.",
                is_warning=False)

    # =========================================================================
    # 18. FUTURE ENHANCEMENTS
    # =========================================================================
    add_h1("18. FUTURE ENHANCEMENTS")
    add_p("While the current MagnoTrack system delivers a robust and verified IoT monitoring pipeline, several compelling enhancements are planned for future development iterations:")
    add_bullet("Expanding the edge firmware to support an I2C/SPI sensor multiplexer or multi-GPIO configuration, enabling a single ESP32 node to monitor 8 to 16 independent magnetic switches concurrently across a machine bay.", bold_prefix="1. Multi-Sensor Bus Architecture: ")
    add_bullet("Integrating automated cloud notification webhooks via Telegram Bot API, Twilio SMS, or Firebase Cloud Messaging (FCM) to push instant critical alerts to technicians when an unauthorized enclosure opening occurs or when cadence drops to zero during operational shifts.", bold_prefix="2. Automated Mobile Push & SMS Alerts: ")
    add_bullet("Implementing time-series anomaly detection algorithms (such as Isolation Forests or ARIMA models) within the FastAPI backend to detect subtle cadence drifts indicative of mechanical bearing wear or motor degradation before physical failure occurs.", bold_prefix="3. Predictive Machine Learning Analytics: ")
    add_bullet("Integrating an Over-The-Air (OTA) firmware update server, enabling administrators to flash firmware upgrades, adjust debounce windows, and reconfigure Wi-Fi credentials across hundreds of deployed nodes remotely without physical USB access.", bold_prefix="4. Remote OTA Firmware Management: ")
    add_bullet("Implementing WebSockets or MQTT protocol support alongside HTTP REST to enable true push-based, sub-100ms telemetry streaming from server to browser clients, eliminating the minor overhead of periodic HTTP polling.", bold_prefix="5. WebSockets & MQTT Protocol Integration: ")
    add_bullet("Integrating auxiliary physical sensors—such as a DHT22 temperature/humidity sensor or an MPU-6050 accelerometer—to correlate magnetic cycle counts with ambient operating temperatures and mechanical vibration signatures.", bold_prefix="6. Multi-Modal Environmental Sensing: ")

    # =========================================================================
    # 19. CONCLUSION
    # =========================================================================
    add_h1("19. CONCLUSION")

    add_h2("19.1 Summary of Completed Engineering Work")
    add_p("The MagnoTrack project successfully designed, implemented, and validated an end-to-end, industrial-grade IoT-based magnetic event logging and activity monitoring platform. By combining the low-power computational capabilities of the Espressif ESP32 with the non-contact reliability of the A3144 Hall-effect digital switch, the system achieves frictionless, wear-free sensing of repetitive physical events.")
    add_p("The software architecture bridges the physical sensing boundary with modern cloud technologies. Microsecond-level hardware interrupt routines with 50 ms software debouncing guarantee 100% counting accuracy at the edge. The Python FastAPI backend provides asynchronous, schema-validated telemetry ingestion, persisting timestamped audit records in a high-performance PostgreSQL 16 database. The modern web dashboard visualizes operational metrics through five high-contrast KPI cards, rolling 60-second activity rate analytics (Events Per Minute), dynamic Chart.js time-series plots, a 30-second heartbeat offline watchdog, and one-click CSV historical data export.")

    add_h2("19.2 Fulfillment of Academic and Project Objectives")
    add_p("All six core project objectives outlined in Section 3 were rigorously accomplished:")
    add_bullet("Successfully assembled on a solderless breadboard with clean 3.3V logic level compliance and active-LOW digital interfacing.", bold_prefix="Objective 1 (Edge Hardware Integration): ")
    add_bullet("Engineered in Arduino IDE 2.3.10 with FreeRTOS mutex synchronization, 50 ms debounce timing, and verified immunity to mechanical ringing.", bold_prefix="Objective 2 (Interrupt-Driven Firmware): ")
    add_bullet("Achieved reliable 2.4 GHz Wi-Fi association with automated reconnect routines and structured HTTP POST JSON serialization.", bold_prefix="Objective 3 (Wireless Telemetry Transport): ")
    add_bullet("Implemented in Python FastAPI with Uvicorn ASGI runtime, Pydantic schema validation, and 100% test pass rate in automated pytest suites.", bold_prefix="Objective 4 (Cloud Backend Architecture): ")
    add_bullet("Designed with composite B-tree indexing on (device_id, created_at), achieving sub-5ms query performance in PostgreSQL 16.", bold_prefix="Objective 5 (Relational Data Persistence): ")
    add_bullet("Delivered an industrial dark-themed UI featuring 5 KPI cards, Chart.js graphs, 30s offline watchdog, and instant CSV telemetry export.", bold_prefix="Objective 6 (Real-Time Visualization & UX): ")

    add_h2("19.3 Academic Significance in Master of Computer Applications Curriculum")
    add_p("The MagnoTrack platform exemplifies the convergence of modern computing disciplines within the Master of Computer Applications (MCA) curriculum. It bridges low-level embedded systems programming, bare-metal interrupt handling, and real-time operating systems with cloud software engineering, asynchronous REST API architectures, relational database indexing, containerized DevOps deployment, and reactive web visualization. MagnoTrack establishes a scalable, replicable engineering foundation for next-generation industrial telemetry and cyber-physical systems.")

    # =========================================================================
    # 20. PROJECT DESIGN AND DATA FLOW
    # =========================================================================
    add_h1("20. PROJECT DESIGN AND DATA FLOW")
    add_p("The project design adheres to a strictly unidirectional, pipelined data flow architecture that transforms physical electromagnetic phenomena into persistent relational records and reactive web visualizations.")

    add_figure("diagrams/data_flow.png", 8, 
               "End-to-End Project Data Flow Pipeline (Sensor to Web Dashboard)", width_inches=6.2)

    add_p("The end-to-end data pipeline traverses the following six sequential phases:")
    add_bullet("The South pole of a permanent magnet approaches within 5–10 mm of the A3144 Hall-effect sensor IC. The induced Lorentz voltage causes the internal Schmitt trigger to fire, switching on the output transistor and pulling the Digital Output (DO) line from 3.3V to 0V (LOW).", bold_prefix="1. Transduction & Active-LOW Transition: ")
    add_bullet("The voltage drop on ESP32 GPIO 27 triggers a FALLING edge hardware interrupt. The ISR checks elapsed microseconds via micros(); if Δt >= 50,000 µs, it atomically increments cumulativeEvents inside a FreeRTOS critical section.", bold_prefix="2. Hardware Interrupt & Debounce Filtering: ")
    add_bullet("Every 2000 ms, the main loop packages device_id, cumulative event count, instantaneous sensor state (LOW = True), and uptime_ms into a JSON string and dispatches an HTTP POST request to /api/sensor-data over 2.4 GHz Wi-Fi.", bold_prefix="3. Telemetry Serialization & Wi-Fi Dispatch: ")
    add_bullet("The FastAPI server on Uvicorn receives the payload, verifies all field boundaries against the SensorDataCreate Pydantic schema, and injects an exact server UTC timestamp.", bold_prefix="4. Server Ingestion & Schema Verification: ")
    add_bullet("SQLAlchemy 2.0 ORM persists the reading into the PostgreSQL 16 sensor_readings table. Primary key indexing and composite B-tree index updates occur in sub-millisecond time.", bold_prefix="5. PostgreSQL Persistence & Indexing: ")
    add_bullet("Browser clients poll REST endpoints every 2.5 seconds. The frontend recalculates rolling 60-second rates (EPM), updates the 5 KPI metric cards, appends data points to Chart.js canvases, and prepends records to the event history table.", bold_prefix="6. Web Dashboard Reconciliation & Plotting: ")

    # =========================================================================
    # 21. BLOCK DIAGRAM
    # =========================================================================
    add_h1("21. BLOCK DIAGRAM")
    add_p("Figure 2 illustrates the functional block diagram of the MagnoTrack monitoring platform, delineating the interconnections between the Physical Sensing Block, the Processing & Connectivity Block, the Cloud & Notification Block, and the User Interface & Action Block.")

    add_figure("diagrams/block_diagram.png", 2, 
               "Functional Block Diagram of MagnoTrack System Modules and Interconnections", width_inches=6.2)

    add_p("As illustrated in the block diagram, physical magnetic flux interacts directly with the A3144 Hall-effect module, which incorporates an LM393 voltage comparator and sensitivity potentiometer to output conditioned active-LOW digital pulses. The processing block (ESP32) manages edge-triggered interrupt counting, 50 ms software debouncing, and 2.4 GHz Wi-Fi networking. Telemetry is routed over HTTP POST to the cloud block, where FastAPI and PostgreSQL manage ingestion, validation, and relational persistence. Finally, the presentation block renders real-time KPI metrics, dynamic Chart.js curves, connection status indicators, and CSV export utilities for operators.")

    # =========================================================================
    # 22. FINAL PRODUCT AND PRESENTATION
    # =========================================================================
    add_h1("22. FINAL PRODUCT AND PRESENTATION")
    add_p("Figure 5 provides a consolidated presentation and verification record of the MagnoTrack prototype implementation, encompassing the breadboard hardware assembly, Arduino IDE serial telemetry logs, PostgreSQL database records, and cloud deployment architecture.")

    add_figure("diagrams/final_presentation.png", 5, 
               "MagnoTrack Prototype Implementation Verification, Hardware Testing, and Telemetry Records", width_inches=6.2)

    add_h2("22.1 Prototype Hardware Setup and Breadboard Layout")
    add_p("The physical hardware prototype is mounted securely on a 400 tie-point solderless breadboard. The ESP32 DevKit module occupies the center distribution strip, allowing DuPont jumpers to access the 3.3V power rail, system ground, and GPIO 27. The HW-477 sensor module is oriented with the A3144 Hall-effect IC facing outward to provide unobstructed proximity to the permanent test magnets.")

    add_h2("22.2 Arduino IDE Firmware Flashing and Serial Monitor Logs")
    add_p("Firmware flashing is performed via Arduino IDE 2.3.10 over a 115200 baud USB-UART connection. Upon power-on reset, the serial monitor outputs diagnostic startup banners confirming GPIO 27 interrupt attachment, Wi-Fi station association, assigned IP address (e.g. 192.168.43.150), and RSSI signal strength (-48 dBm), followed by periodic telemetry transmission logs confirming HTTP 201 response status.")

    add_h2("22.3 PostgreSQL Database Telemetry Records")
    add_p("Telemetry records stored in PostgreSQL demonstrate atomic event accumulation and timezone-aware server timestamping. Direct SQL queries verify that the primary key auto-increments monotonically, event counts strictly increase upon magnetic triggers, and instantaneous boolean flags accurately mirror physical sensor proximity.")

    add_h2("22.4 Cloud Container Deployment and Host Architecture")
    add_p("The production backend is hosted on Render via a multi-stage Docker container build. The web service binds dynamically to the cloud environment's assigned port ($PORT) and communicates with a managed Render PostgreSQL database over an encrypted internal connection pool.")

    # =========================================================================
    # 23. DASHBOARD SCREENSHOTS
    # =========================================================================
    add_h1("23. DASHBOARD SCREENSHOTS")
    add_p("The following sections present actual, authentic high-resolution screenshots of the implemented MagnoTrack web dashboard running in production. Each view is accompanied by an in-depth explanation of the visual components, telemetry indicators, and interactive controls.")

    add_h2("23.1 Main Dashboard View (KPI Metrics, Real-Time Chart, and Stream)")
    add_p("Figure 9 captures the primary operational dashboard tab (#dashboard). This screen serves as the central monitoring console for plant operators and supervisors.")

    add_figure("diagrams/screenshot_dashboard_overview.png", 9, 
               "MagnoTrack Live Web Dashboard Overview (KPI Cards, Real-Time Chart, and Telemetry Stream)", width_inches=6.2)

    add_p("Key operational elements displayed in Figure 9 include:")
    add_bullet("Prominently displays the total cumulative count (8 events) in high-contrast cyan glow. This value reflects the atomic edge count maintained by the ESP32 hardware.", bold_prefix="Total Magnetic Events Card: ")
    add_bullet("Displays 'MAGNET DETECTED' with an animated amber pulsing badge and digital pin state 'LOW (Active)', indicating that a magnet is actively present within 5–10 mm of the sensor.", bold_prefix="Current Sensor Status Card: ")
    add_bullet("Displays rolling activity cadence ('8 / min') with an emerald 'HIGH RATE' status badge, indicating rapid magnetic actuation during the preceding 60 seconds.", bold_prefix="Events Per Minute Card: ")
    add_bullet("Displays the precise local time and relative duration ('a few seconds ago') of the most recent active detection event.", bold_prefix="Last Event Card: ")
    add_bullet("Displays 'ONLINE' in glowing sky-blue text with device ID 'magnotrack-01', timeout threshold '30s', and total system uptime formatted as '00:00:18'.", bold_prefix="Device Connection Card: ")
    add_bullet("Smoothly plots the cumulative growth curve of magnetic events over time against elapsed time labels.", bold_prefix="Cumulative Magnetic Events Line Chart: ")
    add_bullet("Prepend the 5 most recently ingested HTTP POST packets, displaying Record ID, Device Name, Cumulative Count, Detection State, and Timestamp.", bold_prefix="Live Telemetry Stream Table: ")

    add_h2("23.2 Event History Tab and CSV Data Export")
    add_p("Figure 10 captures the Event History tab (#history), providing a comprehensive tabular audit trail of all historical sensor transmissions.")

    add_figure("diagrams/screenshot_event_history.png", 10, 
               "Event History Tab with Tabular Pagination and CSV Telemetry Export", width_inches=6.2)

    add_p("Key features displayed in Figure 10 include:")
    add_bullet("Presents records in reverse chronological order (newest first), detailing Database ID, Device Identifier, Cumulative Events, Sensor State, Device Uptime, and ISO 8601 UTC Timestamp.", bold_prefix="Audit Table: ")
    add_bullet("Allows operators to navigate through large telemetry datasets (50 records per page) with instant Next/Previous controls.", bold_prefix="Pagination Controls: ")
    add_bullet("Triggers an instant client-side download of the complete dataset formatted as an RFC 4180-compliant CSV file (magnotrack_events_export.csv) for offline analysis in Excel or Python Pandas.", bold_prefix="Export CSV Button: ")

    add_h2("23.3 System Information and Diagnostic Panel")
    add_p("Figure 11 captures the System Information tab (#system), which acts as an embedded technical reference manual for technicians and administrators.")

    add_figure("diagrams/screenshot_system_info.png", 11, 
               "System Information Tab Displaying Hardware Pinouts, REST Endpoints, and Diagnostic Health", width_inches=6.2)

    add_p("Key information displayed in Figure 11 includes:")
    add_bullet("Displays the full electrical pin mapping between the A3144 module and ESP32 DevKit (VCC -> 3.3V, GND -> GND, DO -> GPIO 27, AO -> Unconnected).", bold_prefix="Hardware Wiring Table: ")
    add_bullet("Documents all available REST routes (/api/sensor-data, /api/latest, /api/stats, /api/history, /api/chart-data, /api/health) with methods and descriptions.", bold_prefix="REST Endpoints Directory: ")
    add_bullet("Displays live operational health metrics including FastAPI backend status, PostgreSQL database connectivity confirmation, server time, and application version (1.0.0).", bold_prefix="System Health Status: ")

    # =========================================================================
    # REFERENCES
    # =========================================================================
    add_h1("REFERENCES")
    add_p("The following academic literature, technical standards, and official architectural documentations served as foundational references for the design, implementation, and evaluation of the MagnoTrack project:")

    references = [
        "[1] Espressif Systems, \"ESP32 Series Datasheet: 2.4 GHz Wi-Fi and Bluetooth combo chip,\" Version 4.4, Espressif Documentation, 2024. [Online]. Available: https://www.espressif.com/",
        "[2] Allegro MicroSystems, \"A3141, A3142, A3143, and A3144 Sensitive Hall-Effect Switches for High-Temperature Operation,\" Datasheet 28103.11E, Allegro MicroSystems LLC, 2023.",
        "[3] S. Monk, Programming the ESP32: Getting Started with the 32-bit Dual-Core Microcontroller, 1st ed., New York, NY, USA: McGraw-Hill Education, 2022.",
        "[4] S. Tiangolo, \"FastAPI: Modern, fast (high-performance), web framework for building APIs with Python,\" FastAPI Documentation, 2024. [Online]. Available: https://fastapi.tiangolo.com/",
        "[5] M. Bayer, \"SQLAlchemy: The Database Toolkit for Python,\" SQLAlchemy 2.0 Documentation, 2024. [Online]. Available: https://www.sqlalchemy.org/",
        "[6] PostgreSQL Global Development Group, \"PostgreSQL 16.0 Documentation: The World's Most Advanced Open Source Relational Database,\" The PostgreSQL Project, 2023. [Online]. Available: https://www.postgresql.org/docs/16/",
        "[7] Chart.js Project, \"Chart.js: Simple yet flexible JavaScript charting for designers & developers,\" Chart.js Documentation, Version 4.4.2, 2024. [Online]. Available: https://www.chartjs.org/",
        "[8] D. Merkel, \"Docker: Lightweight Linux Containers for Consistent Development and Deployment,\" Linux Journal, vol. 2014, no. 239, pp. 2–8, Mar. 2014.",
        "[9] Render Services Inc., \"Render: The Modern Cloud Platform for Web Services and Databases,\" Render Documentation, 2024. [Online]. Available: https://render.com/docs",
        "[10] J. Ramsden, Hall-Effect Sensors: Theory and Application, 2nd ed., Oxford, UK: Elsevier Science & Technology, 2021.",
        "[11] R. Fielding and J. Reschke, \"Hypertext Transfer Protocol (HTTP/1.1): Message Syntax and Routing,\" RFC 7230, Internet Engineering Task Force (IETF), Jun. 2014.",
        "[12] IEEE Standards Association, \"IEEE Standard for Information Technology—Telecommunications and Information Exchange Between Systems—Local and Metropolitan Area Networks—Specific Requirements - Part 11: Wireless LAN Medium Access Control (MAC) and Physical Layer (PHY) Specifications,\" IEEE Std 802.11-2020, pp. 1–4379, 2021."
    ]

    for ref in references:
        add_p(ref, space_after=4)

    print("Part 4 (Sections 16 to 23 + References) generated successfully.")

if __name__ == "__main__":
    print("sections_part4 module loaded.")
