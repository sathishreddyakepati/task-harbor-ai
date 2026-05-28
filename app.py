import streamlit as st
import pandas as pd

from services.notion import get_tasks
from services.google_calendar import get_upcoming_events, get_todays_events
from services.gmail import get_unread_emails

st.set_page_config(page_title="Task Harbor AI", page_icon="🚀", layout="wide")

st.title("🚀 Task Harbor AI")

# ---------------------
# Load Data
# ---------------------

tasks = get_tasks()
df = pd.DataFrame(tasks)

events = get_upcoming_events()
events_df = pd.DataFrame(events)

today_events = get_todays_events()
today_events_df = pd.DataFrame(today_events)

emails = get_unread_emails()
emails_df = pd.DataFrame(emails)

# ---------------------
# Metrics
# ---------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Tasks", len(df))

with col2:
    st.metric("Upcoming Events", len(events_df))

with col3:
    st.metric("Unread Emails", len(emails_df))

# ---------------------
# AI Query Box
# ---------------------

question = st.text_input(
    "Ask Task Harbor AI", placeholder="What should I work on today?"
)

if question:

    q = question.lower()

    # High Priority Tasks
    if "high" in q:

        result = df[df["Priority"] == "High"]

        st.subheader("🔥 High Priority Tasks")
        st.dataframe(result, use_container_width=True)

    # Todo Tasks
    elif "todo" in q:

        result = df[df["Status"] == "Todo"]

        st.subheader("📋 Todo Tasks")
        st.dataframe(result, use_container_width=True)

    # DSA Tasks
    elif "dsa" in q:

        result = df[df["Category"] == "DSA"]

        st.subheader("🧠 DSA Tasks")
        st.dataframe(result, use_container_width=True)

    # Next Event
    elif "next event" in q:

        st.subheader("📅 Next Event")

        if len(events) > 0:

            st.success(events[0]["Event"])

            st.write("Start:", events[0]["Start"])

        else:

            st.info("No upcoming events found.")

    # Today's Events
    elif "today" in q and ("meeting" in q or "event" in q):

        st.subheader("📅 Today's Schedule")

        if len(today_events_df) > 0:

            st.dataframe(today_events_df, use_container_width=True)

        else:

            st.info("No meetings scheduled for today.")

    # Calendar Events
    elif "calendar" in q or "events" in q:

        st.subheader("📅 Upcoming Events")

        st.dataframe(events_df, use_container_width=True)

    # GitHub Emails
    elif "github" in q:

        github_emails = emails_df[
            emails_df["From"].str.contains("github", case=False, na=False)
        ]

        st.subheader("🐙 GitHub Notifications")

        if len(github_emails) > 0:

            st.dataframe(github_emails, use_container_width=True)

        else:

            st.info("No GitHub emails found.")
      # Emails
    elif "email" in q:

        st.subheader("📧 Unread Emails")

        if len(emails_df) > 0:
            st.dataframe(emails_df, use_container_width=True)

        else:
            st.info("No unread emails found.")

    # AI Recommendation
    elif (
        "work on today" in q or
        "focus today" in q or
        "what should i focus on today" in q
    ):

        high_priority = df[
            (df["Priority"] == "High") &
            (df["Status"] == "Todo")
        ]

        st.subheader("🎯 AI Recommendation")

        st.markdown(f"""
### Today's Productivity Summary

📋 High Priority Tasks: {len(high_priority)}

📅 Events Today: {len(today_events_df)}

📧 Unread Emails: {len(emails_df)}
""")

        if len(high_priority) > 0:

            st.markdown("""
### Recommended Action Plan

1️⃣ Complete high-priority pending tasks

2️⃣ Prepare for today's calendar events

3️⃣ Review important unread emails

4️⃣ Check GitHub notifications and PR updates
""")

            st.dataframe(
                high_priority,
                use_container_width=True
            )

        else:

            st.info(
                "No high-priority tasks found today."
            )

    else:

        st.warning(
            "Sorry, I don't understand that yet."
        )

# ---------------------
# Dashboard
# ---------------------

st.divider()

col1, col2, col3 = st.columns(3)

with col1:

    st.subheader("📋 Tasks")

    st.dataframe(df, use_container_width=True)

with col2:

    st.subheader("📅 Events")

    st.dataframe(events_df, use_container_width=True)

with col3:

    st.subheader("📧 Emails")

    st.dataframe(emails_df.head(5), use_container_width=True)
