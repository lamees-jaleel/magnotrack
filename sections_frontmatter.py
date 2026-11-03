import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

def add_frontmatter(doc, ctx):
    add_h1 = ctx["add_h1"]
    add_h2 = ctx["add_h2"]
    add_p = ctx["add_p"]
    COLOR_NAVY = ctx["COLOR_NAVY"]
    COLOR_BLUE = ctx["COLOR_BLUE"]
    COLOR_SLATE = ctx["COLOR_SLATE"]
    COLOR_BODY = ctx["COLOR_BODY"]
    COLOR_MUTED = ctx["COLOR_MUTED"]
    set_cell_shading = ctx["set_cell_shading"]
    set_cell_margins = ctx["set_cell_margins"]
    set_table_borders = ctx["set_table_borders"]

    # =========================================================================
    # 1. TITLE / COVER PAGE
    # =========================================================================
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(36)
    p_inst.paragraph_format.space_after = Pt(4)
    r_inst = p_inst.add_run("[COLLEGE / INSTITUTION NAME HERE]\n")
    r_inst.font.name = "Arial"
    r_inst.font.size = Pt(15)
    r_inst.font.bold = True
    r_inst.font.color.rgb = COLOR_NAVY
    
    r_dept = p_inst.add_run("DEPARTMENT OF COMPUTER APPLICATIONS\n[INSTITUTION AFFILIATION & ACCREDITATION DETAILS]")
    r_dept.font.name = "Arial"
    r_dept.font.size = Pt(11)
    r_dept.font.color.rgb = COLOR_SLATE

    # Spacer
    p_sp1 = doc.add_paragraph()
    p_sp1.paragraph_format.space_after = Pt(28)

    # Project Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(8)
    r_title = p_title.add_run("MAGNOTRACK: IOT-BASED MAGNETIC EVENT LOGGING AND ACTIVITY MONITORING SYSTEM")
    r_title.font.name = "Arial"
    r_title.font.size = Pt(18)
    r_title.font.bold = True
    r_title.font.color.rgb = COLOR_BLUE

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(36)
    r_sub = p_sub.add_run("A Project Report Submitted in Partial Fulfillment of the Requirements\nfor the Degree of\n")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(11.5)
    r_sub.font.italic = True
    r_sub.font.color.rgb = COLOR_BODY
    
    r_mca = p_sub.add_run("MASTER OF COMPUTER APPLICATIONS (MCA)")
    r_mca.font.name = "Arial"
    r_mca.font.size = Pt(13)
    r_mca.font.bold = True
    r_mca.font.color.rgb = COLOR_NAVY

    # Student & Guide Details Table
    meta_table = doc.add_table(rows=2, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_table.autofit = False
    
    cell_stu = meta_table.cell(0, 0)
    cell_stu.width = Inches(3.1)
    p_stu = cell_stu.paragraphs[0]
    p_stu.paragraph_format.space_after = Pt(2)
    r1 = p_stu.add_run("Submitted by:\n")
    r1.font.bold = True
    r1.font.size = Pt(10.5)
    r1.font.color.rgb = COLOR_NAVY
    r2 = p_stu.add_run("[STUDENT NAME]\nRegister No: [REGISTER NUMBER]")
    r2.font.size = Pt(10.5)
    r2.font.color.rgb = COLOR_BODY

    cell_guide = meta_table.cell(0, 1)
    cell_guide.width = Inches(3.1)
    p_g = cell_guide.paragraphs[0]
    p_g.paragraph_format.space_after = Pt(2)
    r3 = p_g.add_run("Under the Guidance of:\n")
    r3.font.bold = True
    r3.font.size = Pt(10.5)
    r3.font.color.rgb = COLOR_NAVY
    r4 = p_g.add_run("[GUIDE NAME]\n[GUIDE DESIGNATION]\nDepartment of Computer Applications")
    r4.font.size = Pt(10.5)
    r4.font.color.rgb = COLOR_BODY

    cell_empty = meta_table.cell(1, 0)
    cell_empty.width = Inches(3.1)
    cell_year = meta_table.cell(1, 1)
    cell_year.width = Inches(3.1)

    # Academic Year
    p_yr = doc.add_paragraph()
    p_yr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_yr.paragraph_format.space_before = Pt(48)
    r_yr = p_yr.add_run("ACADEMIC YEAR: 2025 – 2026")
    r_yr.font.name = "Arial"
    r_yr.font.size = Pt(11)
    r_yr.font.bold = True
    r_yr.font.color.rgb = COLOR_NAVY

    doc.add_page_break()

    # =========================================================================
    # 2. BONAFIDE CERTIFICATE
    # =========================================================================
    p_cert_title = doc.add_paragraph()
    p_cert_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cert_title.paragraph_format.space_before = Pt(24)
    p_cert_title.paragraph_format.space_after = Pt(18)
    r_ct = p_cert_title.add_run("BONAFIDE CERTIFICATE")
    r_ct.font.name = "Arial"
    r_ct.font.size = Pt(15)
    r_ct.font.bold = True
    r_ct.font.color.rgb = COLOR_NAVY

    add_p("This is to certify that the project report entitled \"MAGNOTRACK – IOT-BASED MAGNETIC EVENT LOGGING AND ACTIVITY MONITORING SYSTEM\" is a bonafide record of work carried out by [STUDENT NAME] (Register No: [REGISTER NUMBER]) in partial fulfillment of the requirements for the award of the degree of MASTER OF COMPUTER APPLICATIONS (MCA) during the academic year 2025–2026.", space_after=12)

    add_p("The project work embodied in this report has been carried out under our supervision and guidance and has not been submitted elsewhere for the award of any degree, diploma, fellowship, or other similar title.", space_after=36)

    # Signatures Table
    sig_table = doc.add_table(rows=2, cols=2)
    sig_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    sig_table.autofit = False

    c_g_sig = sig_table.cell(0, 0)
    c_g_sig.width = Inches(3.1)
    p1 = c_g_sig.paragraphs[0]
    p1.add_run("______________________________\n").font.color.rgb = COLOR_MUTED
    r = p1.add_run("[GUIDE NAME]\nProject Guide / Assistant Professor\nDepartment of Computer Applications")
    r.font.bold = True
    r.font.size = Pt(10)
    r.font.color.rgb = COLOR_NAVY

    c_h_sig = sig_table.cell(0, 1)
    c_h_sig.width = Inches(3.1)
    p2 = c_h_sig.paragraphs[0]
    p2.add_run("______________________________\n").font.color.rgb = COLOR_MUTED
    r = p2.add_run("[HEAD OF THE DEPARTMENT]\nProfessor & Head of Department\nDepartment of Computer Applications")
    r.font.bold = True
    r.font.size = Pt(10)
    r.font.color.rgb = COLOR_NAVY

    # Examiners Row
    c_ie = sig_table.cell(1, 0)
    c_ie.width = Inches(3.1)
    p3 = c_ie.paragraphs[0]
    p3.paragraph_format.space_before = Pt(36)
    p3.add_run("______________________________\n").font.color.rgb = COLOR_MUTED
    r = p3.add_run("Internal Examiner")
    r.font.bold = True
    r.font.size = Pt(10)
    r.font.color.rgb = COLOR_NAVY

    c_ee = sig_table.cell(1, 1)
    c_ee.width = Inches(3.1)
    p4 = c_ee.paragraphs[0]
    p4.paragraph_format.space_before = Pt(36)
    p4.add_run("______________________________\n").font.color.rgb = COLOR_MUTED
    r = p4.add_run("External Examiner")
    r.font.bold = True
    r.font.size = Pt(10)
    r.font.color.rgb = COLOR_NAVY

    p_loc = doc.add_paragraph()
    p_loc.paragraph_format.space_before = Pt(30)
    r_loc = p_loc.add_run("Place: [CITY / CAMPUS]\nDate: [DD/MM/YYYY]")
    r_loc.font.size = Pt(10)
    r_loc.font.color.rgb = COLOR_SLATE

    doc.add_page_break()

    # =========================================================================
    # 3. DECLARATION
    # =========================================================================
    p_dec_title = doc.add_paragraph()
    p_dec_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_dec_title.paragraph_format.space_before = Pt(24)
    p_dec_title.paragraph_format.space_after = Pt(18)
    r_dt = p_dec_title.add_run("DECLARATION")
    r_dt.font.name = "Arial"
    r_dt.font.size = Pt(15)
    r_dt.font.bold = True
    r_dt.font.color.rgb = COLOR_NAVY

    add_p("I, [STUDENT NAME], student of Master of Computer Applications (MCA) at [COLLEGE / INSTITUTION NAME], bearing Register Number [REGISTER NUMBER], hereby declare that the project entitled \"MAGNOTRACK – IOT-BASED MAGNETIC EVENT LOGGING AND ACTIVITY MONITORING SYSTEM\" submitted by me in partial fulfillment of the requirements for the award of the degree of Master of Computer Applications, is an authentic record of my original research and practical development carried out under the guidance and supervision of [GUIDE NAME], [GUIDE DESIGNATION], Department of Computer Applications.", space_after=12)

    add_p("I further declare that this project work has not previously formed the basis for the award of any Degree, Diploma, Associate Fellowship, or other similar academic recognition from any university or educational institution.", space_after=36)

    p_st_sig = doc.add_paragraph()
    p_st_sig.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = p_st_sig.add_run("______________________________\n[STUDENT NAME]\nRegister No: [REGISTER NUMBER]\nDepartment of Computer Applications")
    r.font.bold = True
    r.font.size = Pt(10)
    r.font.color.rgb = COLOR_NAVY

    doc.add_page_break()

    # =========================================================================
    # 4. ACKNOWLEDGEMENT
    # =========================================================================
    p_ack_title = doc.add_paragraph()
    p_ack_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ack_title.paragraph_format.space_before = Pt(24)
    p_ack_title.paragraph_format.space_after = Pt(18)
    r_at = p_ack_title.add_run("ACKNOWLEDGEMENT")
    r_at.font.name = "Arial"
    r_at.font.size = Pt(15)
    r_at.font.bold = True
    r_at.font.color.rgb = COLOR_NAVY

    add_p("First and foremost, I express my profound gratitude to the Almighty for bestowing the perseverance, wisdom, and health necessary to bring this engineering project to successful fruition.", space_after=8)

    add_p("I express my sincere thanks and respectful gratitude to our esteemed Principal / Director, [PRINCIPAL NAME], for providing an exemplary academic environment, cutting-edge laboratory infrastructure, and constant encouragement.", space_after=8)

    add_p("I extend my deepest gratitude to [HOD NAME], Head of the Department of Computer Applications, for academic leadership, administrative assistance, and continuous support throughout the duration of this Master of Computer Applications curriculum.", space_after=8)

    add_p("I am profoundly indebted to my respected project guide, [GUIDE NAME], [GUIDE DESIGNATION], Department of Computer Applications, for exceptional intellectual guidance, constructive critique, and invaluable technical mentorship during every phase of firmware development, database optimization, and cloud architecture implementation.", space_after=8)

    add_p("I also take this opportunity to convey my heartfelt thanks to all faculty members, technical laboratory assistants, and staff members of the Department of Computer Applications for their timely support, insightful feedback, and assistance with hardware test instruments.", space_after=8)

    add_p("Finally, I express my sincere appreciation to my parents, family members, and fellow classmates for their moral support, understanding, and unending encouragement throughout the execution of this project.", space_after=24)

    p_sig_ack = doc.add_paragraph()
    p_sig_ack.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = p_sig_ack.add_run("[STUDENT NAME]\n(Register No: [REGISTER NUMBER])")
    r.font.bold = True
    r.font.size = Pt(10)
    r.font.color.rgb = COLOR_NAVY

    doc.add_page_break()

    # =========================================================================
    # 5. ABSTRACT
    # =========================================================================
    p_abs_title = doc.add_paragraph()
    p_abs_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_abs_title.paragraph_format.space_before = Pt(24)
    p_abs_title.paragraph_format.space_after = Pt(18)
    r_ab = p_abs_title.add_run("ABSTRACT")
    r_ab.font.name = "Arial"
    r_ab.font.size = Pt(15)
    r_ab.font.bold = True
    r_ab.font.color.rgb = COLOR_NAVY

    add_p("The rapid proliferation of the Internet of Things (IoT) in industrial automation, security enclosures, and cyber-physical infrastructure necessitates reliable, real-time telemetry solutions for monitoring physical proximity and repetitive mechanical actions. Traditional magnetic event monitoring relies predominantly on manual inspection or offline mechanical counters, resulting in data latency, lack of centralized visibility, vulnerability to human recording errors, and the inability to conduct longitudinal analytics.", space_after=8)

    add_p("To overcome these fundamental limitations, this project designs, implements, and evaluates MagnoTrack – an end-to-end, IoT-based magnetic event logging and activity monitoring system. The edge sensing layer integrates an Espressif ESP32 32-bit dual-core microcontroller interfaced with an A3144 Hall-effect digital switch module (HW-477) and dual permanent magnets. The A3144 transducer operates as an active-LOW digital magnetic switch, pulling its digital output (DO) pin from 3.3V to 0V when exposed to the South magnetic pole. An interrupt-driven hardware routine on GPIO 27 captures digital falling edges and employs a 50 ms microsecond-level software debouncing filter to eliminate parasitic contact bounce. The edge firmware calculates cumulative detection events and dispatches telemetry packets containing device identification, cumulative count, instantaneous sensor state, and microcontroller uptime over Wi-Fi using HTTP POST requests.", space_after=8)

    add_p("The cloud backend is engineered using Python FastAPI and Uvicorn, implementing high-performance asynchronous REST endpoints. Inbound payloads undergo rigorous schema validation via Pydantic models before being persisted in a relational PostgreSQL 16 database managed through SQLAlchemy 2.0 ORM with connection pooling. A responsive, single-page web dashboard visualizes operational metrics through five high-contrast Key Performance Indicator (KPI) cards: Total Magnetic Events, Current Sensor Status, Events Per Minute (EPM) calculated over a rolling 60-second sliding window, Last Event Timestamp, and Device Connection State with a 30-second offline watchdog. Dynamic Chart.js visualizations plot cumulative event progression and telemetry rate deltas in real time, accompanied by a paginated history table with instant CSV export capabilities.", space_after=8)

    add_p("Comprehensive automated unit and integration testing via pytest verifies 100% test pass rates across database CRUD operations, schema bounds enforcement, offline detection logic, and responsive UI serving. The resulting platform delivers a robust, cost-effective, and highly scalable architecture suitable for industrial machinery cycle counting, door and hatch position monitoring, and academic IoT pedagogy.", space_after=12)

    p_kw = doc.add_paragraph()
    p_kw.paragraph_format.space_after = Pt(12)
    r_kw = p_kw.add_run("Keywords: ")
    r_kw.font.name = "Arial"
    r_kw.font.bold = True
    r_kw.font.size = Pt(10)
    r_kw.font.color.rgb = COLOR_NAVY
    
    r_words = p_kw.add_run("Internet of Things (IoT), ESP32 Microcontroller, A3144 Hall-Effect Sensor, Digital Magnetic Switch, Hardware Interrupt ISR, FastAPI, PostgreSQL, Chart.js, Real-Time Telemetry.")
    r_words.font.name = "Calibri"
    r_words.font.size = Pt(10)
    r_words.font.italic = True
    r_words.font.color.rgb = COLOR_SLATE

    doc.add_page_break()

    # =========================================================================
    # 6. TABLE OF CONTENTS
    # =========================================================================
    p_toc_title = doc.add_paragraph()
    p_toc_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_toc_title.paragraph_format.space_before = Pt(24)
    p_toc_title.paragraph_format.space_after = Pt(14)
    r_tc = p_toc_title.add_run("TABLE OF CONTENTS")
    r_tc.font.name = "Arial"
    r_tc.font.size = Pt(15)
    r_tc.font.bold = True
    r_tc.font.color.rgb = COLOR_NAVY

    toc_items = [
        ("BONAFIDE CERTIFICATE", "ii"),
        ("DECLARATION", "iii"),
        ("ACKNOWLEDGEMENT", "iv"),
        ("ABSTRACT", "v"),
        ("LIST OF FIGURES", "viii"),
        ("LIST OF TABLES", "ix"),
        ("1. INTRODUCTION", "1"),
        ("    1.1 Introduction to IoT in Industrial & Physical Sensing", "1"),
        ("    1.2 Importance and Relevance of Magnetic Event Detection", "2"),
        ("    1.3 Problem Addressed by MagnoTrack", "2"),
        ("    1.4 Overview of the Proposed MagnoTrack Solution", "3"),
        ("2. AIM OF THE PROJECT", "4"),
        ("3. OBJECTIVES", "4"),
        ("4. EXISTING SYSTEM", "5"),
        ("    4.1 Conventional Manual and Mechanical Event Logging", "5"),
        ("    4.2 Limitations and Vulnerabilities of Existing Systems", "5"),
        ("5. PROPOSED SYSTEM", "7"),
        ("    5.1 System Concept and Architectural Overview", "7"),
        ("    5.2 Key Capabilities and Innovation Highlights", "7"),
        ("    5.3 Comparison: Conventional Systems vs. MagnoTrack", "8"),
        ("6. SYSTEM ARCHITECTURE", "9"),
        ("    6.1 High-Level Multi-Tier System Architecture", "9"),
        ("    6.2 Hardware Architecture Overview", "10"),
        ("    6.3 Software Architecture Overview", "10"),
        ("    6.4 Perception & Device Layer", "11"),
        ("    6.5 Network & Communication Layer", "11"),
        ("    6.6 Cloud Backend & API Ingestion Layer", "11"),
        ("    6.7 Relational Database Layer", "12"),
        ("    6.8 Presentation & Visualization Dashboard Layer", "12"),
        ("7. HARDWARE COMPONENTS", "13"),
        ("    7.1 ESP32 Development Board (ESP-WROOM-32)", "13"),
        ("    7.2 A3144 Hall-Effect Sensor Module (HW-477 PCB)", "14"),
        ("    7.3 Permanent Magnets and Polarity Characteristics", "15"),
        ("    7.4 Solderless Breadboard and Interconnect Jumper Wires", "15"),
        ("    7.5 Power Supply and USB Programming Interface", "16"),
        ("    7.6 Prototype Bill of Materials (BOM) Table", "16"),
        ("8. SOFTWARE COMPONENTS", "17"),
        ("    8.1 Arduino IDE 2.3.10 and ESP32 Arduino Core", "17"),
        ("    8.2 Python FastAPI Asynchronous Web Framework", "17"),
        ("    8.3 PostgreSQL 16 Relational Database Engine", "18"),
        ("    8.4 Frontend Technologies: HTML5, Modern CSS3, and ES6 JavaScript", "18"),
        ("    8.5 Chart.js Dynamic Data Visualization Engine", "19"),
        ("    8.6 Docker Containerization and Docker Compose", "19"),
        ("    8.7 Render Cloud Platform as a Service (PaaS)", "20"),
        ("9. WORKING PRINCIPLE", "21"),
        ("    9.1 Comprehensive Step-by-Step Operational Sequence", "21"),
        ("    9.2 Detailed Breakdown of the 10-Stage Lifecycle", "21"),
        ("10. CONNECTION DETAILS", "25"),
        ("    10.1 Hardware Wiring Configuration & Pin Mapping", "25"),
        ("    10.2 Pin Connection Specification Table", "25"),
        ("    10.3 Technical Justification of GPIO 27 & Internal Pull-Up Resistor", "26"),
        ("    10.4 Hall-Effect Sensing Distinction: Digital Switch vs. Analog Transducer", "26"),
        ("    10.5 Polarity Sensitivity and Magnetic Orientation Requirements", "27"),
        ("11. ESP32 FIRMWARE IMPLEMENTATION", "28"),
        ("    11.1 Firmware Architecture and Modular Execution Model", "28"),
        ("    11.2 Edge Detection via Hardware Interrupt Service Routine (ISR)", "28"),
        ("    11.3 Microsecond-Level Software Debounce Algorithm", "29"),
        ("    11.4 Atomic Counter Synchronization with FreeRTOS Mutex", "29"),
        ("    11.5 Wi-Fi Connection Management & Resilience Strategy", "30"),
        ("    11.6 HTTP POST Client Implementation & JSON Formatting", "30"),
        ("    11.7 Code Walkthrough and Representative Excerpts", "31"),
        ("12. BACKEND AND DATABASE IMPLEMENTATION", "33"),
        ("    12.1 FastAPI Framework Architecture & ASGI Server Pipeline", "33"),
        ("    12.2 Lifespan Management & Automatic Table Initialization", "33"),
        ("    12.3 REST API Endpoints Specification", "34"),
        ("    12.4 Pydantic Schemas and Telemetry Validation Rules", "35"),
        ("    12.5 SQLAlchemy 2.0 ORM Engine & Connection Pooling Strategy", "36"),
        ("    12.6 PostgreSQL Relational Schema (`sensor_readings`)", "37"),
        ("    12.7 Rolling-Window Rate Analytics (Events Per Minute Calculation)", "38"),
        ("13. CLOUD AND CONTAINER HOSTING", "39"),
        ("    13.1 Multi-Stage Production Docker Containerization", "39"),
        ("    13.2 Local Orchestration with Docker Compose", "40"),
        ("    13.3 Production Deployment on Render Cloud Platform", "40"),
        ("    13.4 Environment Variables & PostgreSQL Connection String Handling", "41"),
        ("    13.5 Network Traversal: Local LAN vs. Cloud HTTPS Endpoint", "42"),
        ("14. WEB DASHBOARD", "43"),
        ("    14.1 Dashboard Architectural Design Philosophy", "43"),
        ("    14.2 Detailed Breakdown of Key Performance Indicator (KPI) Cards", "43"),
        ("    14.3 Dynamic Time-Series Visualizations with Chart.js", "45"),
        ("    14.4 Event History Table with Search and Pagination", "46"),
        ("    14.5 CSV Telemetry Export Engine", "46"),
        ("    14.6 System Information & Hardware Diagnostic Panel", "47"),
        ("15. RESULTS AND TESTING", "48"),
        ("    15.1 Academic Testing Methodology", "48"),
        ("    15.2 Unit & Integration Testing: Automated Pytest Suite", "48"),
        ("    15.3 Sensor Edge Detection & Interrupt Debounce Verification", "49"),
        ("    15.4 ESP32 Network Connectivity & Latency Benchmarks", "50"),
        ("    15.5 REST API Ingestion & Pydantic Boundary Verification", "50"),
        ("    15.6 PostgreSQL Persistence & Index Query Performance", "51"),
        ("    15.7 Dashboard Polling & Chart Re-rendering Verification", "51"),
        ("    15.8 Device Offline Watchdog Verification (30-second Rule)", "52"),
        ("    15.9 Consolidated Test Verification Matrix Table", "52"),
        ("    15.10 Physical Prototype Verification Notice", "53"),
        ("16. ADVANTAGES", "54"),
        ("17. APPLICATIONS", "55"),
        ("18. FUTURE ENHANCEMENTS", "57"),
        ("19. CONCLUSION", "59"),
        ("20. PROJECT DESIGN AND DATA FLOW", "60"),
        ("21. BLOCK DIAGRAM", "62"),
        ("22. FINAL PRODUCT AND PRESENTATION", "64"),
        ("23. DASHBOARD SCREENSHOTS", "66"),
        ("REFERENCES", "69")
    ]

    toc_table = doc.add_table(rows=len(toc_items), cols=2)
    toc_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    toc_table.autofit = False

    for i, (title, page) in enumerate(toc_items):
        cell_t = toc_table.cell(i, 0)
        cell_t.width = Inches(5.4)
        p = cell_t.paragraphs[0]
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(title)
        r.font.name = "Calibri"
        r.font.size = Pt(9.5)
        if not title.startswith("    "):
            r.font.bold = True
            r.font.color.rgb = COLOR_NAVY
        else:
            r.font.color.rgb = COLOR_BODY

        cell_p = toc_table.cell(i, 1)
        cell_p.width = Inches(0.8)
        p_p = cell_p.paragraphs[0]
        p_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p_p.paragraph_format.space_after = Pt(2)
        rp = p_p.add_run(page)
        rp.font.name = "Calibri"
        rp.font.size = Pt(9.5)
        rp.font.color.rgb = COLOR_SLATE

    doc.add_page_break()

    # =========================================================================
    # 7. LIST OF FIGURES
    # =========================================================================
    p_lof_title = doc.add_paragraph()
    p_lof_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_lof_title.paragraph_format.space_before = Pt(24)
    p_lof_title.paragraph_format.space_after = Pt(14)
    r_lf = p_lof_title.add_run("LIST OF FIGURES")
    r_lf.font.name = "Arial"
    r_lf.font.size = Pt(15)
    r_lf.font.bold = True
    r_lf.font.color.rgb = COLOR_NAVY

    figures_list = [
        ("Figure 1", "High-Level Five-Tier System Architecture of MagnoTrack Monitoring Platform", "9"),
        ("Figure 2", "Functional Block Diagram of MagnoTrack System Modules and Interconnections", "63"),
        ("Figure 3", "MagnoTrack Server Architecture, REST Endpoints, and Database Schema", "37"),
        ("Figure 4", "MagnoTrack Prototype Hardware Components, Sensors, and Specifications", "13"),
        ("Figure 5", "MagnoTrack Prototype Implementation Verification, Hardware Testing, and Telemetry Records", "65"),
        ("Figure 6", "MagnoTrack Dual-Sided Operational Flowchart (Firmware ISR vs. Cloud Analytics)", "24"),
        ("Figure 7", "Hardware Wiring & Pinout Schematic (A3144 HW-477 to ESP32 DevKit)", "25"),
        ("Figure 8", "End-to-End Project Data Flow Pipeline (Sensor to Web Dashboard)", "61"),
        ("Figure 9", "MagnoTrack Live Web Dashboard Overview (KPI Cards, Real-Time Chart, and Telemetry Stream)", "66"),
        ("Figure 10", "Event History Tab with Tabular Pagination and CSV Telemetry Export", "67"),
        ("Figure 11", "System Information Tab Displaying Hardware Pinouts, REST Endpoints, and Diagnostic Health", "68")
    ]

    lof_table = doc.add_table(rows=len(figures_list), cols=3)
    lof_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    lof_table.autofit = False

    for i, (f_num, f_desc, f_page) in enumerate(figures_list):
        c0 = lof_table.cell(i, 0)
        c0.width = Inches(1.1)
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_after = Pt(3)
        r0 = p0.add_run(f_num)
        r0.font.bold = True
        r0.font.size = Pt(9.5)
        r0.font.color.rgb = COLOR_NAVY

        c1 = lof_table.cell(i, 1)
        c1.width = Inches(4.3)
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_after = Pt(3)
        r1 = p1.add_run(f_desc)
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = COLOR_BODY

        c2 = lof_table.cell(i, 2)
        c2.width = Inches(0.8)
        p2 = c2.paragraphs[0]
        p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p2.paragraph_format.space_after = Pt(3)
        r2 = p2.add_run(f_page)
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = COLOR_SLATE

    doc.add_page_break()

    # =========================================================================
    # 8. LIST OF TABLES
    # =========================================================================
    p_lot_title = doc.add_paragraph()
    p_lot_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_lot_title.paragraph_format.space_before = Pt(24)
    p_lot_title.paragraph_format.space_after = Pt(14)
    r_lt = p_lot_title.add_run("LIST OF TABLES")
    r_lt.font.name = "Arial"
    r_lt.font.size = Pt(15)
    r_lt.font.bold = True
    r_lt.font.color.rgb = COLOR_NAVY

    tables_list = [
        ("Table 1", "Comparison Matrix: Conventional Systems vs. MagnoTrack Platform", "8"),
        ("Table 2", "Prototype Hardware Bill of Materials (BOM) & Electrical Specifications", "16"),
        ("Table 3", "Hardware Wiring & Electrical Pin Connection Specification", "25"),
        ("Table 4", "MagnoTrack REST API Endpoints Specification and Data Payloads", "34"),
        ("Table 5", "PostgreSQL Relational Schema Definition (`sensor_readings` table)", "37"),
        ("Table 6", "Automated Pytest Suite Test Verification Matrix and Execution Results", "53")
    ]

    lot_table = doc.add_table(rows=len(tables_list), cols=3)
    lot_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    lot_table.autofit = False

    for i, (t_num, t_desc, t_page) in enumerate(tables_list):
        c0 = lot_table.cell(i, 0)
        c0.width = Inches(1.1)
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_after = Pt(3)
        r0 = p0.add_run(t_num)
        r0.font.bold = True
        r0.font.size = Pt(9.5)
        r0.font.color.rgb = COLOR_NAVY

        c1 = lot_table.cell(i, 1)
        c1.width = Inches(4.3)
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_after = Pt(3)
        r1 = p1.add_run(t_desc)
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = COLOR_BODY

        c2 = lot_table.cell(i, 2)
        c2.width = Inches(0.8)
        p2 = c2.paragraphs[0]
        p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p2.paragraph_format.space_after = Pt(3)
        r2 = p2.add_run(t_page)
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = COLOR_SLATE

    doc.add_page_break()
    print("Frontmatter generated successfully.")

if __name__ == "__main__":
    print("sections_frontmatter module loaded.")
