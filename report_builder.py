"""
Premium Academic Capstone Report & Execution Manual Generator
For Lovely Professional University - School of Computer Science & Engineering
Courses: INT422 (Deep Learning) & INT333 (DevOps Advance Configuration Management)
Students:
- Mohit Raj Deo (12323329 | Roll: 62)
- Akash Choudhary (12301625 | Roll: 11)
- Saif Siddique (12308813 | Roll: 44)
"""

import os
import sys
import shutil
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=120, bottom=120, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'''
        <w:tcMar {nsdecls("w")}>
            <w:top w:w="{top}" w:type="dxa"/>
            <w:bottom w:w="{bottom}" w:type="dxa"/>
            <w:left w:w="{left}" w:type="dxa"/>
            <w:right w:w="{right}" w:type="dxa"/>
        </w:tcMar>
    ''')
    tcPr.append(tcMar)

def set_table_borders(table, color="D3D3D3"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'''
        <w:tblBorders {nsdecls("w")}>
            <w:top w:val="single" w:sz="6" w:space="0" w:color="{color}"/>
            <w:bottom w:val="single" w:sz="8" w:space="0" w:color="{color}"/>
            <w:insideH w:val="single" w:sz="4" w:space="0" w:color="{color}"/>
            <w:insideV w:val="none"/>
            <w:left w:val="none"/>
            <w:right w:val="none"/>
        </w:tblBorders>
    ''')
    tblPr.append(borders)

class AcademicReportBuilder:
    def __init__(self, title, subtitle, student_name, reg_no, roll_no, course_code, course_name, guide_name="Ms. Manpreet Kaur"):
        self.doc = docx.Document()
        self.title = title
        self.subtitle = subtitle
        self.student_name = student_name
        self.reg_no = reg_no
        self.roll_no = roll_no
        self.course_code = course_code
        self.course_name = course_name
        self.guide_name = guide_name
        self._setup_page()

    def _setup_page(self):
        for section in self.doc.sections:
            section.top_margin = Inches(1.0)
            section.bottom_margin = Inches(1.0)
            section.left_margin = Inches(1.0)
            section.right_margin = Inches(1.0)
            section.page_width = Inches(8.5)
            section.page_height = Inches(11.0)

    def add_title_page(self):
        p0 = self.doc.add_paragraph()
        p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r0 = p0.add_run("LOVELY PROFESSIONAL UNIVERSITY\n")
        r0.bold = True
        r0.font.size = Pt(16)
        r0.font.name = "Arial"
        r0.font.color.rgb = RGBColor(16, 44, 87) # Navy

        r0_sub = p0.add_run("School of Computer Science and Engineering\nPhagwara, Punjab (India) - 144411\n\n")
        r0_sub.font.size = Pt(11)
        r0_sub.font.name = "Arial"
        r0_sub.font.color.rgb = RGBColor(100, 100, 100)

        p_rep = self.doc.add_paragraph()
        p_rep.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_rep = p_rep.add_run("FINAL CAPSTONE PROJECT REPORT\n")
        r_rep.bold = True
        r_rep.font.size = Pt(13)
        r_rep.font.name = "Arial"
        r_rep.font.color.rgb = RGBColor(180, 50, 50) # Dark red

        r_course = p_rep.add_run(f"Course: {self.course_code} - {self.course_name}\n\n")
        r_course.font.size = Pt(12)
        r_course.bold = True
        r_course.font.name = "Arial"

        p_title = self.doc.add_paragraph()
        p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_title = p_title.add_run(f"{self.title}\n")
        r_title.bold = True
        r_title.font.size = Pt(20)
        r_title.font.name = "Arial"
        r_title.font.color.rgb = RGBColor(16, 44, 87)

        if self.subtitle:
            r_sub = p_title.add_run(f"{self.subtitle}\n\n\n")
            r_sub.font.size = Pt(12)
            r_sub.font.italic = True
            r_sub.font.name = "Arial"
            r_sub.font.color.rgb = RGBColor(60, 60, 60)

        p_by = self.doc.add_paragraph()
        p_by.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_by = p_by.add_run("Submitted By:\n")
        r_by.font.size = Pt(11)
        r_by.font.italic = True
        
        r_stu = p_by.add_run(f"{self.student_name}\n")
        r_stu.bold = True
        r_stu.font.size = Pt(13)
        r_stu.font.color.rgb = RGBColor(20, 20, 20)

        r_id = p_by.add_run(f"Registration Number: {self.reg_no}\nRoll Number: {self.roll_no}\nB.Tech Computer Science & Engineering\n\n")
        r_id.font.size = Pt(11)

        r_guide_lbl = p_by.add_run("Under the Guidance of:\n")
        r_guide_lbl.font.size = Pt(11)
        r_guide_lbl.font.italic = True

        r_guide = p_by.add_run(f"{self.guide_name}\nAssistant Professor\nSchool of Computer Science & Engineering\nLovely Professional University\n\n")
        r_guide.bold = True
        r_guide.font.size = Pt(12)

        r_date = p_by.add_run("Academic Session: 2024–2025 / 2026–2027\nNovember 2026")
        r_date.font.size = Pt(10)
        r_date.font.color.rgb = RGBColor(120, 120, 120)

        self.doc.add_page_break()

    def add_certificate(self):
        h = self.doc.add_paragraph()
        h.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = h.add_run("CERTIFICATE OF ORIGINALITY")
        r.bold = True
        r.font.size = Pt(16)
        r.font.name = "Arial"
        r.font.color.rgb = RGBColor(16, 44, 87)

        self.doc.add_paragraph()
        p = self.doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.3
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.add_run(
            f"This is to certify that the capstone project entitled "
            f"\"{self.title}\" submitted by {self.student_name} (Registration No: {self.reg_no}, "
            f"Roll No: {self.roll_no}) in partial fulfillment of the requirements for the award of the degree of "
            f"Bachelor of Technology in Computer Science and Engineering for the course {self.course_code}: "
            f"{self.course_name} at Lovely Professional University, Phagwara, Punjab, is an authentic record of "
            f"the candidate's own work carried out under my personal supervision and academic guidance.\n\n"
            f"To the best of my knowledge and technical verification, the matter embodied in this comprehensive "
            f"report has not been submitted to any other University or Institute for the award of any degree, diploma, "
            f"or academic credential. The system implements production-grade microservices, declarative infrastructure "
            f"specifications, verified observability matrices, and standalone user interfaces compliant with university standards."
        )

        p_sig = self.doc.add_paragraph()
        p_sig.paragraph_format.line_spacing = 1.3
        p_sig.add_run("\n\n\n\n")
        p_sig.add_run("_____________________________________\t\t\t_____________________________________\n")
        p_sig.add_run(f"{self.guide_name}\t\t\tHead of Department\n")
        p_sig.add_run("Assistant Professor (Project Guide)\t\t\tSchool of Computer Science & Engineering\n")
        p_sig.add_run("School of Computer Science & Engineering\t\tLovely Professional University\n")
        p_sig.add_run("Lovely Professional University, Punjab\n")

        self.doc.add_page_break()

    def add_declaration(self):
        h = self.doc.add_paragraph()
        h.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = h.add_run("CANDIDATE DECLARATION")
        r.bold = True
        r.font.size = Pt(16)
        r.font.name = "Arial"
        r.font.color.rgb = RGBColor(16, 44, 87)

        self.doc.add_paragraph()
        p = self.doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.3
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.add_run(
            f"I hereby declare that the capstone project work entitled \"{self.title}\" is an authentic record of "
            f"my own original work conducted under the guidance of {self.guide_name}, Assistant Professor, School of Computer "
            f"Science and Engineering, Lovely Professional University, Phagwara, Punjab.\n\n"
            f"I confirm that:\n"
            f"1. The codebase, architectural models, declarative configurations, and empirical evaluation metrics reported herein "
            f"are genuine results of my independent investigation and implementation.\n"
            f"2. All literature sources, third-party libraries (FastAPI, React, Vite, PyTorch, Scikit-Learn, Terraform, Puppet, "
            f"Nagios Core), and research papers cited in this document have been duly acknowledged in the references in accordance with IEEE formatting standards.\n"
            f"3. No portion of this technical report or associated source code has been fabricated or submitted previously for any other degree or certification."
        )

        p_sig = self.doc.add_paragraph()
        p_sig.paragraph_format.line_spacing = 1.3
        p_sig.add_run("\n\n\n\n")
        p_sig.add_run("Date: 15th November 2026\t\t\t\t_____________________________________\n")
        p_sig.add_run(f"Place: Phagwara, Punjab\t\t\t\t{self.student_name}\n")
        p_sig.add_run(f"\t\t\t\t\t\tRegistration No: {self.reg_no}\n")
        p_sig.add_run(f"\t\t\t\t\t\tRoll No: {self.roll_no}\n")

        self.doc.add_page_break()

    def add_acknowledgement(self):
        h = self.doc.add_paragraph()
        h.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = h.add_run("ACKNOWLEDGEMENT")
        r.bold = True
        r.font.size = Pt(16)
        r.font.name = "Arial"
        r.font.color.rgb = RGBColor(16, 44, 87)

        self.doc.add_paragraph()
        p = self.doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.3
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.add_run(
            f"I take this opportunity to express my profound gratitude and deep indebtedness to my project guide, "
            f"{self.guide_name}, Assistant Professor, School of Computer Science and Engineering, Lovely Professional University, "
            f"for her insightful supervision, continuous intellectual encouragement, and meticulous technical guidance throughout "
            f"the design and realization of this capstone project.\n\n"
            f"I would also like to extend my heartfelt appreciation to the Head of the Department and the faculty members of the "
            f"School of Computer Science and Engineering for providing the state-of-the-art computational infrastructure, laboratories, "
            f"and high-performance environments that facilitated the training of deep learning models, orchestration of containerized "
            f"clusters, and execution of automated chaos engineering test suites.\n\n"
            f"Finally, I convey my warmest gratitude to my peers, family, and friends whose unwavering moral support and constructive "
            f"discussions have been invaluable in steering this ambitious enterprise to a successful completion."
        )

        p_sig = self.doc.add_paragraph()
        p_sig.add_run("\n\n")
        p_sig.add_run(f"{self.student_name}\nRegistration No: {self.reg_no} | Roll No: {self.roll_no}")

        self.doc.add_page_break()

    def add_abstract(self, text, keywords):
        h = self.doc.add_paragraph()
        h.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = h.add_run("ABSTRACT")
        r.bold = True
        r.font.size = Pt(16)
        r.font.name = "Arial"
        r.font.color.rgb = RGBColor(16, 44, 87)

        self.doc.add_paragraph()
        p = self.doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.3
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.add_run(text)

        p_kw = self.doc.add_paragraph()
        p_kw.paragraph_format.line_spacing = 1.3
        r_kw_lbl = p_kw.add_run("\nKeywords: ")
        r_kw_lbl.bold = True
        r_kw_lbl.font.color.rgb = RGBColor(16, 44, 87)
        p_kw.add_run(keywords)

        self.doc.add_page_break()

    def add_table_of_contents(self, items):
        h = self.doc.add_paragraph()
        h.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = h.add_run("TABLE OF CONTENTS")
        r.bold = True
        r.font.size = Pt(16)
        r.font.name = "Arial"
        r.font.color.rgb = RGBColor(16, 44, 87)

        self.doc.add_paragraph()
        table = self.doc.add_table(rows=1, cols=3)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False

        headers = ["Chapter / Section", "Title / Description", "Page"]
        widths = [Inches(1.8), Inches(4.2), Inches(0.8)]

        hdr_cells = table.rows[0].cells
        for i, text in enumerate(headers):
            hdr_cells[i].text = text
            hdr_cells[i].paragraphs[0].runs[0].bold = True
            hdr_cells[i].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
            hdr_cells[i].paragraphs[0].runs[0].font.size = Pt(10)
            set_cell_background(hdr_cells[i], "102C57")
            set_cell_margins(hdr_cells[i], 100, 100, 120, 120)
            hdr_cells[i].width = widths[i]

        for num_str, title, page_no in items:
            row_cells = table.add_row().cells
            row_cells[0].text = num_str
            row_cells[1].text = title
            row_cells[2].text = str(page_no)
            for j in range(3):
                row_cells[j].paragraphs[0].runs[0].font.size = Pt(9.5)
                row_cells[j].paragraphs[0].runs[0].font.name = "Arial"
                set_cell_margins(row_cells[j], 80, 80, 100, 100)
                row_cells[j].width = widths[j]
                if num_str.startswith("CHAPTER") or num_str in ["ABSTRACT", "REFERENCES"]:
                    row_cells[j].paragraphs[0].runs[0].bold = True
                    set_cell_background(row_cells[j], "F0F4F8")

        set_table_borders(table)
        self.doc.add_page_break()

    def add_chapter_heading(self, num, title):
        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(8)
        r_ch = p.add_run(f"CHAPTER {num}\n")
        r_ch.bold = True
        r_ch.font.size = Pt(14)
        r_ch.font.name = "Arial"
        r_ch.font.color.rgb = RGBColor(180, 50, 50)

        r_title = p.add_run(title.upper())
        r_title.bold = True
        r_title.font.size = Pt(16)
        r_title.font.name = "Arial"
        r_title.font.color.rgb = RGBColor(16, 44, 87)

    def add_section_heading(self, num_str, title):
        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run(f"{num_str}  {title}")
        r.bold = True
        r.font.size = Pt(12.5)
        r.font.name = "Arial"
        r.font.color.rgb = RGBColor(16, 44, 87)

    def add_subsection_heading(self, num_str, title):
        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(f"{num_str}  {title}")
        r.bold = True
        r.font.size = Pt(11)
        r.font.name = "Arial"
        r.font.color.rgb = RGBColor(60, 60, 60)

    def add_paragraph(self, text):
        p = self.doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.25
        p.paragraph_format.space_after = Pt(6)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r = p.add_run(text)
        r.font.size = Pt(10)
        r.font.name = "Calibri"
        return p

    def add_callout(self, title, text):
        table = self.doc.add_table(rows=1, cols=1)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = table.rows[0].cells[0]
        set_cell_background(cell, "F4F6F9")
        set_cell_margins(cell, 120, 120, 160, 160)
        
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(f'''
            <w:tcBorders {nsdecls("w")}>
                <w:left w:val="single" w:sz="24" w:space="0" w:color="102C57"/>
                <w:top w:val="none"/>
                <w:right w:val="none"/>
                <w:bottom w:val="none"/>
            </w:tcBorders>
        ''')
        tcPr.append(borders)

        p = cell.paragraphs[0]
        p.paragraph_format.line_spacing = 1.2
        r_t = p.add_run(f"■ {title}: ")
        r_t.bold = True
        r_t.font.size = Pt(10)
        r_t.font.name = "Arial"
        r_t.font.color.rgb = RGBColor(16, 44, 87)

        r_b = p.add_run(text)
        r_b.font.size = Pt(9.5)
        r_b.font.name = "Calibri"
        self.doc.add_paragraph().paragraph_format.space_after = Pt(4)

    def add_code_block(self, code_text):
        table = self.doc.add_table(rows=1, cols=1)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = table.rows[0].cells[0]
        set_cell_background(cell, "272822")
        set_cell_margins(cell, 100, 100, 140, 140)

        p = cell.paragraphs[0]
        p.paragraph_format.line_spacing = 1.05
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(code_text.strip())
        r.font.name = "Courier New"
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(248, 248, 242) # Monokai text
        self.doc.add_paragraph().paragraph_format.space_after = Pt(4)

    def add_table(self, headers, rows, col_widths=None):
        table = self.doc.add_table(rows=len(rows) + 1, cols=len(headers))
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False

        hdr_cells = table.rows[0].cells
        for i, h_text in enumerate(headers):
            hdr_cells[i].text = h_text
            p = hdr_cells[i].paragraphs[0]
            if len(p.runs) > 0:
                p.runs[0].bold = True
                p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
                p.runs[0].font.size = Pt(9.5)
                p.runs[0].font.name = "Arial"
            set_cell_background(hdr_cells[i], "102C57")
            set_cell_margins(hdr_cells[i], 100, 100, 120, 120)
            if col_widths and i < len(col_widths):
                hdr_cells[i].width = col_widths[i]

        for r_idx, row in enumerate(rows):
            row_cells = table.rows[r_idx + 1].cells
            bg = "F9FBFC" if r_idx % 2 == 1 else "FFFFFF"
            for c_idx, val in enumerate(row):
                row_cells[c_idx].text = str(val)
                p = row_cells[c_idx].paragraphs[0]
                if len(p.runs) > 0:
                    p.runs[0].font.size = Pt(9)
                    p.runs[0].font.name = "Calibri"
                set_cell_background(row_cells[c_idx], bg)
                set_cell_margins(row_cells[c_idx], 80, 80, 100, 100)
                if col_widths and c_idx < len(col_widths):
                    row_cells[c_idx].width = col_widths[c_idx]

        set_table_borders(table)
        self.doc.add_paragraph().paragraph_format.space_after = Pt(4)

    def add_image(self, img_path, caption, width_in_inches=5.5):
        if os.path.exists(img_path):
            p = self.doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(8)
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run()
            run.add_picture(img_path, width=Inches(width_in_inches))

            p_cap = self.doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_after = Pt(8)
            r_cap = p_cap.add_run(f"Figure: {caption}")
            r_cap.font.size = Pt(9)
            r_cap.font.italic = True
            r_cap.font.name = "Arial"
            r_cap.font.color.rgb = RGBColor(80, 80, 80)
        else:
            self.add_callout("Image Warning", f"Diagram file not found at path: {img_path}")

    def save(self, filepath):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        self.doc.save(filepath)
        print(f"[SUCCESS] Saved Word Document -> {filepath}")

