from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
import os
from utils.oncall_db import get_all_oncalls

def generate_oncall_pdf():
    filename = "bereitschaftsplan.pdf"
    filepath = os.path.join("db", filename)

    doc = SimpleDocTemplate(filepath, pagesize=A4)
    styles = getSampleStyleSheet()
    story = [Paragraph("Bereitschaftsdienst – Übersicht", styles["Title"]), Spacer(1, 12)]

    data = [["ID", "Kalenderwoche", "Name", "Rolle", "E-Mail"]]
    for row in get_all_oncalls():
        data.append(row)

    table = Table(data, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("ALIGN", (0, 0), (-1, -1), "LEFT")
    ]))

    story.append(table)
    doc.build(story)
    return filepath
