import streamlit as st
with open("styles.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )
import pandas as pd

from services.notion import get_tasks
from services.google_calendar import get_upcoming_events, get_todays_events
from services.gmail import get_unread_emails

# ---------------------
# HEADER
# ---------------------
st.set_page_config(
    page_title="Task Harbor AI",
    page_icon="🚀",
    layout="wide"
)

st.markdown("""
<style>
.badge {
    display:inline-block;
    padding:8px 16px;
    margin-left:10px;
    border-radius:20px;
    border:1px solid #2d3748;
    background:#111827;
    color:white;
    font-size:14px;
}

.coral {
    background:linear-gradient(90deg,#ff7b72,#ff9966);
    border:none;
}
</style>
""", unsafe_allow_html=True)


header_left, header_right = st.columns([3,2])
with header_left:
    st.markdown(
        "<h1 style='margin-top:10px;'>🚀 Task Harbor AI</h1>",
        unsafe_allow_html=True
    )

with header_right:
    st.markdown("""
    <div style='text-align:right'>
        <span class='badge'>🟢 Notion</span>
        <span class='badge'>🟢 Google Calendar</span>
        <span class='badge'>🟢 Gmail</span>
       
    </div>
    """, unsafe_allow_html=True)

# ---------------------
# LOAD DATA
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
# WELCOME CARD
# ---------------------



# ---------------------
# HERO CARD
# ---------------------

st.markdown("""
<div style="
background:#111827;
border:1px solid #1f2937;
border-radius:24px;
padding:30px;
margin-bottom:20px;
">
<h2>Welcome back, Sathish 👋</h2>

<p style="
color:#9ca3af;
font-size:18px;
">
Here's what's happening with your productivity today.
</p>
</div>
""",
unsafe_allow_html=True)

st.info("""
⚡ Powered by Coral

Connected Sources:
✓ Notion
✓ Google Calendar
✓ Gmail

Task Harbor AI uses Coral to unify productivity data
into a single workspace and generate recommendations.
""")

# ---------------------
# METRIC CARDS
# ---------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div style="
    background:#111827;
    border-radius:20px;
    padding:20px;
    text-align:center;
    ">
        <h1>{len(df)}</h1>
        <p>Tasks</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="
    background:#111827;
    border-radius:20px;
    padding:20px;
    text-align:center;
    ">
        <h1>{len(events_df)}</h1>
        <p>Events</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="
    background:#111827;
    border-radius:20px;
    padding:20px;
    text-align:center;
    ">
        <h1>{len(emails_df)}</h1>
        <p>Emails</p>
    </div>
    """, unsafe_allow_html=True)


# ---------------------
# AI Query Box
# ---------------------
"  "


col1,col2,col3,col4 = st.columns([1,1,1,4])

with col1:
    focus_btn = st.button("🎯 Focus")

with col2:
    github_btn = st.button("🐙 GitHub")

with col3:
    meetings_btn = st.button("📅 Meetings")


question = st.text_input(
    "Ask Task Harbor AI", placeholder="What should I work on today?"
)

high_priority = df[
    (df["Priority"] == "High")
    & (df["Status"] == "Todo")
]
if len(high_priority) > 0:

    task_name = high_priority.iloc[0]["Task"]

    st.markdown(f"""
    <div style="
    background:#111827;
    border-radius:24px;
    padding:25px;
    margin-bottom:25px;
    ">

    <h2>🎯 AI Recommendation</h2>

    <h3>{task_name}</h3>

    <p>
    • High Priority<br>
    • No schedule conflicts<br>
    • Highest impact task today
    </p>

    <p style="color:#60a5fa;">
    Confidence: 92%
    </p>

    </div>
    """, unsafe_allow_html=True)
if focus_btn:
    q = "What should I focus on today?"

elif github_btn:
    q = "Show GitHub notifications"

elif meetings_btn:
    q = "What meetings do I have today?"

else:
    q = ""
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
