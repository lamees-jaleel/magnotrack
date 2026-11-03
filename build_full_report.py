import os
import sys
import subprocess
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

from sections_frontmatter import add_frontmatter
from sections_part1 import add_part1
from sections_part2 import add_part2
from sections_part3 import add_part3
from sections_part4 import add_part4

def main():
    print("=" * 60)
    print("MAGNOTRACK ACADEMIC REPORT BUILDER")
    print("=" * 60)

    doc = docx.Document()

    # Configure A4 Page Setup and Margins
    for section in doc.sections:
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
        # Configure Header
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("MagnoTrack – IoT Magnetic Event Logging & Monitoring System")
        hrun.font.name = "Calibri"
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = RGBColor(100, 116, 139)

    # Color Palette Definitions
    COLOR_NAVY = RGBColor(15, 23, 42)       # Slate 900
    COLOR_BLUE = RGBColor(30, 64, 175)      # Blue 800
    COLOR_SLATE = RGBColor(51, 65, 85)      # Slate 700
    COLOR_BODY = RGBColor(30, 41, 59)       # Slate 800
    COLOR_MUTED = RGBColor(100, 116, 139)   # Slate 500
    HEX_NAVY = "0F172A"
    HEX_LIGHT_ROW = "F8FAFC"
    HEX_BORDER = "CBD5E1"
    HEX_CALLOUT_BG = "EFF6FF"
    HEX_CALLOUT_BORDER = "3B82F6"
    HEX_NOTE_BG = "FEF3C7"
    HEX_NOTE_BORDER = "F59E0B"

    # Helper: Set Cell Shading
    def set_cell_shading(cell, color_hex):
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
        cell._tc.get_or_add_tcPr().append(shd)

    # Helper: Set Cell Margins (Padding)
    def set_cell_margins(cell, top=100, bottom=100, left=120, right=120):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = OxmlElement('w:tcMar')
        for m_name, m_val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
            node = OxmlElement(f'w:{m_name}')
            node.set(qn('w:w'), str(m_val))
            node.set(qn('w:type'), 'dxa')
            tcMar.append(node)
        tcPr.append(tcMar)

    # Helper: Table Borders
    def set_table_borders(table, color="CBD5E1"):
        tblPr = table._tbl.tblPr
        borders = parse_xml(
            f'<w:tblBorders {nsdecls("w")}>'
            f'  <w:top w:val="single" w:sz="6" w:space="0" w:color="{color}"/>'
            f'  <w:bottom w:val="single" w:sz="6" w:space="0" w:color="{color}"/>'
            f'  <w:left w:val="none"/>'
            f'  <w:right w:val="none"/>'
            f'  <w:insideH w:val="single" w:sz="4" w:space="0" w:color="{color}"/>'
            f'  <w:insideV w:val="none"/>'
            f'</w:tblBorders>'
        )
        tblPr.append(borders)

    # Helper: Add Heading 1
    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Arial"
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = COLOR_NAVY
        return p

    # Helper: Add Heading 2
    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Arial"
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = COLOR_BLUE
        return p

    # Helper: Add Heading 3
    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Arial"
        run.font.size = Pt(10.5)
        run.font.bold = True
        run.font.color.rgb = COLOR_SLATE
        return p

    # Helper: Add Body Paragraph
    def add_p(text, bold_prefix=None, space_after=5):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            brun = p.add_run(bold_prefix)
            brun.font.name = "Calibri"
            brun.font.size = Pt(11)
            brun.font.bold = True
            brun.font.color.rgb = COLOR_NAVY
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(11)
        run.font.color.rgb = COLOR_BODY
        return p

    # Helper: Add Bullet Item
    def add_bullet(text, bold_prefix=None):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            brun = p.add_run(bold_prefix)
            brun.font.name = "Calibri"
            brun.font.size = Pt(10.5)
            brun.font.bold = True
            brun.font.color.rgb = COLOR_NAVY
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(10.5)
        run.font.color.rgb = COLOR_BODY
        return p

    # Helper: Add Callout Note Box
    def add_callout(title, text, is_warning=False):
        table = doc.add_table(rows=1, cols=1)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = table.cell(0, 0)
        cell.width = Inches(6.27)
        bg_col = HEX_NOTE_BG if is_warning else HEX_CALLOUT_BG
        border_col = HEX_NOTE_BORDER if is_warning else HEX_CALLOUT_BORDER
        set_cell_shading(cell, bg_col)
        set_cell_margins(cell, top=100, bottom=100, left=160, right=140)
        
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'  <w:left w:val="single" w:sz="24" w:space="0" w:color="{border_col}"/>'
            f'  <w:top w:val="none"/>'
            f'  <w:bottom w:val="none"/>'
            f'  <w:right w:val="none"/>'
            f'</w:tcBorders>'
        )
        tcPr.append(borders)
        
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        trun = p.add_run(f"[{title}] ")
        trun.font.name = "Arial"
        trun.font.size = Pt(9.5)
        trun.font.bold = True
        trun.font.color.rgb = RGBColor(180, 83, 9) if is_warning else RGBColor(29, 78, 216)
        
        brun = p.add_run(text)
        brun.font.name = "Calibri"
        brun.font.size = Pt(9.5)
        brun.font.color.rgb = RGBColor(120, 53, 15) if is_warning else RGBColor(30, 58, 138)
        
        sp = doc.add_paragraph()
        sp.paragraph_format.space_after = Pt(4)

    # Helper: Add Code Block
    def add_code_block(code_text):
        table = doc.add_table(rows=1, cols=1)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = table.cell(0, 0)
        cell.width = Inches(6.27)
        set_cell_shading(cell, "F1F5F9")
        set_cell_margins(cell, top=80, bottom=80, left=140, right=140)
        
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'  <w:left w:val="single" w:sz="6" w:space="0" w:color="CBD5E1"/>'
            f'  <w:top w:val="single" w:sz="6" w:space="0" w:color="CBD5E1"/>'
            f'  <w:bottom w:val="single" w:sz="6" w:space="0" w:color="CBD5E1"/>'
            f'  <w:right w:val="single" w:sz="6" w:space="0" w:color="CBD5E1"/>'
            f'</w:tcBorders>'
        )
        tcPr.append(borders)
        
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.0
        run = p.add_run(code_text.strip())
        run.font.name = "Consolas"
        run.font.size = Pt(8.5)
        run.font.color.rgb = RGBColor(15, 23, 42)
        
        sp = doc.add_paragraph()
        sp.paragraph_format.space_after = Pt(4)

    # Helper: Add Centered Image with Caption
    def add_figure(image_path, fig_num, caption_text, width_inches=6.0):
        if os.path.exists(image_path):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(8)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.keep_with_next = True
            run = p.add_run()
            run.add_picture(image_path, width=Inches(width_inches))
            
            cp = doc.add_paragraph()
            cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            cp.paragraph_format.space_after = Pt(12)
            crun1 = cp.add_run(f"Figure {fig_num}: ")
            crun1.font.name = "Arial"
            crun1.font.size = Pt(9.5)
            crun1.font.bold = True
            crun1.font.color.rgb = COLOR_NAVY
            
            crun2 = cp.add_run(caption_text)
            crun2.font.name = "Calibri"
            crun2.font.size = Pt(9.5)
            crun2.font.italic = True
            crun2.font.color.rgb = COLOR_SLATE

    ctx = {
        "set_cell_shading": set_cell_shading,
        "set_cell_margins": set_cell_margins,
        "set_table_borders": set_table_borders,
        "add_h1": add_h1,
        "add_h2": add_h2,
        "add_h3": add_h3,
        "add_p": add_p,
        "add_bullet": add_bullet,
        "add_callout": add_callout,
        "add_code_block": add_code_block,
        "add_figure": add_figure,
        "COLOR_NAVY": COLOR_NAVY,
        "COLOR_BLUE": COLOR_BLUE,
        "COLOR_SLATE": COLOR_SLATE,
        "COLOR_BODY": COLOR_BODY,
        "COLOR_MUTED": COLOR_MUTED,
        "HEX_NAVY": HEX_NAVY,
        "HEX_LIGHT_ROW": HEX_LIGHT_ROW,
        "HEX_BORDER": HEX_BORDER
    }

    # Assembling sections
    print("Building Frontmatter...")
    add_frontmatter(doc, ctx)

    print("Building Part 1 (Sections 1-5)...")
    add_part1(doc, ctx)

    print("Building Part 2 (Sections 6-10)...")
    add_part2(doc, ctx)

    print("Building Part 3 (Sections 11-15)...")
    add_part3(doc, ctx)

    print("Building Part 4 (Sections 16-23 + References)...")
    add_part4(doc, ctx)

    docx_out = "MagnoTrack_Project_Report.docx"
    pdf_out = "MagnoTrack_Project_Report.pdf"

    print(f"Saving Word report: {docx_out} ...")
    doc.save(docx_out)
    print("Word document saved successfully!")

    # Convert to PDF using Microsoft Word COM Automation
    print(f"Converting {docx_out} to {pdf_out} via Microsoft Word COM automation...")
    cmd = [
        "powershell",
        "-ExecutionPolicy", "Bypass",
        "-File", ".\\convert_to_pdf.ps1",
        "-docxPath", docx_out,
        "-pdfPath", pdf_out
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    print("PowerShell Output:", res.stdout)
    if res.stderr:
        print("PowerShell Error:", res.stderr)

    if os.path.exists(pdf_out):
        print(f"SUCCESS: {pdf_out} generated successfully!")
        pdf_size = os.path.getsize(pdf_out)
        print(f"PDF Size: {pdf_size / 1024:.1f} KB")
    else:
        print(f"ERROR: {pdf_out} was not created.")

if __name__ == "__main__":
    main()
