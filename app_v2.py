import streamlit as st
import pandas as pd
import html as _html
from datetime import datetime

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Task Harbor AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── GLOBAL CSS ─────────────────────────────────────────────────────────────
# FIX 1: Added unsafe_allow_html=True (was missing — caused all HTML to render as raw text)
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
    --bg-base:       #07090f;
    --bg-surface:    #0d1117;
    --bg-elevated:   #111827;
    --bg-card:       #131c2e;
    --border:        #1e2d45;
    --border-bright: #2a3f5f;
    --coral:         #ff6b47;
    --coral-dim:     #cc4a2a;
    --coral-glow:    rgba(255, 107, 71, 0.18);
    --coral-subtle:  rgba(255, 107, 71, 0.08);
    --teal:          #00d4aa;
    --teal-subtle:   rgba(0, 212, 170, 0.10);
    --blue:          #4f8ef7;
    --blue-subtle:   rgba(79, 142, 247, 0.10);
    --yellow:        #f5c842;
    --yellow-subtle: rgba(245, 200, 66, 0.10);
    --text-primary:  #e8edf5;
    --text-secondary:#8b9ab5;
    --text-muted:    #4a5870;
    --font:          'Sora', sans-serif;
    --mono:          'DM Mono', monospace;
}

.stApp {
    background: var(--bg-base) !important;
    font-family: var(--font) !important;
    color: var(--text-primary) !important;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }
[data-testid="stToolbar"] { display: none; }
section[data-testid="stSidebar"] { display: none; }

::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: var(--bg-base); }
::-webkit-scrollbar-thumb { background: var(--border-bright); border-radius: 2px; }

.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.03'/%3E%3C/svg%3E");
    pointer-events: none;
    z-index: 0;
    opacity: 0.4;
}

.th-topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 14px 32px;
    background: rgba(13, 17, 23, 0.92);
    border-bottom: 1px solid var(--border);
    backdrop-filter: blur(20px);
    position: sticky;
    top: 0;
    z-index: 100;
}
.th-logo {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 17px;
    font-weight: 700;
    letter-spacing: -0.3px;
    color: var(--text-primary);
}
.th-logo-icon {
    width: 32px; height: 32px;
    background: linear-gradient(135deg, var(--coral), #ff9966);
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 16px;
    box-shadow: 0 0 20px var(--coral-glow);
}
.th-badges { display: flex; align-items: center; gap: 8px; }
.th-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 500;
    font-family: var(--font);
    border: 1px solid var(--border);
    background: var(--bg-elevated);
    color: var(--text-secondary);
    letter-spacing: 0.2px;
}
.th-badge .dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--teal);
    box-shadow: 0 0 6px var(--teal);
}
.th-coral-badge {
    background: linear-gradient(135deg, var(--coral) 0%, #ff9966 100%);
    border: none;
    color: white;
    font-weight: 600;
    box-shadow: 0 0 20px var(--coral-glow);
    padding: 6px 14px;
}

.th-main {
    padding: 28px 32px 40px;
    max-width: 1440px;
    margin: 0 auto;
}

.th-hero {
    background: linear-gradient(135deg,
        rgba(255,107,71,0.06) 0%,
        rgba(19,28,46,0.8) 50%,
        rgba(79,142,247,0.04) 100%
    );
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 28px 32px;
    margin-bottom: 20px;
    position: relative;
    overflow: hidden;
}
.th-hero::after {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(255,107,71,0.12) 0%, transparent 70%);
    pointer-events: none;
}
.th-hero-title { font-size: 26px; font-weight: 700; letter-spacing: -0.5px; color: var(--text-primary); margin-bottom: 4px; }
.th-hero-subtitle { font-size: 14px; color: var(--text-secondary); font-weight: 400; }
.th-hero-date { font-size: 12px; color: var(--text-muted); font-family: var(--mono); margin-top: 2px; }

.th-metric-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 22px 24px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s, transform 0.15s;
    height: 120px;
}
.th-metric-card:hover { border-color: var(--border-bright); transform: translateY(-1px); }
.th-metric-num { font-size: 40px; font-weight: 800; font-family: var(--mono); letter-spacing: -2px; line-height: 1; margin-bottom: 6px; }
.th-metric-label { font-size: 12px; font-weight: 500; text-transform: uppercase; letter-spacing: 1px; color: var(--text-muted); }
.th-metric-icon { position: absolute; top: 20px; right: 20px; font-size: 20px; opacity: 0.5; }
.th-metric-coral .th-metric-num { color: var(--coral); }
.th-metric-teal  .th-metric-num { color: var(--teal); }
.th-metric-blue  .th-metric-num { color: var(--blue); }

.th-section-label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 10px;
    margin-top: 24px;
}

.th-search-wrap {
    background: var(--bg-card);
    border: 1.5px solid var(--border);
    border-radius: 16px;
    padding: 6px 6px 16px;
    margin-bottom: 20px;
    transition: border-color 0.2s;
}
.th-search-wrap:focus-within {
    border-color: var(--coral);
    box-shadow: 0 0 0 3px var(--coral-glow);
}
.th-search-header {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 14px 8px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 10px;
}
.th-search-icon {
    width: 28px; height: 28px;
    background: linear-gradient(135deg, var(--coral), #ff9966);
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 13px;
    flex-shrink: 0;
    box-shadow: 0 0 14px var(--coral-glow);
}
.th-search-title { font-size: 13px; font-weight: 600; color: var(--text-primary); }
.th-search-subtitle { font-size: 11px; color: var(--text-muted); }
.th-chips { display: flex; flex-wrap: wrap; gap: 6px; padding: 0 14px 2px; }
.th-chip {
    font-size: 11px;
    font-weight: 500;
    color: var(--text-muted);
    background: var(--bg-elevated);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 3px 10px;
    font-family: var(--font);
}
.th-chip span { color: var(--text-secondary); margin-right: 4px; }

.th-ai-rec {
    background: linear-gradient(135deg, rgba(255,107,71,0.08) 0%, rgba(19,28,46,0.9) 100%);
    border: 1px solid rgba(255,107,71,0.25);
    border-radius: 16px;
    padding: 22px 24px;
    position: relative;
    overflow: hidden;
}
.th-ai-rec::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    background: linear-gradient(180deg, var(--coral), #ff9966);
    border-radius: 3px 0 0 3px;
}
.th-ai-rec-eyebrow { font-size: 10px; font-weight: 600; letter-spacing: 1.5px; text-transform: uppercase; color: var(--coral); margin-bottom: 6px; display: flex; align-items: center; gap: 6px; }
.th-ai-rec-task { font-size: 20px; font-weight: 700; letter-spacing: -0.3px; color: var(--text-primary); margin-bottom: 12px; }
.th-ai-rec-reasons { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 14px; }
.th-reason-pill { font-size: 11px; font-weight: 500; padding: 3px 10px; border-radius: 20px; font-family: var(--font); }
.th-reason-pill.priority { background: rgba(255,107,71,0.12); color: var(--coral); border: 1px solid rgba(255,107,71,0.2); }
.th-reason-pill.schedule { background: var(--teal-subtle); color: var(--teal); border: 1px solid rgba(0,212,170,0.2); }
.th-reason-pill.impact   { background: var(--blue-subtle); color: var(--blue); border: 1px solid rgba(79,142,247,0.2); }
.th-confidence-bar-wrap { display: flex; align-items: center; gap: 10px; }
.th-confidence-bar-bg { flex: 1; height: 4px; background: var(--border); border-radius: 2px; overflow: hidden; }
.th-confidence-bar-fill { height: 100%; background: linear-gradient(90deg, var(--coral), #ff9966); border-radius: 2px; box-shadow: 0 0 6px var(--coral-glow); }
.th-confidence-pct { font-family: var(--mono); font-size: 11px; color: var(--coral); min-width: 36px; text-align: right; }

.th-panel { background: var(--bg-card); border: 1px solid var(--border); border-radius: 16px; padding: 20px; height: 100%; }
.th-panel-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px; }
.th-panel-title { font-size: 13px; font-weight: 600; color: var(--text-primary); display: flex; align-items: center; gap: 7px; }
.th-panel-count { font-size: 11px; font-weight: 500; background: var(--bg-elevated); border: 1px solid var(--border); border-radius: 10px; padding: 2px 8px; color: var(--text-muted); font-family: var(--mono); }

.th-task-row { display: flex; align-items: center; gap: 10px; padding: 8px 0; border-bottom: 1px solid var(--border); }
.th-task-row:last-child { border-bottom: none; }
.th-task-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.th-task-dot.high   { background: var(--coral); box-shadow: 0 0 6px var(--coral-glow); }
.th-task-dot.medium { background: var(--yellow); box-shadow: 0 0 6px rgba(245,200,66,0.3); }
.th-task-dot.low    { background: var(--teal);   box-shadow: 0 0 6px rgba(0,212,170,0.2); }
.th-task-name { flex: 1; font-size: 13px; font-weight: 500; color: var(--text-primary); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.th-task-category { font-size: 10px; font-weight: 500; padding: 2px 7px; border-radius: 8px; background: var(--bg-elevated); border: 1px solid var(--border); color: var(--text-muted); flex-shrink: 0; }
.th-status-badge { font-size: 10px; font-weight: 600; padding: 2px 8px; border-radius: 8px; flex-shrink: 0; font-family: var(--mono); letter-spacing: 0.3px; }
.th-status-badge.todo        { background: var(--yellow-subtle); color: var(--yellow); border: 1px solid rgba(245,200,66,0.2); }
.th-status-badge.inprogress  { background: var(--blue-subtle); color: var(--blue); border: 1px solid rgba(79,142,247,0.2); }
.th-status-badge.done        { background: var(--teal-subtle); color: var(--teal); border: 1px solid rgba(0,212,170,0.2); }

.th-event-row { display: flex; align-items: flex-start; gap: 12px; padding: 9px 0; border-bottom: 1px solid var(--border); }
.th-event-row:last-child { border-bottom: none; }
.th-event-time-block { min-width: 58px; text-align: center; background: var(--bg-elevated); border: 1px solid var(--border); border-radius: 8px; padding: 5px 6px; flex-shrink: 0; }
.th-event-time { font-family: var(--mono); font-size: 11px; font-weight: 500; color: var(--blue); white-space: nowrap; }
.th-event-name { font-size: 13px; font-weight: 500; color: var(--text-primary); }
.th-event-meta { font-size: 11px; color: var(--text-muted); margin-top: 2px; }

.th-email-row { display: flex; align-items: center; gap: 10px; padding: 8px 0; border-bottom: 1px solid var(--border); }
.th-email-row:last-child { border-bottom: none; }
.th-email-avatar { width: 28px; height: 28px; border-radius: 50%; background: linear-gradient(135deg, var(--coral), #ff9966); display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 700; color: white; flex-shrink: 0; }
.th-email-from { font-size: 12px; font-weight: 600; color: var(--text-primary); }
.th-email-subject { font-size: 11px; color: var(--text-secondary); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.th-unread-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--coral); box-shadow: 0 0 6px var(--coral-glow); flex-shrink: 0; }

/* ── Query result section heading ── */
.th-result-heading {
    font-family: var(--font);
    font-size: 14px;
    font-weight: 600;
    color: var(--text-primary);
    padding: 14px 0 10px;
    letter-spacing: -0.2px;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* ── Focus summary cards ── */
.th-focus-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 16px; }
.th-focus-stat {
    background: var(--bg-elevated);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px;
    text-align: center;
}
.th-focus-stat-num { font-size: 28px; font-weight: 800; font-family: var(--mono); letter-spacing: -1px; margin-bottom: 4px; }
.th-focus-stat-label { font-size: 11px; font-weight: 500; text-transform: uppercase; letter-spacing: 0.8px; color: var(--text-muted); }
.th-action-plan {
    background: var(--bg-elevated);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 16px;
}
.th-action-plan-title { font-size: 12px; font-weight: 600; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px; }
.th-action-step { display: flex; align-items: center; gap: 10px; padding: 7px 0; border-bottom: 1px solid var(--border); font-size: 13px; color: var(--text-primary); }
.th-action-step:last-child { border-bottom: none; }
.th-action-step-num { font-family: var(--mono); font-size: 11px; color: var(--coral); font-weight: 600; min-width: 20px; }

/* ── GitHub notification card ── */
.th-notif-row { display: flex; align-items: center; gap: 10px; padding: 9px 0; border-bottom: 1px solid var(--border); }
.th-notif-row:last-child { border-bottom: none; }
.th-notif-icon { font-size: 16px; flex-shrink: 0; }
.th-notif-subject { font-size: 13px; font-weight: 500; color: var(--text-primary); flex: 1; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.th-notif-time { font-size: 10px; font-family: var(--mono); color: var(--text-muted); flex-shrink: 0; }

/* ── Empty state ── */
.th-empty {
    text-align: center;
    padding: 24px;
    color: var(--text-muted);
    font-size: 13px;
}

/* ── Buttons ── */
.stButton > button {
    background: var(--bg-elevated) !important;
    color: var(--text-secondary) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    font-family: var(--font) !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    padding: 7px 14px !important;
    transition: all 0.15s !important;
    box-shadow: none !important;
    white-space: nowrap !important;
}
.stButton > button:hover { border-color: var(--border-bright) !important; color: var(--text-primary) !important; background: var(--bg-card) !important; }
.stButton > button:active { background: var(--coral-subtle) !important; border-color: var(--coral) !important; color: var(--coral) !important; }

/* ── Text input ── */
.stTextInput > div > div > input {
    background: var(--bg-elevated) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 12px !important;
    color: var(--text-primary) !important;
    font-family: var(--font) !important;
    font-size: 14px !important;
    padding: 10px 16px !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stTextInput > div > div > input:focus { border-color: var(--coral) !important; box-shadow: 0 0 0 3px var(--coral-glow) !important; }
.stTextInput > div > div > input::placeholder { color: var(--text-muted) !important; }
.stTextInput label { display: none !important; }

/* ── Native Streamlit overrides (alerts, dividers) ── */
.stAlert { background: rgba(79,142,247,0.07) !important; border: 1px solid rgba(79,142,247,0.2) !important; border-radius: 12px !important; color: var(--text-secondary) !important; font-family: var(--font) !important; }
hr { border-color: var(--border) !important; margin: 20px 0 !important; }
[data-testid="stHorizontalBlock"] { gap: 12px !important; }
.th-spacer { height: 20px; }
</style>
""",
    unsafe_allow_html=True,
)  # FIX 1 applied here


# ─── SERVICE IMPORTS WITH MOCK FALLBACK ─────────────────────────────────────
# FIX 5: Real services are attempted first; mock data is only used if imports fail.
# Remove the try/except fallback block once your real services are confirmed working.
try:
    from services.notion import get_tasks
    from services.google_calendar import get_upcoming_events, get_todays_events
    from services.gmail import get_unread_emails

    _USE_REAL = True
except ImportError:
    _USE_REAL = False


@st.cache_data(ttl=60)
def load_tasks():
    return get_tasks()


@st.cache_data(ttl=60)
def load_events():
    return get_upcoming_events()


@st.cache_data(ttl=60)
def load_emails():
    return get_unread_emails()


@st.cache_data(ttl=60)
def load_today_events():
    return get_todays_events()


if _USE_REAL:

    tasks_raw = load_tasks()
    events_raw = load_events()
    today_events_raw = load_today_events()
    emails_raw = load_emails()
else:
    # ── MOCK DATA — remove this block once real services are wired ──
    tasks_raw = [
        {
            "Task": "DSA: Solve 2 DP Problems",
            "Priority": "High",
            "Status": "Todo",
            "Category": "DSA",
        },
        {
            "Task": "Build Coral Integration API",
            "Priority": "High",
            "Status": "Todo",
            "Category": "Dev",
        },
        {
            "Task": "Review PR #42",
            "Priority": "Medium",
            "Status": "In Progress",
            "Category": "Dev",
        },
        {
            "Task": "Write blog post on AI",
            "Priority": "Medium",
            "Status": "Todo",
            "Category": "Content",
        },
        {
            "Task": "LeetCode: Tree Traversal",
            "Priority": "High",
            "Status": "Todo",
            "Category": "DSA",
        },
        {
            "Task": "Update Notion docs",
            "Priority": "Low",
            "Status": "Done",
            "Category": "Docs",
        },
    ]
    events_raw = [
        {
            "Event": "Team Standup",
            "Start": "09:00 AM",
            "Duration": "30 min",
            "Type": "Meeting",
        },
        {
            "Event": "Coral Hackathon Sync",
            "Start": "11:00 AM",
            "Duration": "1 hr",
            "Type": "Meeting",
        },
        {
            "Event": "Design Review",
            "Start": "02:00 PM",
            "Duration": "45 min",
            "Type": "Review",
        },
        {
            "Event": "1:1 with Mentor",
            "Start": "04:00 PM",
            "Duration": "30 min",
            "Type": "Meeting",
        },
        {
            "Event": "Deep Work Block",
            "Start": "05:00 PM",
            "Duration": "2 hrs",
            "Type": "Focus",
        },
    ]
    today_events_raw = events_raw.copy()
    emails_raw = [
        {"From": "GitHub", "Subject": "PR #42 approved by reviewer", "Time": "2m ago"},
        {
            "From": "Notion HQ",
            "Subject": "Your workspace export is ready",
            "Time": "18m ago",
        },
        {
            "From": "Google Calendar",
            "Subject": "Reminder: Team Standup in 30 minutes",
            "Time": "45m ago",
        },
        {
            "From": "Coral Platform",
            "Subject": "Your API keys are live 🚀",
            "Time": "1h ago",
        },
        {"From": "LinkedIn", "Subject": "3 new connection requests", "Time": "3h ago"},
    ]

df = pd.DataFrame(tasks_raw)
events_df = pd.DataFrame(events_raw)
today_events_df = pd.DataFrame(today_events_raw)
emails_df = pd.DataFrame(emails_raw)


# ─── HTML CARD RENDERERS ────────────────────────────────────────────────────
# FIX 2 + 4: Replaced all st.dataframe() calls with themed HTML card builders.
# FIX 4 (data escaping): Every user-data string is passed through _html.escape()
#   to prevent raw data containing <, >, &, or " from breaking the HTML parser.


def _e(s):
    """HTML-escape a value safely."""
    return _html.escape(str(s))


def render_task_cards(data_df, container_class="th-panel"):
    """Render a DataFrame of tasks as styled th-task-row cards."""
    if data_df is None or len(data_df) == 0:
        st.markdown(
            '<div class="th-empty">No tasks found.</div>', unsafe_allow_html=True
        )
        return
    rows = ""
    for _, row in data_df.iterrows():
        dot_cls = _e(row.get("Priority", "")).lower()
        status_raw = _e(row.get("Status", ""))
        status_cls = status_raw.lower().replace(" ", "")
        rows += f"""
        <div class="th-task-row">
          <div class="th-task-dot {dot_cls}"></div>
          <div class="th-task-name">{_e(row.get('Task',''))}</div>
          <div class="th-task-category">{_e(row.get('Category',''))}</div>
          <div class="th-status-badge {status_cls}">{status_raw}</div>
        </div>"""
    st.markdown(
        f"""
    <div class="{container_class}">
      <div class="th-panel-header">
        <div class="th-panel-title">📋 Tasks</div>
        <span class="th-panel-count">{len(data_df)}</span>
      </div>
      {rows}
    </div>""",
        unsafe_allow_html=True,
    )


def render_event_cards(data_df, title="📅 Events", container_class="th-panel"):
    """Render a DataFrame of events as styled th-event-row cards."""
    if data_df is None or len(data_df) == 0:
        st.markdown(
            '<div class="th-empty">No events found.</div>', unsafe_allow_html=True
        )
        return
    rows = ""
    for _, row in data_df.iterrows():
        rows += f"""
        <div class="th-event-row">
          <div class="th-event-time-block">
            <div class="th-event-time">{_e(row.get('Start',''))}</div>
          </div>
          <div style="min-width:0;">
            <div class="th-event-name">{_e(row.get('Event',''))}</div>
            <div class="th-event-meta">{_e(row.get('Duration',''))} &nbsp;·&nbsp; {_e(row.get('Type',''))}</div>
          </div>
        </div>"""
    st.markdown(
        f"""
    <div class="{container_class}">
      <div class="th-panel-header">
        <div class="th-panel-title">{title}</div>
        <span class="th-panel-count">{len(data_df)}</span>
      </div>
      {rows}
    </div>""",
        unsafe_allow_html=True,
    )


def render_email_cards(data_df, title="📧 Inbox", container_class="th-panel"):
    """Render a DataFrame of emails as styled th-email-row cards."""
    if data_df is None or len(data_df) == 0:
        st.markdown(
            '<div class="th-empty">No emails found.</div>', unsafe_allow_html=True
        )
        return
    rows = ""
    for _, row in data_df.iterrows():
        sender = _e(row.get("From", "?"))
        avatar = sender[0].upper() if sender else "?"
        rows += f"""
        <div class="th-email-row">
          <div class="th-unread-dot"></div>
          <div class="th-email-avatar">{avatar}</div>
          <div style="flex:1;min-width:0;">
            <div class="th-email-from">{sender}</div>
            <div class="th-email-subject">{_e(row.get('Subject',''))}</div>
          </div>
          <div style="font-size:10px;color:var(--text-muted);font-family:var(--mono);flex-shrink:0;">{_e(row.get('Time',''))}</div>
        </div>"""
    st.markdown(
        f"""
    <div class="{container_class}">
      <div class="th-panel-header">
        <div class="th-panel-title">{title}</div>
        <span class="th-panel-count">{len(data_df)}</span>
      </div>
      {rows}
    </div>""",
        unsafe_allow_html=True,
    )


def render_github_cards(data_df):
    """Render GitHub notification emails as styled notification cards."""
    if data_df is None or len(data_df) == 0:
        st.markdown(
            '<div class="th-panel"><div class="th-empty">No GitHub notifications found.</div></div>',
            unsafe_allow_html=True,
        )
        return
    rows = ""
    for _, row in data_df.iterrows():
        rows += f"""
        <div class="th-notif-row">
          <div class="th-notif-icon">🐙</div>
          <div class="th-notif-subject">{_e(row.get('Subject',''))}</div>
          <div class="th-notif-time">{_e(row.get('Time',''))}</div>
        </div>"""
    st.markdown(
        f"""
    <div class="th-panel">
      <div class="th-panel-header">
        <div class="th-panel-title">🐙 GitHub Notifications</div>
        <span class="th-panel-count">{len(data_df)}</span>
      </div>
      {rows}
    </div>""",
        unsafe_allow_html=True,
    )


def render_focus_summary(high_priority_df, today_events_df_, emails_df_):
    """Render the focus summary with stat cards and an action plan — no st.metric()."""
    # FIX 3: Replaced st.metric() with themed HTML stat cards
    st.markdown(
        f"""
    <div class="th-focus-grid">
      <div class="th-focus-stat">
        <div class="th-focus-stat-num" style="color:var(--coral);">{len(high_priority_df)}</div>
        <div class="th-focus-stat-label">High Priority Tasks</div>
      </div>
      <div class="th-focus-stat">
        <div class="th-focus-stat-num" style="color:var(--teal);">{len(today_events_df_)}</div>
        <div class="th-focus-stat-label">Events Today</div>
      </div>
      <div class="th-focus-stat">
        <div class="th-focus-stat-num" style="color:var(--blue);">{len(emails_df_)}</div>
        <div class="th-focus-stat-label">Unread Emails</div>
      </div>
    </div>
    <div class="th-action-plan">
      <div class="th-action-plan-title">Recommended Action Plan</div>
      <div class="th-action-step"><span class="th-action-step-num">01</span>Complete high-priority pending tasks</div>
      <div class="th-action-step"><span class="th-action-step-num">02</span>Prepare for today's calendar events</div>
      <div class="th-action-step"><span class="th-action-step-num">03</span>Review important unread emails</div>
      <div class="th-action-step"><span class="th-action-step-num">04</span>Check GitHub notifications and PR updates</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    if len(high_priority_df) > 0:
        render_task_cards(high_priority_df)
    else:
        st.markdown(
            '<div class="th-empty">No high-priority tasks for today.</div>',
            unsafe_allow_html=True,
        )


# ─── TOPBAR ─────────────────────────────────────────────────────────────────
# FIX 1: unsafe_allow_html=True on every st.markdown with HTML
st.markdown(
    """
<div class="th-topbar">
  <div class="th-logo">
    <div class="th-logo-icon">🚀</div>
    Task Harbor AI
  </div>
  <div class="th-badges">
    <span class="th-badge"><span class="dot"></span>Notion</span>
    <span class="th-badge"><span class="dot"></span>Google Calendar</span>
    <span class="th-badge"><span class="dot"></span>Gmail</span>
    <span class="th-badge th-coral-badge">⚡ Powered by Coral</span>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown('<div class="th-main">', unsafe_allow_html=True)

# ─── HERO ───────────────────────────────────────────────────────────────────
now = datetime.now()
greeting = (
    "Good morning"
    if now.hour < 12
    else ("Good afternoon" if now.hour < 18 else "Good evening")
)
date_str = now.strftime("%A, %B %d · %I:%M %p")

st.markdown(
    f"""
<div class="th-hero">
  <div class="th-hero-title">{greeting}, Sathish 👋</div>
  <div class="th-hero-subtitle">Here's your productivity snapshot — you have high-priority tasks waiting.</div>
  <div class="th-hero-date">{date_str}</div>
</div>
""",
    unsafe_allow_html=True,
)

# ─── METRICS ────────────────────────────────────────────────────────────────
m1, m2, m3 = st.columns(3)
high_count = len(df[df["Priority"] == "High"])

with m1:
    st.markdown(
        f"""
    <div class="th-metric-card th-metric-coral">
      <span class="th-metric-icon">📋</span>
      <div class="th-metric-num">{len(df)}</div>
      <div class="th-metric-label">Total Tasks &nbsp;·&nbsp; {high_count} high priority</div>
    </div>""",
        unsafe_allow_html=True,
    )

with m2:
    st.markdown(
        f"""
    <div class="th-metric-card th-metric-teal">
      <span class="th-metric-icon">📅</span>
      <div class="th-metric-num">{len(events_df)}</div>
      <div class="th-metric-label">Events Today</div>
    </div>""",
        unsafe_allow_html=True,
    )

with m3:
    st.markdown(
        f"""
    <div class="th-metric-card th-metric-blue">
      <span class="th-metric-icon">📧</span>
      <div class="th-metric-num">{len(emails_df)}</div>
      <div class="th-metric-label">Unread Emails</div>
    </div>""",
        unsafe_allow_html=True,
    )

# ─── AI SEARCH ──────────────────────────────────────────────────────────────
st.markdown('<div class="th-section-label">AI Assistant</div>', unsafe_allow_html=True)
st.markdown(
    """
<div class="th-search-wrap">
  <div class="th-search-header">
    <div class="th-search-icon">✦</div>
    <div>
      <div class="th-search-title">Ask Task Harbor AI</div>
      <div class="th-search-subtitle">Powered by Coral — queries across Notion, Calendar &amp; Gmail</div>
    </div>
  </div>
  <div class="th-chips">
    <span class="th-chip"><span>→</span>What should I focus on today?</span>
    <span class="th-chip"><span>→</span>Show high priority tasks</span>
    <span class="th-chip"><span>→</span>What meetings do I have today?</span>
    <span class="th-chip"><span>→</span>Show GitHub notifications</span>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

btn_col1, btn_col2, btn_col3, _sp = st.columns([1, 1, 1, 5])
with btn_col1:
    focus_btn = st.button("🎯 Focus")
with btn_col2:
    github_btn = st.button("🐙 GitHub")
with btn_col3:
    meetings_btn = st.button("📅 Meetings")

question = st.text_input(
    label="query",
    placeholder="What should I work on today?",
    label_visibility="collapsed",
)

# ─── AI RECOMMENDATION ──────────────────────────────────────────────────────
high_priority = df[(df["Priority"] == "High") & (df["Status"] == "Todo")]

if len(high_priority) > 0:
    task_name = _e(high_priority.iloc[0]["Task"])
    cat = _e(high_priority.iloc[0]["Category"])
    st.markdown(
        f"""
    <div class="th-ai-rec">
      <div class="th-ai-rec-eyebrow">✦ AI Recommendation &nbsp;·&nbsp; Focus Today</div>
      <div class="th-ai-rec-task">{task_name}</div>
      <div class="th-ai-rec-reasons">
        <span class="th-reason-pill priority">🔴 High Priority</span>
        <span class="th-reason-pill schedule">✓ No Schedule Conflicts</span>
        <span class="th-reason-pill impact">⚡ Highest Impact Today</span>
        <span class="th-reason-pill impact" style="background:var(--yellow-subtle);color:var(--yellow);border-color:rgba(245,200,66,0.2);">📂 {cat}</span>
      </div>
      <div class="th-confidence-bar-wrap">
        <div class="th-confidence-bar-bg">
          <div class="th-confidence-bar-fill" style="width:92%"></div>
        </div>
        <span class="th-confidence-pct">92%</span>
      </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

st.markdown('<div class="th-spacer"></div>', unsafe_allow_html=True)

# ─── QUERY HANDLING ─────────────────────────────────────────────────────────
# FIX 2: All st.dataframe() and st.subheader() replaced with themed HTML card functions.
# FIX 3: st.metric() replaced with render_focus_summary().
# Results render directly below the search box — no layout jumps.

# Resolve active query — only one source wins (button > text input)
q = ""
if focus_btn:
    q = "focus"
elif github_btn:
    q = "github"
elif meetings_btn:
    q = "meetings today"
elif question:
    q = question.strip().lower()


import time

if q:

    if "high" in q:
        result = df[df["Priority"] == "High"]
        st.markdown(
            '<div class="th-result-heading">🔥 High Priority Tasks</div>',
            unsafe_allow_html=True,
        )
        render_task_cards(result)

    elif "todo" in q:
        result = df[df["Status"] == "Todo"]
        st.markdown(
            '<div class="th-result-heading">📋 Todo Tasks</div>', unsafe_allow_html=True
        )
        render_task_cards(result)

    elif "dsa" in q:
        result = df[df["Category"] == "DSA"]
        st.markdown(
            '<div class="th-result-heading">🧠 DSA Tasks</div>', unsafe_allow_html=True
        )
        render_task_cards(result)

    elif "next event" in q:
        st.markdown(
            '<div class="th-result-heading">📅 Next Event</div>', unsafe_allow_html=True
        )
        if len(events_raw) > 0:
            ev = events_raw[0]
            st.markdown(
                f"""
            <div class="th-panel">
              <div class="th-event-row">
                <div class="th-event-time-block">
                  <div class="th-event-time">{_e(ev.get('Start',''))}</div>
                </div>
                <div>
                  <div class="th-event-name">{_e(ev.get('Event',''))}</div>
                  <div class="th-event-meta">{_e(ev.get('Duration',''))} &nbsp;·&nbsp; {_e(ev.get('Type',''))}</div>
                </div>
              </div>
            </div>""",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div class="th-empty">No upcoming events found.</div>',
                unsafe_allow_html=True,
            )

    elif "meeting" in q or ("today" in q and "event" in q):
        st.markdown(
            '<div class="th-result-heading">📅 Today\'s Schedule</div>',
            unsafe_allow_html=True,
        )
        if len(today_events_df) > 0:
            render_event_cards(today_events_df)
        else:
            st.markdown(
                '<div class="th-empty">No meetings scheduled for today.</div>',
                unsafe_allow_html=True,
            )

    elif "calendar" in q or "events" in q:
        st.markdown(
            '<div class="th-result-heading">📅 Upcoming Events</div>',
            unsafe_allow_html=True,
        )
        render_event_cards(events_df)

    elif "github" in q:
        github_emails = emails_df[
            emails_df["From"].str.contains("github", case=False, na=False)
        ]
        render_github_cards(github_emails)

    elif "email" in q:
        st.markdown(
            '<div class="th-result-heading">📧 Unread Emails</div>',
            unsafe_allow_html=True,
        )
        render_email_cards(emails_df)

    elif "focus" in q or "work on today" in q or "what should" in q:
        st.markdown(
            '<div class="th-result-heading">🎯 Today\'s Productivity Summary</div>',
            unsafe_allow_html=True,
        )
        render_focus_summary(high_priority, today_events_df, emails_df)

    else:
        st.markdown(
            """
        <div class="th-panel" style="border-color:rgba(245,200,66,0.2);background:var(--yellow-subtle);">
          <div style="color:var(--yellow);font-size:13px;font-weight:500;">
            ⚠️ I don't understand that yet — try asking about tasks, emails, events, or GitHub.
          </div>
        </div>""",
            unsafe_allow_html=True,
        )

# ─── DASHBOARD PANELS ───────────────────────────────────────────────────────
st.markdown('<div class="th-section-label">Workspace</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["📋 Tasks", "📅 Calendar", "📧 Emails", "🐙 GitHub"])

with tab1:
    st.markdown(
        "<h1 style='color:red'>TASK TEST</h1>",
        unsafe_allow_html=True
    )

with tab2:
    render_event_cards(events_df)

with tab3:
    render_email_cards(emails_df)

with tab4:
    github_emails = emails_df[
        emails_df["From"].str.contains("github", case=False, na=False)
    ]
    render_github_cards(github_emails)
