import streamlit as st
import datetime
import pandas as pd
from utils.db_handler import create_incident, init_db
from utils.mailer import send_email_with_pdf, send_pdf_report
from utils.pdf_generator import generate_pdf
from utils.task_db import init_task_table, add_task, get_all_tasks
from utils.oncall_db import init_oncall_table, add_oncall, get_all_oncalls
from utils.task_report import generate_task_pdf
from utils.oncall_report import generate_oncall_pdf

# ---------- INIT ----------
st.set_page_config(page_title="OpsBoard – Operationsplaner", layout="wide")
init_db()
init_task_table()
init_oncall_table()

# ---------- HEADER ----------
st.title("🛠️ OpsBoard – Operationsplaner für IT")
st.markdown("Ein zentrales Tool zur Erfassung von Incidents, Arbeitspaketen und Bereitschaftsdiensten.")

# ---------- TABS ----------
tab1, tab2, tab3 = st.tabs(["📄 Incident-Reporting", "📋 Arbeitspakete (SOLL/IST)", "📆 Bereitschaftsdienst"])

# ============================
# TAB 1 – INCIDENTS
# ============================
with tab1:
    st.subheader("📄 Incident-Daten eingeben")

    with st.form("incident_form"):
        title = st.text_input("Titel des Incidents")
        description = st.text_area("Beschreibung")
        category = st.selectbox("Kategorie", ["Systemfehler", "Datenproblem", "Performance", "Security", "Sonstiges"])
        priority = st.radio("Priorität", ["P1", "P2", "P3", "P4"], horizontal=True)
        sla = st.text_input("SLA (z. B. 4h, 1d)")
        teams = st.text_input("Beteiligte Teams (z. B. ABS, SNOW, DevOps)")

        generate_pdf_flag = st.checkbox("PDF-Bericht erzeugen")
        send_email_flag = st.checkbox("E-Mail an Verantwortlichen senden")

        submitted = st.form_submit_button("✅ Incident speichern")

    if submitted:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        incident_id = create_incident(title, description, category, priority, sla, teams, timestamp)

        st.success(f"Incident ID {incident_id} wurde gespeichert.")

        if generate_pdf_flag:
            pdf_path = generate_pdf(incident_id, title, description, category, priority, sla, teams, timestamp)
            st.info(f"PDF-Bericht gespeichert unter: `{pdf_path}`")

            if send_email_flag:
                send_email_with_pdf(pdf_path)
                st.success("E-Mail wurde versendet.")

# ============================
# TAB 2 – TASKS
# ============================
with tab2:
    st.subheader("📋 Arbeitspakete (SOLL-/IST-Vergleich)")

    with st.form("task_form"):
        t_title = st.text_input("Titel des Arbeitspakets")
        t_responsible = st.text_input("Verantwortlich")
        t_soll = st.date_input("SOLL-Fertigstellung")
        t_ist = st.date_input("IST-Fertigstellung (optional)", value=None)
        t_status = st.selectbox("Status", ["Offen", "In Arbeit", "Fertig", "Verschoben"])
        t_notes = st.text_area("Notizen")

        t_submit = st.form_submit_button("💾 Arbeitspaket speichern")

    if t_submit:
        add_task(t_title, t_responsible, str(t_soll), str(t_ist), t_status, t_notes)
        st.success("Arbeitspaket gespeichert.")

    if st.checkbox("📄 Zeige alle Arbeitspakete"):
        tasks = get_all_tasks()
        if tasks:
            df = pd.DataFrame(tasks, columns=["ID", "Titel", "Verantwortlich", "SOLL", "IST", "Status", "Notizen"])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Noch keine Aufgaben eingetragen.")

    if st.button("📤 Arbeitspaket-Übersicht als PDF senden"):
        pdf_path = generate_task_pdf()
        send_pdf_report(pdf_path, subject="📋 Arbeitspakete – Übersicht", body="Anbei die Übersicht aller Arbeitspakete.")

# ============================
# TAB 3 – ONCALL
# ============================
with tab3:
    st.subheader("📆 Bereitschaftsdienst planen")

    with st.form("oncall_form"):
        kw = st.text_input("Kalenderwoche (z. B. KW33/2025)")
        name = st.text_input("Name der verantwortlichen Person")
        role = st.selectbox("Rolle", ["Primary", "Backup", "Bereitschaft"])
        email = st.text_input("E-Mail (optional)")
        o_submit = st.form_submit_button("💾 Dienst eintragen")

    if o_submit:
        add_oncall(kw, name, role, email)
        st.success(f"Bereitschaftsdienst für {name} in {kw} gespeichert.")

    if st.checkbox("📄 Zeige alle geplanten Dienste"):
        oncalls = get_all_oncalls()
        if oncalls:
            df = pd.DataFrame(oncalls, columns=["ID", "KW", "Name", "Rolle", "E-Mail"])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Noch keine Dienste eingetragen.")

    if st.button("📤 Bereitschaftsplan als PDF senden"):
        pdf_path = generate_oncall_pdf()
        send_pdf_report(pdf_path, subject="📆 Bereitschaftsdienst – Übersicht", body="Anbei der aktuelle Bereitschaftsplan.")
