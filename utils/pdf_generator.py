from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
import os

def generate_pdf(incident_id, title, description, category, priority, sla, teams, created_at):
    filename = f"incident_{incident_id}.pdf"
    filepath = os.path.join("db", filename)

    doc = SimpleDocTemplate(filepath, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph(f"<b>Incident Report – ID {incident_id}</b>", styles["Title"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"<b>Titel:</b> {title}", styles["Normal"]))
    story.append(Paragraph(f"<b>Beschreibung:</b> {description}", styles["Normal"]))
    story.append(Paragraph(f"<b>Kategorie:</b> {category}", styles["Normal"]))
    story.append(Paragraph(f"<b>Priorität:</b> {priority}", styles["Normal"]))
    story.append(Paragraph(f"<b>SLA:</b> {sla}", styles["Normal"]))
    story.append(Paragraph(f"<b>Beteiligte Teams:</b> {teams}", styles["Normal"]))
    story.append(Paragraph(f"<b>Erstellt am:</b> {created_at}", styles["Normal"]))
    story.append(Spacer(1, 24))
    story.append(Paragraph("Automatisch generierter Bericht aus dem Incident Assistant.", styles["Italic"]))

    doc.build(story)
    return filepath
