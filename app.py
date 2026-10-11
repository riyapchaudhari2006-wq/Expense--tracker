import streamlit as st
import pandas as pd
import plotly.express as px
from database import create_table, add_expense, get_expenses, delete_expense

create_table()

st.title("💰 Personal Expenses Tracker")

CATEGORIES = ["Food", "Travel", "Education", "Shopping", "Bills", "Entertainment", "Other"]
MODES = ["UPI", "Cash", "Card"]

# ---- खर्च टाकण्याचा फॉर्म ----
st.subheader("नवीन खर्च जोडा")
with st.form("expense_form", clear_on_submit=True):
    date = st.date_input("तारीख")
    category = st.selectbox("कॅटेगरी", CATEGORIES)
    amount = st.number_input("रक्कम (₹)", min_value=0.0, step=10.0)
    mode = st.selectbox("पेमेंट मोड", MODES)
    note = st.text_input("नोट (ऐच्छिक)")
    submitted = st.form_submit_button("Save")

if submitted:
    if amount > 0:
        add_expense(str(date), category, amount, mode, note)
        st.success("खर्च सेव्ह झाला!")
    else:
        st.warning("रक्कम 0 पेक्षा जास्त टाका.")

# ---- सगळे खर्च ----
rows = get_expenses()
df = pd.DataFrame(rows, columns=["ID", "Date", "Category", "Amount", "Mode", "Note"])

if df.empty:
    st.info("अजून कोणताही खर्च नाही. वर फॉर्म भरून सुरुवात करा.")
else:
    st.subheader("सारांश")
    st.metric("एकूण खर्च", "₹ {:.2f}".format(df["Amount"].sum()))

    col1, col2 = st.columns(2)
    with col1:
        fig1 = px.pie(df, names="Category", values="Amount", title="कॅटेगरीनुसार खर्च")
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        df["Month"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m")
        monthly = df.groupby("Month")["Amount"].sum().reset_index()
        fig2 = px.bar(monthly, x="Month", y="Amount", title="महिन्यानुसार खर्च")
        fig2.update_xaxes(type="category")
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("सगळे खर्च")
    st.dataframe(df[["ID", "Date", "Category", "Amount", "Mode", "Note"]])

    st.subheader("खर्च डिलीट करा")
    del_id = st.selectbox("ID निवडा", df["ID"].tolist())
    if st.button("Delete"):
        delete_expense(int(del_id))
        st.experimental_rerun()