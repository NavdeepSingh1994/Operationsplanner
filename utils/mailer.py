import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import streamlit as st

# clemens.geistler@nolock.at
def send_email_with_pdf(pdf_path):
    sender_email = "singh.navdeep.htl.donaustadt@gmail.com"
    password = st.secrets["email_password"]

    # Für das Gespräch bitte NICHT aktiv setzen:
    recipient_email = "# navdeepsingh@live.at"

    # >>> Aktiv setzen nur zum echten Testen <<<
    recipient_email = "navdeepsingh@live.at"

    subject = "📄 Neuer Incident-Bericht"
    body = "Anbei findest du den automatisch erstellten Incident-Bericht als PDF."

    send_pdf_report(pdf_path, subject, body)


def send_pdf_report(pdf_path, subject="📄 Report", body="Bitte finden Sie den angehängten Bericht."):
    sender_email = "singh.navdeep.htl.donaustadt@gmail.com"
    password = st.secrets["email_password"]

    # Empfänger – aktuell du selbst (zum Test)
    recipient_email = "navdeepsingh@live.at"

    # E-Mail erstellen
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    # PDF anhängen
    with open(pdf_path, "rb") as f:
        part = MIMEApplication(f.read(), Name=os.path.basename(pdf_path))
        part["Content-Disposition"] = f'attachment; filename="{os.path.basename(pdf_path)}"'
        msg.attach(part)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)
        server.send_message(msg)
        server.quit()
        st.success("E-Mail erfolgreich versendet.")
    except Exception as e:
        st.error(f"E-Mail-Versand fehlgeschlagen: {e}")
