# generate_pdf.py - Pure Python standard PDF generator (Zero dependencies)
import os

def create_resume_pdf(filename):
    # Standard PDF 1.4 canvas implementation
    objects = []
    
    def add_object(content):
        objects.append(content)
        return len(objects)

    # We will build page stream
    # Page size: A4 (595.28 x 841.89 points)
    width = 595.28
    height = 841.89
    
    stream_lines = []
    
    # Helper commands
    # Colors (RGB 0.0 to 1.0)
    # Navy: 0.12, 0.23, 0.54 (#1e3a8a)
    # Dark Slate: 0.1, 0.15, 0.25
    # Gray: 0.35, 0.4, 0.5
    # Light Border: 0.8, 0.84, 0.9
    
    def set_fill(r, g, b):
        stream_lines.append(f"{r:.3f} {g:.3f} {b:.3f} rg")
        
    def set_stroke(r, g, b):
        stream_lines.append(f"{r:.3f} {g:.3f} {b:.3f} RG")
        
    def draw_line(x1, y1, x2, y2, lw=1.0):
        stream_lines.append(f"{lw:.2f} w")
        stream_lines.append(f"{x1:.2f} {y1:.2f} m {x2:.2f} {y2:.2f} l S")
        
    def draw_rect(x, y, w, h, fill=False, stroke=True, lw=1.0):
        stream_lines.append(f"{lw:.2f} w")
        op = "B" if (fill and stroke) else ("f" if fill else "S")
        stream_lines.append(f"{x:.2f} {y:.2f} {w:.2f} {h:.2f} re {op}")

    def draw_text(x, y, text, font="F1", size=10, r=0.1, g=0.15, b=0.25):
        clean_text = text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
        stream_lines.append("BT")
        stream_lines.append(f"/{font} {size:.1f} Tf")
        stream_lines.append(f"{r:.3f} {g:.3f} {b:.3f} rg")
        stream_lines.append(f"{x:.2f} {y:.2f} Td")
        stream_lines.append(f"({clean_text}) Tj")
        stream_lines.append("ET")

    margin_left = 42.0
    content_width = width - (margin_left * 2) # ~511 pt
    
    cur_y = height - 48.0
    
    # 1. Header
    draw_text(margin_left, cur_y, "KOMAL RATHOR", font="F2", size=22, r=0.12, g=0.23, b=0.54)
    cur_y -= 16
    draw_text(margin_left, cur_y, "Aspiring Web Developer | B.Tech CSE Scholar", font="F1", size=11, r=0.3, g=0.35, b=0.45)
    cur_y -= 14
    
    # Contact Row (NO PHONE NUMBER!)
    contact_str = "Email: komalrathorebgs@gmail.com  |  Location: Jaipur, Rajasthan (Joyti Vidya Peeth University)"
    draw_text(margin_left, cur_y, contact_str, font="F1", size=9, r=0.2, g=0.25, b=0.35)
    cur_y -= 12
    social_str = "LinkedIn: linkedin.com/in/komal-rathor-0609262a4  |  Instagram: @komal__5916"
    draw_text(margin_left, cur_y, social_str, font="F1", size=9, r=0.12, g=0.23, b=0.54)
    cur_y -= 12
    
    # Top Divider
    set_stroke(0.12, 0.23, 0.54)
    draw_line(margin_left, cur_y, margin_left + content_width, cur_y, lw=2.0)
    cur_y -= 18

    # Section Helper
    def render_section_heading(title, y):
        draw_text(margin_left, y, title, font="F2", size=11, r=0.12, g=0.23, b=0.54)
        set_stroke(0.75, 0.8, 0.88)
        draw_line(margin_left, y - 4, margin_left + content_width, y - 4, lw=1.0)
        return y - 16

    # 2. Career Objective
    cur_y = render_section_heading("CAREER OBJECTIVE", cur_y)
    obj_l1 = "Motivated B.Tech student with a Diploma background and hands-on experience building modern, responsive"
    obj_l2 = "web applications using HTML, CSS, JavaScript, React, Next.js, and Python. Seeking an entry-level web developer role"
    obj_l3 = "to contribute to real-world projects, build scalable digital solutions, and continuously grow into a proficient developer."
    draw_text(margin_left, cur_y, obj_l1, font="F1", size=9.5, r=0.15, g=0.2, b=0.3)
    cur_y -= 13
    draw_text(margin_left, cur_y, obj_l2, font="F1", size=9.5, r=0.15, g=0.2, b=0.3)
    cur_y -= 13
    draw_text(margin_left, cur_y, obj_l3, font="F1", size=9.5, r=0.15, g=0.2, b=0.3)
    cur_y -= 18

    # 3. Education
    cur_y = render_section_heading("EDUCATION", cur_y)
    
    # Table Header Box
    th_y = cur_y - 14
    set_fill(0.95, 0.96, 0.98)
    set_stroke(0.8, 0.84, 0.9)
    draw_rect(margin_left, th_y, content_width, 18, fill=True, stroke=True, lw=0.8)
    
    # Header Columns
    draw_text(margin_left + 6, th_y + 5, "Qualification", font="F2", size=9, r=0.12, g=0.23, b=0.54)
    draw_text(margin_left + 155, th_y + 5, "Institution", font="F2", size=9, r=0.12, g=0.23, b=0.54)
    draw_text(margin_left + 380, th_y + 5, "Session", font="F2", size=9, r=0.12, g=0.23, b=0.54)
    draw_text(margin_left + 450, th_y + 5, "Result", font="F2", size=9, r=0.12, g=0.23, b=0.54)
    
    cur_y = th_y
    
    edu_rows = [
        ("B.Tech (Computer Science & Engg.)", "Jyoti Vidyapeeth Women's Univ., Jaipur", "2024 - 2027", "Pursuing"),
        ("Diploma in Engineering (CSE)", "Jyoti Vidyapeeth Women's Univ., Jaipur", "2021 - 2024", "7.7 CGPA"),
        ("Class X (Matriculation)", "Bihar School Examination Board (BSEB)", "2021", "63%")
    ]
    
    for qual, inst, sess, res in edu_rows:
        row_y = cur_y - 18
        set_fill(1.0, 1.0, 1.0)
        set_stroke(0.85, 0.88, 0.92)
        draw_rect(margin_left, row_y, content_width, 18, fill=True, stroke=True, lw=0.6)
        draw_text(margin_left + 6, row_y + 5, qual, font="F2", size=8.5, r=0.1, g=0.15, b=0.25)
        draw_text(margin_left + 155, row_y + 5, inst, font="F1", size=8.5, r=0.2, g=0.25, b=0.35)
        draw_text(margin_left + 380, row_y + 5, sess, font="F1", size=8.5, r=0.2, g=0.25, b=0.35)
        draw_text(margin_left + 450, row_y + 5, res, font="F2", size=8.5, r=0.12, g=0.23, b=0.54)
        cur_y = row_y
        
    cur_y -= 18

    # 4. Technical Skills
    cur_y = render_section_heading("TECHNICAL SKILLS", cur_y)
    skills = [
        ("Frontend & Web:", "HTML5, CSS3, JavaScript (ES6+), React.js, Next.js, Tailwind CSS, TypeScript, Responsive Web Design"),
        ("Programming:", "Python Language, C Programming, C++, Core Java (OOPs, Collections), SQL & Relational Databases"),
        ("Productivity & Tools:", "Git, GitHub, Vercel Deployment, VS Code, MS Word, MS Excel, MS PowerPoint")
    ]
    for cat, items in skills:
        draw_text(margin_left + 4, cur_y, "- " + cat, font="F2", size=9, r=0.1, g=0.15, b=0.25)
        draw_text(margin_left + 115, cur_y, items, font="F1", size=9, r=0.2, g=0.25, b=0.35)
        cur_y -= 14
        
    cur_y -= 4

    # 5. Projects
    cur_y = render_section_heading("FEATURED PROJECTS", cur_y)
    
    # Project 1: OSCA India
    draw_text(margin_left + 4, cur_y, "OSCA India - Digital Marketing Agency Website", font="F2", size=9.5, r=0.1, g=0.15, b=0.25)
    draw_text(margin_left + 280, cur_y, "| React, Next.js, Tailwind, Vercel (oscaindia.vercel.app)", font="F1", size=8.5, r=0.12, g=0.23, b=0.54)
    cur_y -= 12
    draw_text(margin_left + 12, cur_y, "* Designed and developed a high-performance business website for a digital marketing agency using Next.js.", font="F1", size=8.5, r=0.25, g=0.3, b=0.4)
    cur_y -= 11
    draw_text(margin_left + 12, cur_y, "* Implemented responsive layouts, service showcases, growth dashboard metrics, and interactive contact actions.", font="F1", size=8.5, r=0.25, g=0.3, b=0.4)
    cur_y -= 15

    # Project 2: Weather Dashboard
    draw_text(margin_left + 4, cur_y, "Live Weather Forecast & Climate Dashboard", font="F2", size=9.5, r=0.1, g=0.15, b=0.25)
    draw_text(margin_left + 265, cur_y, "| JavaScript (Fetch API), REST API, CSS3 Flexbox/Grid", font="F1", size=8.5, r=0.12, g=0.23, b=0.54)
    cur_y -= 12
    draw_text(margin_left + 12, cur_y, "* Integrated OpenWeather REST API to fetch real-time global weather conditions, humidity, and 5-day forecasts.", font="F1", size=8.5, r=0.25, g=0.3, b=0.4)
    cur_y -= 15

    # Project 3: TaskFlow
    draw_text(margin_left + 4, cur_y, "TaskFlow - Daily To-Do & Task Manager", font="F2", size=9.5, r=0.1, g=0.15, b=0.25)
    draw_text(margin_left + 250, cur_y, "| JavaScript, LocalStorage API, DOM Manipulation", font="F1", size=8.5, r=0.12, g=0.23, b=0.54)
    cur_y -= 12
    draw_text(margin_left + 12, cur_y, "* Built a productivity task manager featuring CRUD operations, category priority tagging, and persistent local storage.", font="F1", size=8.5, r=0.25, g=0.3, b=0.4)
    cur_y -= 15

    # Project 4: Python Records
    draw_text(margin_left + 4, cur_y, "Student & Records Management System", font="F2", size=9.5, r=0.1, g=0.15, b=0.25)
    draw_text(margin_left + 245, cur_y, "| Python 3, Object-Oriented Programming, File Handling", font="F1", size=8.5, r=0.12, g=0.23, b=0.54)
    cur_y -= 12
    draw_text(margin_left + 12, cur_y, "* Developed an end-to-end Python software implementing OOP architectures, automated GPA calculation, and data storage.", font="F1", size=8.5, r=0.25, g=0.3, b=0.4)
    cur_y -= 18

    # 6. Strengths
    cur_y = render_section_heading("STRENGTHS & ATTRIBUTES", cur_y)
    str_l1 = "* Positive Attitude & Adaptability   * Time Management & Self-Learning   * Responsible & Dedicated Work Ethic"
    str_l2 = "* Teamwork & Cross-functional Communication   * Problem Solving & Analytical Thinking   * Attention to Detail & UI Precision"
    draw_text(margin_left + 4, cur_y, str_l1, font="F1", size=9, r=0.15, g=0.2, b=0.3)
    cur_y -= 13
    draw_text(margin_left + 4, cur_y, str_l2, font="F1", size=9, r=0.15, g=0.2, b=0.3)
    cur_y -= 18

    # 7. Languages
    cur_y = render_section_heading("LANGUAGES", cur_y)
    draw_text(margin_left + 4, cur_y, "English (Professional Working Proficiency)  |  Hindi (Native / Fluent)  |  Technical Documentation", font="F1", size=9, r=0.15, g=0.2, b=0.3)
    cur_y -= 18

    # 8. Declaration
    cur_y = render_section_heading("DECLARATION", cur_y)
    draw_text(margin_left + 4, cur_y, "I hereby declare that the information provided above is true and correct to the best of my knowledge.", font="F1", size=8.5, r=0.35, g=0.4, b=0.45)
    cur_y -= 14
    draw_text(margin_left + content_width - 80, cur_y, "Komal Rathor", font="F2", size=10, r=0.12, g=0.23, b=0.54)

    # Content Stream Object
    stream_data = "\n".join(stream_lines).encode("utf-8")
    stream_len = len(stream_data)

    # Assembly PDF structures
    # Obj 1: Catalog
    # Obj 2: Outlines
    # Obj 3: Pages
    # Obj 4: Page
    # Obj 5: Font F1 (Helvetica)
    # Obj 6: Font F2 (Helvetica-Bold)
    # Obj 7: Content stream
    
    pdf_parts = []
    offsets = []
    
    def append_obj(obj_str):
        offsets.append(sum(len(p) for p in pdf_parts))
        pdf_parts.append(obj_str.encode("latin1"))

    # Header
    pdf_parts.append(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    
    # 1: Catalog
    append_obj("1 0 obj\n<< /Type /Catalog /Pages 3 0 R >>\nendobj\n")
    
    # 2: Outlines
    append_obj("2 0 obj\n<< /Type /Outlines /Count 0 >>\nendobj\n")
    
    # 3: Pages
    append_obj("3 0 obj\n<< /Type /Pages /Kids [4 0 R] /Count 1 >>\nendobj\n")
    
    # 4: Page
    append_obj(f"4 0 obj\n<< /Type /Page /Parent 3 0 R /MediaBox [0 0 {width:.2f} {height:.2f}] /Contents 7 0 R /Resources << /Font << /F1 5 0 R /F2 6 0 R >> >> >>\nendobj\n")
    
    # 5: Font F1
    append_obj("5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>\nendobj\n")
    
    # 6: Font F2
    append_obj("6 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>\nendobj\n")
    
    # 7: Contents
    append_obj(f"7 0 obj\n<< /Length {stream_len} >>\nstream\n{stream_data.decode('latin1')}\nendstream\nendobj\n")
    
    # Xref
    xref_offset = sum(len(p) for p in pdf_parts)
    xref_str = f"xref\n0 {len(offsets) + 1}\n0000000000 65535 f \n"
    for o in offsets:
        xref_str += f"{o:010d} 00000 n \n"
        
    trailer_str = f"trailer\n<< /Size {len(offsets) + 1} /Root 1 0 R >>\nstartxref\n{xref_offset}\n%%EOF\n"
    
    pdf_parts.append(xref_str.encode("latin1"))
    pdf_parts.append(trailer_str.encode("latin1"))
    
    with open(filename, "wb") as f:
        f.write(b"".join(pdf_parts))
    print(f"Generated clean PDF successfully: {filename} ({os.path.getsize(filename)} bytes)")

if __name__ == "__main__":
    out1 = r"c:\komal rathore\Komal_Rathor_Resume.pdf"
    out2 = r"c:\komal rathore\Komal_Rathore_Resume.pdf"
    create_resume_pdf(out1)
    create_resume_pdf(out2)
