import streamlit as st
import pandas as pd
from services.notion import get_tasks

st.title("🚀 Task Harbor AI")

tasks = get_tasks()
df = pd.DataFrame(tasks)

question = st.text_input(
    "Ask Task Harbor AI",
    placeholder="What are my high priority tasks?"
)

if question:

    q = question.lower()

    if "high" in q:
        result = df[df["Priority"] == "High"]
        st.subheader("🔥 High Priority Tasks")
        st.dataframe(result)

    elif "todo" in q:
        result = df[df["Status"] == "Todo"]
        st.subheader("📋 Todo Tasks")
        st.dataframe(result)

    elif "dsa" in q:
        result = df[df["Category"] == "DSA"]
        st.subheader("🧠 DSA Tasks")
        st.dataframe(result)

    else:
        st.write("Sorry, I don't understand that yet.")

st.divider()

st.subheader("All Tasks")
st.dataframe(df)