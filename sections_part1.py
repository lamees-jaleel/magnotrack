import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

def add_part1(doc, ctx):
    add_h1 = ctx["add_h1"]
    add_h2 = ctx["add_h2"]
    add_h3 = ctx["add_h3"]
    add_p = ctx["add_p"]
    add_bullet = ctx["add_bullet"]
    add_callout = ctx["add_callout"]
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
    # 1. INTRODUCTION
    # =========================================================================
    add_h1("1. INTRODUCTION")

    add_h2("1.1 Introduction to IoT in Industrial & Physical Sensing")
    add_p("The Internet of Things (IoT) represents an epochal architectural paradigm in modern computing and cyber-physical engineering, facilitating the ubiquitous interconnection of physical transducers, edge embedded microcontrollers, network transport protocols, and cloud computing infrastructures. By bridging the physical divide between hardware sensors and distributed digital services, IoT systems enable automated data acquisition, real-time telemetry processing, and remote decision support across critical domains such as industrial automation, facility management, smart building security, and manufacturing logistics.")
    add_p("At the core of IoT perception lies the transducer—an electronic element capable of converting continuous physical phenomena (such as temperature, pressure, optical flux, or magnetic fields) into conditioned electrical signals. When coupled with low-power, high-performance edge microcontrollers equipped with integrated wireless transceivers (such as the Espressif ESP32), physical sensing systems achieve unprecedented agility. Real-time telemetry streams can be dispatched securely across local area networks and wide-area cloud environments, transforming isolated physical interactions into actionable, longitudinally archived analytical intelligence.")

    add_h2("1.2 Importance and Relevance of Magnetic Event Detection")
    add_p("Magnetic event detection constitutes a foundational sensing mechanism across modern industrial machinery, security access points, and positional tracking systems. Unlike mechanical contact switches—which are inherently vulnerable to physical friction, mechanical wear, dust accumulation, contact bounce, and environmental corrosion—magnetic sensing operates via non-contact electromagnetic coupling. In particular, Hall-effect sensing leverages the Lorentz force exerted on mobile charge carriers within a semiconductor conductor exposed to a transverse magnetic flux density, producing a measurable transverse Hall voltage.")
    add_p("Solid-state magnetic switches offer high reliability, near-infinite mechanical lifespans, hermetic environmental isolation, and immunity to particulate contamination. Consequently, magnetic event detection is extensively deployed for:")
    add_bullet("Cycle and stroke counting in reciprocating pneumatic pistons, automated packaging conveyors, and manufacturing presses.", bold_prefix="Industrial Actuator Tracking: ")
    add_bullet("Tamper detection and open/closed state verification on doors, security enclosures, safety cages, and perimeter barriers.", bold_prefix="Security & Access Enclosures: ")
    add_bullet("Non-contact detection of rotating cams, gear teeth, and magnetic markers to monitor operational cadence without mechanical resistance.", bold_prefix="Rotational & Reciprocating Cadence: ")
    add_bullet("Laboratory experiments demonstrating solid-state physics, electromagnetic transduction, and digital event logging.", bold_prefix="Educational IoT Systems: ")

    add_h2("1.3 Problem Addressed by MagnoTrack")
    add_p("Despite the ubiquity of magnetic switches, traditional implementations in small-to-medium manufacturing environments, laboratory facilities, and legacy security enclosures suffer from severe architectural shortcomings. Historically, magnetic event monitoring has relied upon manual observation, handwritten paper logs, or standalone electromechanical tally counters. These conventional paradigms present critical operational failure modes:")
    add_bullet("Manual tallying or periodic visual inspections inherently introduce substantial reporting latency, preventing operators from detecting unexpected machine stoppages or unauthorized enclosure openings in real time.", bold_prefix="Lack of Real-Time Visibility: ")
    add_bullet("Human log keeping is notoriously prone to transcription inaccuracies, missed counts during rapid actuation cycles, and unverified data falsification.", bold_prefix="Human Error & Inaccuracy: ")
    add_bullet("Standalone mechanical counters fail to capture timestamps, event duration, or historical velocity (cadence), rendering root-cause failure analysis and predictive maintenance impossible.", bold_prefix="Absence of Historical Telemetry: ")
    add_bullet("Conventional mechanical counters require physical presence to read the dial, making centralized facility-wide oversight cost-prohibitive and impractical across geographically distributed nodes.", bold_prefix="No Remote Connectivity: ")

    add_h2("1.4 Overview of the Proposed MagnoTrack Solution")
    add_p("To definitively solve these operational bottlenecks, this project presents MagnoTrack: an industrial-grade, academic IoT-based magnetic event logging and activity monitoring platform. MagnoTrack establishes a tightly integrated, multi-tier cyber-physical pipeline spanning edge transduction, microsecond-level edge signal debouncing, wireless telemetry transport, asynchronous cloud ingestion, relational persistence, and interactive web visualization.")
    add_p("At the edge layer, MagnoTrack combines an Espressif ESP32 32-bit dual-core microcontroller with an A3144 Hall-effect digital switch module (HW-477) and dual permanent magnets. When a magnetic field of appropriate polarity (South pole) approaches the sensor within 5–10 mm, the sensor's internal open-collector transistor activates, pulling the digital output (DO) pin to LOW (0V). An interrupt-driven service routine (ISR) on ESP32 GPIO 27 captures this falling edge and increments an atomic hardware event counter protected by a 50 ms microsecond-level software debounce window.")
    add_p("Every two seconds, the ESP32 serializes its current operational telemetry—including unique device ID, cumulative event count, instantaneous sensor state, and microcontroller uptime—into a JSON payload and dispatches it via HTTP POST over 2.4 GHz Wi-Fi to a cloud-hosted backend. The backend, built using Python FastAPI and Uvicorn, validates incoming payloads against Pydantic schemas and stores records in a PostgreSQL 16 database. Operators observe live operations through a modern, responsive web dashboard powered by Chart.js, featuring five KPI metric cards, rolling 60-second activity rate analytics (Events Per Minute), a 30-second device offline watchdog, and one-click CSV historical data export.")

    # =========================================================================
    # 2. AIM OF THE PROJECT
    # =========================================================================
    add_h1("2. AIM OF THE PROJECT")
    add_p("The primary aim of the MagnoTrack project is to design, architect, engineer, and rigorously validate a complete, low-cost, university-level IoT-based magnetic event logging and activity monitoring system that autonomously senses magnetic proximity events at the physical edge, reliably counts detections using interrupt-driven edge firmware, wirelessly transmits structured telemetry to a scalable cloud backend, securely archives time-series records in a relational database, and delivers real-time operational visibility and historical analytics through an interactive, browser-based monitoring dashboard.")

    # =========================================================================
    # 3. OBJECTIVES
    # =========================================================================
    add_h1("3. OBJECTIVES")
    add_p("To accomplish the primary aim, the project is structured around the following six measurable, academic, and technical objectives:")
    add_bullet("To design and assemble a robust, low-voltage hardware sensing node using an ESP32 microcontroller, an A3144 Hall-effect digital switch module (HW-477), and permanent neodymium magnets on a solderless breadboard with clean 3.3V logic interfacing.", bold_prefix="Objective 1 (Edge Hardware Integration): ")
    add_bullet("To develop robust embedded C++ firmware in Arduino IDE 2.3.10 leveraging hardware interrupts on GPIO 27, a 50 ms microsecond-level software debounce filter, and atomic FreeRTOS thread-safe variables to achieve 100% detection accuracy without false mechanical double-triggering.", bold_prefix="Objective 2 (Interrupt-Driven Firmware): ")
    add_bullet("To implement wireless networking on the ESP32 to establish stable 2.4 GHz Wi-Fi connectivity with automated reconnect routines, and transmit JSON telemetry payloads via HTTP POST requests to a cloud REST API at regular intervals.", bold_prefix="Objective 3 (Wireless Telemetry Transport): ")
    add_bullet("To construct a high-performance, asynchronous REST API backend using Python FastAPI and Uvicorn, incorporating strict Pydantic payload validation and SQLAlchemy 2.0 ORM connection pooling.", bold_prefix="Objective 4 (Cloud Backend Architecture): ")
    add_bullet("To design a normalized PostgreSQL 16 relational database schema optimized with composite B-tree indexing on (device_id, created_at) to ensure sub-millisecond retrieval of historical telemetry and rolling-window rate analytics.", bold_prefix="Objective 5 (Relational Data Persistence): ")
    add_bullet("To build a modern, high-contrast industrial web dashboard using HTML5, CSS3, and JavaScript with Chart.js, rendering live cumulative event graphs, activity frequency deltas, rolling 60-second Events Per Minute (EPM) ratings, a 30-second heartbeat offline watchdog, and paginated CSV data export.", bold_prefix="Objective 6 (Real-Time Visualization & UX): ")

    # =========================================================================
    # 4. EXISTING SYSTEM
    # =========================================================================
    add_h1("4. EXISTING SYSTEM")

    add_h2("4.1 Conventional Manual and Mechanical Event Logging")
    add_p("In conventional operational environments, physical displacement, cycle counts, and enclosure states have traditionally been tracked through two primary mechanisms: manual record-keeping and mechanical tally counters.")
    add_bullet("Floor operators or laboratory technicians manually observe the position of a mechanism or door, recording observations on paper sheets or static desktop spreadsheets at scheduled intervals (e.g., hourly or at shift ends).", bold_prefix="Manual Visual Inspection: ")
    add_bullet("Mechanical ratchet counters or electromechanical totalizers are mounted adjacent to moving components. When a physical arm strikes the lever, an internal pawl advances a numbered dial.", bold_prefix="Electromechanical Counters: ")

    add_h2("4.2 Limitations and Vulnerabilities of Existing Systems")
    add_p("While conceptually straightforward, these traditional methodologies exhibit severe technical and operational deficiencies when evaluated against modern industrial automation and academic research standards:")
    add_bullet("Because manual logs are recorded at coarse intervals (e.g., once per shift), critical operational failures—such as unexpected equipment stalls, erratic cycle speeds, or unauthorized access breaches—remain undetected for hours.", bold_prefix="Severe Reporting Latency: ")
    add_bullet("Manual tallying is inherently vulnerable to human distraction, fatigue, accidental miscounts, and deliberate log falsification. In rapid automated systems, human eyes cannot accurately resolve actuation frequencies exceeding 1–2 Hz.", bold_prefix="High Human Error Rate: ")
    add_bullet("Mechanical counters feature moving linkages, springs, and contact pins subject to friction wear, mechanical fatigue, dust jamming, and contact oxidation, requiring frequent physical maintenance.", bold_prefix="Mechanical Wear & Contact Bounce: ")
    add_bullet("Mechanical registers maintain only an aggregated integer dial. They capture zero temporal context: there is no record of the exact second an event occurred, the time elapsed between strokes, or fluctuations in operating speed over time.", bold_prefix="Total Absence of Time-Series Analytics: ")
    add_bullet("Neither paper forms nor mechanical dials can communicate over network protocols. Supervisors cannot monitor equipment performance remotely, necessitating physical transit across facilities to inspect dials.", bold_prefix="Zero Remote Accessibility: ")
    add_bullet("Scaling a legacy monitoring system across multiple machine bays or enclosure clusters requires deploying additional personnel, resulting in unsustainable recurrent labor expenses.", bold_prefix="Poor Scalability: ")

    # =========================================================================
    # 5. PROPOSED SYSTEM
    # =========================================================================
    add_h1("5. PROPOSED SYSTEM")

    add_h2("5.1 System Concept and Architectural Overview")
    add_p("The proposed MagnoTrack platform establishes an autonomous, non-contact, cyber-physical telemetry architecture designed specifically to overcome all limitations of conventional manual and mechanical event monitoring. MagnoTrack replaces physical mechanical strikers with a solid-state A3144 Hall-effect sensor module and replaces manual paper logs with a high-performance Python FastAPI backend and a PostgreSQL 16 relational database.")
    add_p("The operational concept centers around edge-level precision combined with cloud-level elasticity. At the physical edge, the ESP32 microcontroller executes high-priority interrupt service routines to count magnetic field transitions with microsecond resolution. Because the cumulative counter increments atomically directly within the ESP32's onboard SRAM, the system is immune to transient network outages: even if the Wi-Fi connection drops momentarily, zero events are lost. Once network connectivity is restored, the ESP32 transmits the true, accurate cumulative count to the cloud backend.")

    add_h2("5.2 Key Capabilities and Innovation Highlights")
    add_p("The MagnoTrack platform delivers distinct engineering advantages:")
    add_bullet("The A3144 sensor detects magnetic flux without physical contact, providing near-infinite operating cycles and total immunity to mechanical friction or contact oxidation.", bold_prefix="Frictionless Non-Contact Sensing: ")
    add_bullet("Firmware-level microsecond timing enforces a 50 ms debounce lockout, cleanly suppressing magnetic fringing and mechanical bounce.", bold_prefix="Hardware Edge Debouncing: ")
    add_bullet("Every reading is timestamped at the cloud server with coordinated universal time (UTC) precision, creating an immutable, audit-ready historical record.", bold_prefix="High-Precision Time-Series Telemetry: ")
    add_bullet("The web dashboard continuously computes events detected within a sliding 60-second window, categorizing operational velocity into IDLE, ACTIVE, and HIGH RATE states.", bold_prefix="Rolling-Window Rate Analytics (EPM): ")
    add_bullet("A background watchdog compares server time against the latest packet timestamp. If no telemetry is received for >30 seconds, the UI dynamically alerts operators that the device is OFFLINE.", bold_prefix="Active Heartbeat & Offline Detection: ")
    add_bullet("Operators can review paginated historical transmissions and download the entire telemetry corpus as a comma-separated values (CSV) file with a single click.", bold_prefix="Instant Diagnostic CSV Export: ")

    add_h2("5.3 Comparison: Conventional Systems vs. MagnoTrack")
    add_p("Table 1 summarizes the architectural and operational contrasts between traditional event monitoring methods and the proposed MagnoTrack system.")

    # Table 1: Comparison Matrix
    t1_data = [
        ["Evaluation Parameter", "Manual Log Keeping", "Mechanical Counters", "MagnoTrack IoT Platform"],
        ["Sensing Mechanism", "Visual human observation", "Physical mechanical lever/pawl", "Solid-state A3144 Hall-effect switch"],
        ["Contact Wear & Friction", "N/A (Subject to fatigue)", "High mechanical friction & wear", "Zero mechanical contact (Magnetic flux)"],
        ["Detection Latency", "Hours / Shift-end manual entry", "Instant on dial; hours to report", "< 2.0 seconds end-to-end cloud sync"],
        ["Counting Accuracy", "Vulnerable to missed counts", "Subject to mechanical slip/jam", "100% edge ISR with 50ms debouncing"],
        ["Time-Series Timestamping", "None or coarse hour notes", "Completely absent (Dial only)", "Microsecond server UTC timestamps"],
        ["Remote Accessibility", "None (Requires physical visit)", "None (Requires physical inspection)", "Universal web access via any browser"],
        ["Activity Rate Analytics", "Manual retroactive estimation", "Impossible", "Real-time rolling 60s Events/Min (EPM)"],
        ["Network Resilience", "N/A", "N/A", "Atomic edge counter retains state"],
        ["Health Monitoring", "None", "None", "30s automated heartbeat watchdog"],
        ["Data Exportability", "Tedious manual transcription", "Manual entry into spreadsheets", "One-click CSV telemetry export"]
    ]

    t1 = doc.add_table(rows=len(t1_data), cols=4)
    t1.alignment = WD_TABLE_ALIGNMENT.CENTER
    t1.autofit = False
    set_table_borders(t1, HEX_BORDER)

    col_widths = [Inches(1.5), Inches(1.5), Inches(1.5), Inches(1.77)]

    for row_idx, row in enumerate(t1.rows):
        is_header = (row_idx == 0)
        for col_idx, cell in enumerate(row.cells):
            cell.width = col_widths[col_idx]
            set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
            if is_header:
                set_cell_shading(cell, HEX_NAVY)
            elif row_idx % 2 == 1:
                set_cell_shading(cell, HEX_LIGHT_ROW)
            
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.05
            run = p.add_run(t1_data[row_idx][col_idx])
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
    c1 = cp.add_run("Table 1: ")
    c1.font.bold = True
    c1.font.size = Pt(9.5)
    c1.font.color.rgb = COLOR_NAVY
    c2 = cp.add_run("Comparison Matrix: Conventional Systems vs. MagnoTrack Platform")
    c2.font.italic = True
    c2.font.size = Pt(9.5)
    c2.font.color.rgb = COLOR_SLATE

    print("Part 1 (Sections 1 to 5) generated successfully.")

if __name__ == "__main__":
    print("sections_part1 module loaded.")
