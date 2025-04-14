import streamlit as st
import psycopg2
import smtplib
from email.message import EmailMessage
import os

st.title("📝 AEM Vendor Submission Form")

name = st.text_input("Vendor Name")
email = st.text_input("Email")
service = st.text_area("Services Provided")
submit = st.button("Submit")

if submit:
    if not name or not email or not service:
        st.warning("Please fill all fields.")
    else:
        try:
            conn = psycopg2.connect(
                host=os.getenv("DB_HOST"),
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASS"),
                port=5432
            )
            cur = conn.cursor()
            cur.execute("INSERT INTO pending_vendors (name, email, service) VALUES (%s, %s, %s)", (name, email, service))
            conn.commit()
            cur.close()
            conn.close()
            st.success("Form submitted for approval!")

            msg = EmailMessage()
            msg["Subject"] = "New Vendor Submission"
            msg["From"] = os.getenv("EMAIL_HOST_USER")
            msg["To"] = os.getenv("ADMIN_EMAIL")
            msg.set_content(f"New vendor submitted:\n\nName: {name}\nEmail: {email}\nService: {service}")

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(os.getenv("EMAIL_HOST_USER"), os.getenv("EMAIL_HOST_PASS"))
                smtp.send_message(msg)

        except Exception as e:
            st.error(f"Error: {e}")
