import streamlit as st
import pandas as pd
from services.notion import get_tasks

st.title("🚀 Task Harbor AI")

if st.button("Load Tasks"):
    tasks = get_tasks()

    st.dataframe(pd.DataFrame(tasks))