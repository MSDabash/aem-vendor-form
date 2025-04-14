import streamlit as st
import psycopg2
import os

st.set_page_config(page_title="Vendor Approval Panel", page_icon="✅")

st.title("🔒 Vendor Approval Dashboard")

password = st.text_input("Enter Admin Password", type="password")
if password != os.getenv("ADMIN_PASSWORD"):
    st.stop()

try:
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        port=5432
    )
    cur = conn.cursor()
    cur.execute("SELECT id, name, email, service FROM pending_vendors")
    rows = cur.fetchall()

    for row in rows:
        st.markdown("---")
        st.write(f"**Name:** {row[1]}")
        st.write(f"**Email:** {row[2]}")
        st.write(f"**Service:** {row[3]}")

        col1, col2 = st.columns(2)
        if col1.button(f"✅ Approve {row[1]}", key=f"approve_{row[0]}"):
            cur.execute("INSERT INTO vendors (name, email, service) VALUES (%s, %s, %s)", (row[1], row[2], row[3]))
            cur.execute("DELETE FROM pending_vendors WHERE id = %s", (row[0],))
            conn.commit()
            st.success(f"{row[1]} approved and moved to main vendor list.")

        if col2.button(f"❌ Reject {row[1]}", key=f"reject_{row[0]}"):
            cur.execute("DELETE FROM pending_vendors WHERE id = %s", (row[0],))
            conn.commit()
            st.error(f"{row[1]} has been rejected.")

    cur.close()
    conn.close()
except Exception as e:
    st.error(f"Database error: {e}")
