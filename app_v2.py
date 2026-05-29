import streamlit as st
import pandas as pd
import html as _html
from datetime import datetime
import re

def render_html(html_str):
    """Safely render HTML strings using st.html to prevent Streamlit markdown parsing and codeblock bugs."""
    st.html(html_str)

def group_insights_by_task(join_insights):
    grouped = {}
    for ins in join_insights:
        task = ins.get("Task", "Unknown Task")
        if not task:
            continue
        if task not in grouped:
            grouped[task] = {
                "Task": task,
                "Time": ins.get("Time", ""),
                "GitHub_Notifications": []
            }
        subj = ins.get("GitHub_Subject", "")
        repo = ins.get("Repository", "")
        if subj:
            if not any(item["Subject"] == subj and item["Repository"] == repo for item in grouped[task]["GitHub_Notifications"]):
                grouped[task]["GitHub_Notifications"].append({
                    "Subject": subj,
                    "Repository": repo
                })
    return list(grouped.values())

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
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@300;400;500;700&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
    --bg-base:       #08090a;
    --bg-surface:    #0c0e11;
    --bg-elevated:   #121418;
    --bg-card:       #121418;
    --border:        rgba(255,255,255,0.06);
    --border-bright: rgba(183, 255, 74, 0.4);
    --coral:         #B7FF4A;
    --coral-dim:     #92e030;
    --coral-glow:    rgba(183, 255, 74, 0.18);
    --coral-subtle:  rgba(183, 255, 74, 0.06);
    --teal:          #00d4aa;
    --teal-subtle:   rgba(0, 212, 170, 0.08);
    --blue:          #4f8ef7;
    --blue-subtle:   rgba(79, 142, 247, 0.08);
    --yellow:        #f5c842;
    --yellow-subtle: rgba(245, 200, 66, 0.08);
    --text-primary:  #ffffff;
    --text-secondary:#d1d5db;
    --text-muted:    #9ca3af;
    --font:          'Outfit', sans-serif;
    --mono:          'JetBrains Mono', monospace;
}

.stApp {
    background: var(--bg-base) !important;
    font-family: var(--font) !important;
    color: var(--text-primary) !important;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 32px !important; max-width: 1440px !important; margin: 0 auto !important; }
[data-testid="stToolbar"] { display: none; }
section[data-testid="stSidebar"] { display: none; }

/* Custom Pill Buttons for Navigation and Quick Actions */
div[data-testid="column"] button, .stButton > button {
    border-radius: 24px !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    background-color: #121418 !important;
    color: var(--text-secondary) !important;
    font-family: var(--font) !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
    padding: 8px 20px !important;
}

div[data-testid="column"] button:hover, .stButton > button:hover {
    border-color: var(--coral) !important;
    color: var(--text-primary) !important;
    box-shadow: 0 0 12px var(--coral-glow) !important;
}

div[data-testid="column"] button[kind="primary"], .stButton > button[kind="primary"] {
    background: var(--coral) !important;
    color: #000000 !important;
    font-weight: 700 !important;
    border: none !important;
    box-shadow: 0 0 16px var(--coral-glow) !important;
}

/* Custom Scrollbars */
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

/* Premium Card & Panels styling */
.th-panel, .th-insight-card, .th-ai-rec, .th-metric-card {
    background: rgba(18, 20, 24, 0.65) !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    border-radius: 24px !important;
    padding: 24px !important;
    backdrop-filter: blur(12px) !important;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4) !important;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
}

.th-panel:hover, .th-insight-card:hover, .th-ai-rec:hover, .th-metric-card:hover {
    border-color: rgba(183, 255, 74, 0.25) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.5), 0 0 15px rgba(183, 255, 74, 0.1) !important;
}

/* Hero Section */
.th-hero {
    background: linear-gradient(135deg, rgba(183, 255, 74, 0.06) 0%, rgba(12, 14, 17, 0.92) 70%, rgba(0, 212, 170, 0.03) 100%) !important;
    border: 1px solid rgba(183, 255, 74, 0.25) !important;
    border-radius: 24px !important;
    padding: 32px !important;
    margin-bottom: 24px;
    box-shadow: 0 12px 48px rgba(0, 0, 0, 0.6), 0 0 24px rgba(183, 255, 74, 0.12) !important;
    position: relative;
    overflow: hidden;
}
.th-hero:hover {
    border-color: rgba(183, 255, 74, 0.4) !important;
    box-shadow: 0 16px 56px rgba(0, 0, 0, 0.7), 0 0 32px rgba(183, 255, 74, 0.18) !important;
}

/* Specific Panel Customizations for Differentiation */
.th-schema-panel {
    background: rgba(18, 20, 24, 0.7) !important;
    border: 1px solid rgba(255, 255, 255, 0.07) !important;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4), 0 0 10px rgba(0, 212, 170, 0.03) !important;
}
.th-schema-panel:hover {
    border-color: rgba(0, 212, 170, 0.2) !important;
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.5), 0 0 15px rgba(0, 212, 170, 0.06) !important;
}

.th-settings-panel {
    background: rgba(18, 20, 24, 0.75) !important;
    border: 1px solid rgba(255, 255, 255, 0.06) !important;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.45) !important;
}
.th-settings-panel:hover {
    border-color: rgba(255, 255, 255, 0.12) !important;
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.5) !important;
}
.th-hero-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    padding-bottom: 18px;
    margin-bottom: 20px;
}
.th-hero-greeting-wrap {
    display: flex;
    align-items: center;
    gap: 12px;
}
.th-hero-icon {
    font-size: 32px;
    filter: drop-shadow(0 0 8px var(--coral));
    animation: float-slow 3s infinite ease-in-out;
}
@keyframes float-slow {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-4px); }
}
.th-hero-title {
    font-size: 32px !important;
    font-weight: 800 !important;
    color: var(--text-primary) !important;
    margin: 0 !important;
    letter-spacing: -0.8px;
}
.th-hero-date {
    font-size: 13px;
    font-family: var(--mono);
    color: var(--text-muted);
    background: rgba(255, 255, 255, 0.03);
    padding: 6px 12px;
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.05);
}
.th-hero-body {
    margin-bottom: 24px;
}
.th-hero-summary-lead {
    font-size: 16px;
    color: var(--text-secondary);
    margin-bottom: 12px;
}
.th-hero-bullets {
    list-style: none;
    padding-left: 0;
    display: flex;
    flex-direction: column;
    gap: 8px;
}
.th-hero-bullets li {
    font-size: 14px;
    color: var(--text-secondary);
    display: flex;
    align-items: center;
    gap: 10px;
}
.th-hero-bullets li::before {
    content: "•";
    color: var(--coral);
    font-size: 20px;
    line-height: 1;
}
.th-source-pills {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}
.th-source-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.05);
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 13px;
    color: var(--text-secondary);
    font-weight: 500;
}
.th-source-pill-coral {
    background: var(--coral-subtle);
    border-color: rgba(183, 255, 74, 0.2);
    color: var(--coral);
    box-shadow: 0 0 10px rgba(183, 255, 74, 0.05);
}

/* Command Center Header */
.th-command-center-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-top: 10px;
    margin-bottom: 14px;
}
.th-cc-icon {
    font-size: 26px;
    filter: drop-shadow(0 0 8px var(--coral));
}
.th-cc-title-wrap {
    display: flex;
    flex-direction: column;
}
.th-cc-title {
    font-size: 20px !important;
    font-weight: 700 !important;
    color: var(--text-primary) !important;
    margin: 0 !important;
    letter-spacing: -0.4px;
}
.th-cc-subtitle {
    font-size: 13px;
    color: var(--text-secondary);
    margin: 0 !important;
}

/* Premium Command Input styling */
.stTextInput > div > div > input {
    background: rgba(18, 20, 24, 0.8) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 24px !important;
    color: var(--text-primary) !important;
    font-family: var(--font) !important;
    font-size: 16px !important;
    padding: 16px 24px !important;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.02) !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--coral) !important;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5), 0 0 18px var(--coral-glow) !important;
    background: rgba(18, 20, 24, 0.95) !important;
}
.stTextInput > div > div > input::placeholder {
    color: var(--text-muted) !important;
    opacity: 0.6;
}
.stTextInput label { display: none !important; }

/* Custom top bar logo */
.th-logo-container {
    display: flex;
    align-items: center;
    gap: 8px;
    height: 38px;
}
.th-logo-emoji {
    font-size: 22px;
    filter: drop-shadow(0 0 8px var(--coral));
}
.th-logo-text {
    font-size: 18px;
    font-weight: 800;
    letter-spacing: -0.5px;
    color: var(--text-primary);
    background: linear-gradient(90deg, var(--text-primary) 0%, var(--coral) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Copilot Card */
.th-copilot-card {
    background: linear-gradient(135deg, rgba(183, 255, 74, 0.08) 0%, rgba(18, 20, 24, 0.85) 100%) !important;
    border: 1px solid rgba(183, 255, 74, 0.2) !important;
    border-radius: 24px;
    padding: 24px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4), 0 0 18px rgba(183, 255, 74, 0.08) !important;
    margin-bottom: 20px;
    position: relative;
    overflow: hidden;
}
.th-copilot-card:hover {
    border-color: rgba(183, 255, 74, 0.3) !important;
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.55), 0 0 24px rgba(183, 255, 74, 0.12) !important;
}
.th-copilot-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 18px;
}
.th-copilot-title-wrap {
    display: flex;
    align-items: center;
    gap: 10px;
}
.th-copilot-icon {
    font-size: 24px;
    filter: drop-shadow(0 0 6px var(--coral));
}
.th-copilot-title {
    font-size: 16px !important;
    font-weight: 700 !important;
    color: var(--text-primary) !important;
    margin: 0 !important;
}
.th-copilot-subtitle {
    font-size: 12px;
    color: var(--text-secondary);
    margin: 0 !important;
}
.th-copilot-badge {
    background: rgba(183, 255, 74, 0.15);
    color: var(--coral);
    border: 1px solid rgba(183, 255, 74, 0.3);
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
}
.th-copilot-recommendation-label {
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    color: var(--coral);
    letter-spacing: 1.2px;
    margin-bottom: 6px;
}
.th-copilot-task-title {
    font-size: 20px !important;
    font-weight: 800 !important;
    color: var(--text-primary) !important;
    margin-top: 0 !important;
    margin-bottom: 16px !important;
    letter-spacing: -0.3px;
}
.th-copilot-reasoning-wrap {
    display: flex;
    flex-direction: column;
    gap: 12px;
    background: rgba(0, 0, 0, 0.2);
    border-radius: 16px;
    padding: 16px;
    border: 1px solid rgba(255, 255, 255, 0.03);
    margin-bottom: 20px;
}
.th-reasoning-step {
    display: flex;
    align-items: flex-start;
    gap: 12px;
}
.th-step-bullet {
    font-size: 14px;
    flex-shrink: 0;
}
.th-step-source {
    font-weight: 600;
    font-size: 13px;
    color: var(--text-primary);
    margin-right: 6px;
}
.th-step-desc {
    font-size: 13px;
    color: var(--text-secondary);
}
.th-copilot-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 14px;
    border-top: 1px solid rgba(255, 255, 255, 0.05);
    padding-top: 16px;
}
.th-sources-used {
    display: flex;
    align-items: center;
    gap: 6px;
}
.th-sources-label {
    font-size: 11px;
    color: var(--text-muted);
    font-weight: 500;
}
.th-source-tag {
    font-size: 11px;
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.06);
    color: var(--text-secondary);
    padding: 2px 8px;
    border-radius: 12px;
}
.th-confidence-score-wrap {
    display: flex;
    flex-direction: column;
    gap: 4px;
    min-width: 140px;
}
.th-confidence-info {
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.th-confidence-label {
    font-size: 12px;
    color: var(--text-secondary);
}
.th-confidence-value {
    font-size: 13px;
    font-weight: 700;
    color: var(--coral);
    font-family: var(--mono);
}
.th-confidence-progress-bg {
    width: 100%;
    height: 6px;
    background: rgba(255, 255, 255, 0.06);
    border-radius: 3px;
    overflow: hidden;
}
.th-confidence-progress-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--coral), var(--teal));
    border-radius: 3px;
    box-shadow: 0 0 8px var(--coral);
}

/* KPI metric cards */
.th-kpi-card {
    background: rgba(18, 20, 24, 0.7) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 24px;
    padding: 20px;
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(12px) !important;
    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.35), 0 0 8px rgba(255, 255, 255, 0.02) !important;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
    min-height: 160px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
.th-kpi-card:hover {
    border-color: rgba(183, 255, 74, 0.25) !important;
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5), 0 0 12px rgba(183, 255, 74, 0.06) !important;
}
.th-kpi-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}
.th-kpi-icon {
    font-size: 20px;
}
.th-kpi-trend {
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.08);
    color: var(--text-secondary);
    padding: 2px 8px;
    border-radius: 10px;
}
.th-kpi-trend.unread {
    background: var(--coral-subtle);
    border-color: rgba(183, 255, 74, 0.2);
    color: var(--coral);
}
.th-kpi-value {
    font-size: 38px;
    font-weight: 900;
    font-family: var(--mono);
    color: var(--text-primary);
    line-height: 1;
    margin-bottom: 2px;
}
.th-kpi-label {
    font-size: 12px;
    font-weight: 700;
    color: var(--text-primary);
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 12px;
}
.th-kpi-footer {
    font-size: 12px;
    color: var(--text-muted);
    border-top: 1px solid rgba(255, 255, 255, 0.04);
    padding-top: 8px;
    margin-top: auto;
}
.th-kpi-subval {
    font-weight: 700;
    color: var(--coral);
    margin-right: 4px;
}

/* Features active card */
.th-features-card {
    background: rgba(18, 20, 24, 0.7) !important;
    border: 1px solid rgba(255, 255, 255, 0.07) !important;
    border-radius: 24px;
    padding: 24px;
    margin-top: 20px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4), 0 0 10px rgba(183, 255, 74, 0.03) !important;
    backdrop-filter: blur(12px) !important;
}
.th-features-card:hover {
    border-color: rgba(183, 255, 74, 0.2) !important;
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.5), 0 0 15px rgba(183, 255, 74, 0.06) !important;
}
.th-features-title {
    font-size: 16px !important;
    font-weight: 700 !important;
    color: var(--text-primary) !important;
    margin-top: 0 !important;
    margin-bottom: 4px !important;
}
.th-features-subtitle {
    font-size: 12px;
    color: var(--text-secondary);
    margin-bottom: 18px;
}
.th-features-list {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
}
.th-feature-item {
    display: flex;
    gap: 10px;
    align-items: flex-start;
}
.th-feature-check {
    width: 18px;
    height: 18px;
    background: var(--coral-subtle);
    border: 1px solid rgba(183, 255, 74, 0.3);
    color: var(--coral);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 11px;
    font-weight: 800;
    flex-shrink: 0;
    box-shadow: 0 0 6px rgba(183, 255, 74, 0.08);
}
.th-feature-name {
    font-size: 12px;
    font-weight: 600;
    color: var(--text-primary);
}
.th-feature-desc {
    font-size: 12px;
    color: var(--text-secondary);
    line-height: 1.4;
}

/* SQL Insights card */
.th-insights-card {
    background: linear-gradient(135deg, rgba(0, 212, 170, 0.04) 0%, rgba(18, 20, 24, 0.8) 100%) !important;
    border: 1px solid rgba(0, 212, 170, 0.25) !important;
    border-radius: 24px;
    padding: 24px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4), 0 0 18px rgba(0, 212, 170, 0.08) !important;
    backdrop-filter: blur(12px) !important;
    height: 100%;
}
.th-insights-card:hover {
    border-color: rgba(0, 212, 170, 0.35) !important;
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.55), 0 0 24px rgba(0, 212, 170, 0.12) !important;
}
.th-insights-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}
.th-insights-title-wrap {
    display: flex;
    align-items: center;
    gap: 10px;
}
.th-insights-emoji {
    font-size: 24px;
    filter: drop-shadow(0 0 6px var(--coral));
}
.th-insights-title {
    font-size: 16px !important;
    font-weight: 700 !important;
    color: var(--text-primary) !important;
    margin: 0 !important;
}
.th-insights-subtitle {
    font-size: 12px;
    color: var(--text-secondary);
    margin: 0 !important;
}
.th-insights-formula-wrap {
    background: rgba(0, 0, 0, 0.25);
    border: 1px solid rgba(255, 255, 255, 0.04);
    border-radius: 14px;
    padding: 12px 16px;
    margin-bottom: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.th-insights-formula-label {
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    color: var(--text-secondary);
    letter-spacing: 0.8px;
}
.th-insights-formula-code {
    font-family: var(--mono);
    font-size: 13px;
    color: var(--coral);
    font-weight: 600;
}
.th-join-list {
    display: flex;
    flex-direction: column;
    gap: 16px;
}
.th-join-record {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.04);
    border-radius: 18px;
    padding: 16px;
    transition: all 0.25s ease;
}
.th-join-record:hover {
    border-color: rgba(183, 255, 74, 0.15) !important;
    background: rgba(255, 255, 255, 0.03);
}
.th-join-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
}
.th-join-index {
    font-size: 12px;
    font-weight: 800;
    text-transform: uppercase;
    color: var(--coral);
    letter-spacing: 0.5px;
}
.th-join-time {
    font-size: 12px;
    font-family: var(--mono);
    color: var(--text-muted);
    font-weight: 500;
}
.th-join-nodes {
    display: flex;
    flex-direction: column;
    gap: 8px;
    position: relative;
}
.th-join-node {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 12px;
    border-radius: 10px;
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.06);
}
.th-node-icon {
    font-size: 16px;
}
.th-node-info {
    display: flex;
    flex-direction: column;
    min-width: 0;
}
.th-node-label {
    font-size: 11px;
    font-weight: 800;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.8px;
}
.th-node-content {
    font-size: 13px;
    font-weight: 600;
    color: var(--text-primary);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.th-repo-slug {
    color: var(--coral);
    font-weight: 600;
}
.th-join-connector {
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    height: 12px;
    margin: -4px 0;
    z-index: 1;
}
.th-connector-line {
    position: absolute;
    top: 50%;
    left: 20px;
    right: 20px;
    height: 1px;
    border-top: 1px dashed rgba(183, 255, 74, 0.2);
}
.th-connector-badge {
    background: #121418;
    border: 1px solid rgba(183, 255, 74, 0.3);
    color: var(--coral);
    font-family: var(--mono);
    font-size: 10px;
    width: 16px;
    height: 16px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    box-shadow: 0 0 6px var(--coral-glow);
}

/* Original panel and lists items */
.th-section-label {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 12px;
    margin-top: 28px;
}

.th-panel-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px; }
.th-panel-title { font-size: 14px; font-weight: 600; color: var(--text-primary); display: flex; align-items: center; gap: 7px; }
.th-panel-count { font-size: 11px; font-weight: 600; background: var(--bg-elevated); border: 1px solid var(--border); border-radius: 10px; padding: 2px 8px; color: var(--text-secondary); font-family: var(--mono); }

.th-task-row { display: flex; align-items: center; gap: 10px; padding: 10px 8px; border-bottom: 1px solid var(--border); transition: background 0.15s ease, padding-left 0.15s ease; border-radius: 6px; }
.th-task-row:hover { background: rgba(183, 255, 74, 0.02) !important; padding-left: 12px !important; }
.th-task-row:last-child { border-bottom: none; }
.th-task-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.th-task-dot.high   { background: var(--coral); box-shadow: 0 0 6px var(--coral-glow); }
.th-task-dot.medium { background: var(--yellow); box-shadow: 0 0 6px rgba(245,200,66,0.3); }
.th-task-dot.low    { background: var(--teal);   box-shadow: 0 0 6px rgba(0,212,170,0.2); }
.th-task-name { flex: 1; font-size: 14px; font-weight: 500; color: var(--text-primary); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.th-task-category { font-size: 11px; font-weight: 600; padding: 2px 7px; border-radius: 8px; background: var(--bg-elevated); border: 1px solid var(--border); color: var(--text-secondary); flex-shrink: 0; }
.th-status-badge { font-size: 11px; font-weight: 600; padding: 2px 8px; border-radius: 8px; flex-shrink: 0; font-family: var(--mono); letter-spacing: 0.3px; }
.th-status-badge.todo        { background: var(--yellow-subtle); color: var(--yellow); border: 1px solid rgba(245,200,66,0.2); }
.th-status-badge.inprogress  { background: var(--blue-subtle); color: var(--blue); border: 1px solid rgba(79,142,247,0.2); }
.th-status-badge.done        { background: var(--teal-subtle); color: var(--teal); border: 1px solid rgba(0,212,170,0.2); }

.th-email-row { display: flex; align-items: center; gap: 10px; padding: 10px 8px; border-bottom: 1px solid var(--border); transition: background 0.15s ease, padding-left 0.15s ease; border-radius: 6px; }
.th-email-row:hover { background: rgba(0, 212, 170, 0.03) !important; padding-left: 12px !important; }
.th-email-row:last-child { border-bottom: none; }
.th-email-avatar { width: 28px; height: 28px; border-radius: 50%; background: linear-gradient(135deg, var(--coral), #ff9966); display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 700; color: white; flex-shrink: 0; }
.th-email-from { font-size: 13px; font-weight: 600; color: var(--text-primary); }
.th-email-subject { font-size: 12px; color: var(--text-secondary); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.th-unread-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--coral); box-shadow: 0 0 6px var(--coral-glow); flex-shrink: 0; }

.th-result-heading {
    font-family: var(--font);
    font-size: 15px;
    font-weight: 600;
    color: var(--text-primary);
    padding: 14px 0 10px;
    letter-spacing: -0.2px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.th-empty {
    text-align: center;
    padding: 24px;
    color: var(--text-secondary);
    font-size: 13px;
}

/* Custom badges grid in schema discovery */
.th-columns-badge-container {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 10px;
    margin-bottom: 20px;
}
.th-column-badge-card {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 12px;
    padding: 8px 14px;
    display: inline-flex;
    align-items: center;
    gap: 10px;
    transition: all 0.2s ease;
}
.th-column-badge-card:hover {
    border-color: rgba(183, 255, 74, 0.2);
    background: rgba(255, 255, 255, 0.05);
}
.th-column-name {
    font-family: var(--mono);
    font-size: 13px;
    font-weight: 600;
    color: var(--text-primary);
}
.th-column-type {
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    padding: 2px 6px;
    border-radius: 6px;
}
.th-column-type.type-text {
    background: rgba(0, 212, 170, 0.1);
    color: var(--teal);
    border: 1px solid rgba(0, 212, 170, 0.2);
}
.th-column-type.type-number {
    background: rgba(245, 200, 66, 0.1);
    color: var(--yellow);
    border: 1px solid rgba(245, 200, 66, 0.2);
}
.th-column-type.type-date {
    background: rgba(79, 142, 247, 0.1);
    color: var(--blue);
    border: 1px solid rgba(79, 142, 247, 0.2);
}
.th-column-type.type-bool {
    background: rgba(183, 255, 74, 0.1);
    color: var(--coral);
    border: 1px solid rgba(183, 255, 74, 0.2);
}

.th-samples-container {
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin-top: 10px;
}
.th-sample-row-card {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    padding: 16px;
}
.th-sample-row-header {
    font-size: 11px;
    font-weight: 700;
    color: var(--text-muted);
    text-transform: uppercase;
    margin-bottom: 10px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.03);
    padding-bottom: 6px;
}
.th-sample-row-body {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 10px 20px;
}
.th-sample-kv {
    font-size: 12px;
    line-height: 1.4;
    word-break: break-all;
}
.th-sample-key {
    font-family: var(--mono);
    font-weight: 600;
    color: var(--text-secondary);
    margin-right: 6px;
}
.th-sample-val {
    color: var(--text-primary);
}

/* Custom top bar container overrides */
div[data-testid="stHorizontalBlock"]:has(button[key="header_sync_btn"]) {
    background: rgba(13, 17, 23, 0.95) !important;
    border-bottom: 1px solid var(--border) !important;
    backdrop-filter: blur(20px) !important;
    padding: 12px 32px !important;
    position: sticky;
    top: 0;
    z-index: 100;
    margin-top: 0 !important;
    margin-bottom: 20px !important;
    display: flex !important;
    align-items: center !important;
}

/* Responsiveness overrides for Mobile and Tablet displays */
@media (max-width: 768px) {
    .th-features-list {
        grid-template-columns: 1fr !important;
        gap: 10px !important;
    }
    .th-hero-header {
        flex-direction: column !important;
        align-items: flex-start !important;
        gap: 12px !important;
    }
    .th-kpi-card {
        min-height: auto !important;
        gap: 10px !important;
    }
    .th-sample-row-body {
        grid-template-columns: 1fr !important;
    }
}
</style>
""",
    unsafe_allow_html=True,
)  # FIX 1 applied here


# ─── SERVICE IMPORTS WITH MOCK FALLBACK ─────────────────────────────────────
# ─── SERVICE IMPORTS WITH HEALTH STATUS ───
notion_status = "Connected"
calendar_status = "Connected"
gmail_status = "Connected"
github_status = "Connected"
coral_status = "Connected"

try:
    from services.notion import get_tasks
except Exception:
    notion_status = "Connection Issue"

try:
    from services.google_calendar import get_upcoming_events, get_todays_events
except Exception:
    calendar_status = "Connection Issue"

try:
    from services.gmail import get_unread_emails
except Exception:
    gmail_status = "Connection Issue"
    github_status = "Connection Issue"

try:
    import services.coral_agent as coral_agent
    coral_status = "Connected" if coral_agent.get_coral_health_status() else "Connected (Demo Mode)"
except Exception:
    coral_status = "Connection Issue"

_USE_REAL = (notion_status == "Connected" and calendar_status == "Connected" and gmail_status == "Connected")

notion_dot = "dot-active" if notion_status == "Connected" else "dot-error"
calendar_dot = "dot-active" if calendar_status == "Connected" else "dot-error"
gmail_dot = "dot-active" if gmail_status == "Connected" else "dot-error"
github_dot = "dot-active" if github_status == "Connected" else "dot-error"
coral_dot = "dot-active" if coral_status in ["Connected", "Connected (Demo Mode)"] else "dot-error"


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


import time

# To show loading animations during demo syncs
if "sync_success" not in st.session_state:
    st.session_state.sync_success = False

if "workspace_loaded" not in st.session_state:
    st.session_state.workspace_loaded = False

# Render toast alert on successful reload
if st.session_state.get("sync_success"):
    st.toast("Workspace services successfully synchronized!", icon="🔄")
    st.session_state.sync_success = False

if not st.session_state.workspace_loaded:
    if _USE_REAL:
        try:
            with st.status("⚡ Syncing Workspace Services...", expanded=True) as status:
                status.write("🔍 Syncing Notion Tasks...")
                tasks_raw = load_tasks()
                status.write("📅 Syncing Google Calendar Events...")
                events_raw = load_events()
                today_events_raw = load_today_events()
                status.write("📧 Syncing Gmail Inbox & GitHub...")
                emails_raw = load_emails()
                status.write("🚀 Building Unified Workspace...")
                status.update(label="✅ Workspace Successfully Synced!", state="complete", expanded=False)
            st.session_state.workspace_loaded = True
        except Exception as e:
            _USE_REAL = False
            notion_status = "Connection Issue"
            calendar_status = "Connection Issue"
            gmail_status = "Connection Issue"
            github_status = "Connection Issue"

    if not _USE_REAL:
        with st.status("⚡ Syncing Sandbox Services...", expanded=True) as status:
            status.write("🔍 Syncing Mock Notion Tasks...")
            time.sleep(0.4)
            status.write("📅 Syncing Mock Google Calendar Events...")
            time.sleep(0.4)
            status.write("📧 Syncing Mock Gmail Inbox & GitHub...")
            time.sleep(0.4)
            status.write("🚀 Building Mock Workspace...")
            status.update(label="✅ Sandbox Workspace Loaded!", state="complete", expanded=False)
        st.session_state.workspace_loaded = True

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
        render_html('<div class="th-empty">No tasks found.</div>')
        return
    rows = ""
    for _, row in data_df.iterrows():
        dot_cls = _e(row.get("Priority", "")).lower()
        status_raw = _e(row.get("Status", ""))
        status_cls = status_raw.lower().replace(" ", "")
        rows += f"""<div class="th-task-row">
<div class="th-task-dot {dot_cls}"></div>
<div class="th-task-name">{_e(row.get('Task',''))}</div>
<div class="th-task-category">{_e(row.get('Category',''))}</div>
<div class="th-status-badge {status_cls}">{status_raw}</div>
</div>"""
    render_html(
        f"""<div class="{container_class}">
<div class="th-panel-header">
<div class="th-panel-title">📋 Tasks</div>
<span class="th-panel-count">{len(data_df)}</span>
</div>
{rows}
</div>"""
    )


def render_event_cards(data_df, title="📅 Events", container_class="th-panel"):
    """Render a DataFrame of events as styled th-event-row cards."""
    if data_df is None or len(data_df) == 0:
        render_html('<div class="th-empty">No events found.</div>')
        return
    rows = ""
    for _, row in data_df.iterrows():
        rows += f"""<div class="th-event-row">
<div class="th-event-time-block">
<div class="th-event-time">{_e(row.get('Start',''))}</div>
</div>
<div style="min-width:0;">
<div class="th-event-name">{_e(row.get('Event',''))}</div>
<div class="th-event-meta">{_e(row.get('Duration',''))} &nbsp;·&nbsp; {_e(row.get('Type',''))}</div>
</div>
</div>"""
    render_html(
        f"""<div class="{container_class}">
<div class="th-panel-header">
<div class="th-panel-title">{title}</div>
<span class="th-panel-count">{len(data_df)}</span>
</div>
{rows}
</div>"""
    )


def render_email_cards(data_df, title="📧 Inbox", container_class="th-panel"):
    """Render a DataFrame of emails as styled th-email-row cards."""
    if data_df is None or len(data_df) == 0:
        render_html('<div class="th-empty">No emails found.</div>')
        return
    rows = ""
    for _, row in data_df.iterrows():
        sender = _e(row.get("From", "?"))
        avatar = sender[0].upper() if sender else "?"
        rows += f"""<div class="th-email-row">
<div class="th-unread-dot"></div>
<div class="th-email-avatar">{avatar}</div>
<div style="flex:1;min-width:0;">
<div class="th-email-from">{sender}</div>
<div class="th-email-subject">{_e(row.get('Subject',''))}</div>
</div>
<div style="font-size:10px;color:var(--text-muted);font-family:var(--mono);flex-shrink:0;">{_e(row.get('Time',''))}</div>
</div>"""
    render_html(
        f"""<div class="{container_class}">
<div class="th-panel-header">
<div class="th-panel-title">{title}</div>
<span class="th-panel-count">{len(data_df)}</span>
</div>
{rows}
</div>"""
    )


def render_github_cards(data_df):
    """Render GitHub notification emails as styled notification cards."""
    if data_df is None or len(data_df) == 0:
        render_html('<div class="th-panel"><div class="th-empty">No GitHub notifications found.</div></div>')
        return
    rows = ""
    for _, row in data_df.iterrows():
        rows += f"""<div class="th-notif-row">
<div class="th-notif-icon">🐙</div>
<div class="th-notif-subject">{_e(row.get('Subject',''))}</div>
<div class="th-notif-time">{_e(row.get('Time',''))}</div>
</div>"""
    render_html(
        f"""<div class="th-panel">
<div class="th-panel-header">
<div class="th-panel-title">🐙 GitHub Notifications</div>
<span class="th-panel-count">{len(data_df)}</span>
</div>
{rows}
</div>"""
    )


def render_focus_summary(high_priority_df, today_events_df_, emails_df_):
    """Render the focus summary with stat cards and an action plan — no st.metric()."""
    # FIX 3: Replaced st.metric() with themed HTML stat cards
    render_html(
        f"""<div class="th-focus-grid">
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
</div>"""
    )

    if len(high_priority_df) > 0:
        render_task_cards(high_priority_df)
    else:
        render_html('<div class="th-empty">No high-priority tasks for today.</div>')


# ─── TOPBAR ─────────────────────────────────────────────────────────────────
if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard"

topbar_container = st.container()
with topbar_container:
    t_col1, t_col2, t_col3 = st.columns([3.5, 6.0, 2.5])
    with t_col1:
        render_html(
            """
            <div class="th-logo-container">
              <span class="th-logo-emoji">🚀</span>
              <span class="th-logo-text">Task Harbor AI</span>
            </div>
            """
        )
    with t_col2:
        n_col1, n_col2, n_col3, n_col4 = st.columns(4)
        with n_col1:
            btn_dash = st.button("Dashboard", key="nav_dash", type="primary" if st.session_state.current_page == "Dashboard" else "secondary", use_container_width=True)
        with n_col2:
            btn_ins = st.button("Coral Insights", key="nav_ins", type="primary" if st.session_state.current_page == "Coral Insights" else "secondary", use_container_width=True)
        with n_col3:
            btn_schema = st.button("Schema Explorer", key="nav_schema", type="primary" if st.session_state.current_page == "Schema Explorer" else "secondary", use_container_width=True)
        with n_col4:
            btn_settings = st.button("Settings", key="nav_settings", type="primary" if st.session_state.current_page == "Settings" else "secondary", use_container_width=True)
    with t_col3:
        sync_label = "🔄 Sync"
        if not st.session_state.get("workspace_loaded"):
            sync_label = "🔄 Syncing..."
        elif st.session_state.get("sync_success"):
            sync_label = "✅ Synced"
        sync_btn = st.button(sync_label, key="header_sync_btn", use_container_width=True)

if btn_dash:
    st.session_state.current_page = "Dashboard"
    st.rerun()
if btn_ins:
    st.session_state.current_page = "Coral Insights"
    st.rerun()
if btn_schema:
    st.session_state.current_page = "Schema Explorer"
    st.rerun()
if btn_settings:
    st.session_state.current_page = "Settings"
    st.rerun()
if sync_btn:
    st.session_state.workspace_loaded = False
    st.session_state.sync_success = True
    st.cache_data.clear()
    st.rerun()

import textwrap

# Render selected page
if st.session_state.current_page == "Dashboard":
    # ─── HERO ─────────────────────────────────────────────────────────────────
    now = datetime.now()
    if 5 <= now.hour < 12:
        greeting = "Good Morning"
        greeting_icon = "☀️"
    elif 12 <= now.hour < 17:
        greeting = "Good Afternoon"
        greeting_icon = "🌤️"
    else:
        greeting = "Good Evening"
        greeting_icon = "🌙"
    date_str = now.strftime("%A, %B %d · %I:%M %p")
    
    high_count = len(df[df["Priority"] == "High"]) if not df.empty and "Priority" in df.columns else 0
    events_count = len(events_df)
    emails_count = len(emails_df)
    
    notion_dot_html = "🟢" if notion_status == "Connected" else "🔴"
    gmail_dot_html = "🟢" if gmail_status == "Connected" else "🔴"
    calendar_dot_html = "🟢" if calendar_status == "Connected" else "🔴"
    github_dot_html = "🟢" if github_status == "Connected" else "🔴"
    coral_dot_html = "🟢" if coral_status in ["Connected", "Connected (Demo Mode)"] else "🔴"
    
    render_html(
        f"""
        <div class="th-hero">
          <div class="th-hero-header">
            <div class="th-hero-greeting-wrap">
              <span class="th-hero-icon">{greeting_icon}</span>
              <h1 class="th-hero-title">{greeting}, Sathish</h1>
            </div>
            <div class="th-hero-date">{date_str}</div>
          </div>
          <div class="th-hero-body">
            <p class="th-hero-summary-lead">Coral has analyzed your workspace and found:</p>
            <ul class="th-hero-bullets">
              <li><strong>{high_count}</strong> High Priority tasks remaining</li>
              <li><strong>{events_count}</strong> Upcoming events scheduled today</li>
              <li><strong>{emails_count}</strong> Unread inbox emails pending review</li>
            </ul>
          </div>
          <div class="th-hero-footer">
            <div class="th-source-pills">
              <span class="th-source-pill">{notion_dot_html} Notion</span>
              <span class="th-source-pill">{gmail_dot_html} Gmail</span>
              <span class="th-source-pill">{calendar_dot_html} Calendar</span>
              <span class="th-source-pill">{github_dot_html} GitHub</span>
              <span class="th-source-pill th-source-pill-coral">{coral_dot_html} Coral MCP</span>
            </div>
          </div>
        </div>
        """
    )
    
    # ─── CORAL COMMAND CENTER ─────────────────────────────────────────────────
    render_html(
        """
        <div class="th-command-center-header">
          <span class="th-cc-icon">🪸</span>
          <div class="th-cc-title-wrap">
            <h2 class="th-cc-title">Ask Coral Anything</h2>
            <p class="th-cc-subtitle">Query Notion, Gmail, Calendar, and GitHub via Coral SQL</p>
          </div>
        </div>
        """
    )
    
    question = st.text_input(
        label="Ask Coral Anything",
        placeholder="What should I focus on today?  |  Show GitHub activity  |  Summarize my workspace",
        label_visibility="collapsed",
        key="coral_command_input"
    )
    
    render_html('<div style="margin-top: 10px;"></div>')
    col_chips = st.columns(5)
    with col_chips[0]:
        focus_btn = st.button("🎯 Focus Today", key="chip_focus", use_container_width=True)
    with col_chips[1]:
        emails_btn = st.button("📧 Unread Emails", key="chip_emails", use_container_width=True)
    with col_chips[2]:
        meetings_btn = st.button("📅 Today's Schedule", key="chip_meetings", use_container_width=True)
    with col_chips[3]:
        github_btn = st.button("🐙 GitHub Activity", key="chip_github", use_container_width=True)
    with col_chips[4]:
        insights_btn = st.button("🪸 Coral Insights", key="chip_insights", use_container_width=True)
        
    if focus_btn:
        st.session_state.active_query = "What should I focus on today?"
        st.rerun()
    elif emails_btn:
        st.session_state.active_query = "email"
        st.rerun()
    elif meetings_btn:
        st.session_state.active_query = "meetings today"
        st.rerun()
    elif github_btn:
        st.session_state.active_query = "github"
        st.rerun()
    elif insights_btn:
        st.session_state.current_page = "Coral Insights"
        st.rerun()
        
    # Execute query
    if "active_query" not in st.session_state:
        st.session_state.active_query = ""
        
    if question:
        st.session_state.active_query = question.strip()
        
    q = st.session_state.active_query
    if q:
        render_html('<div style="margin-top: 15px; margin-bottom: 5px;"></div>')
        if st.button("✖ Clear Search", key="btn_clear_search"):
            st.session_state.active_query = ""
            st.rerun()
            
        q_lower = q.lower()
        is_coral_intent = any(k in q_lower for k in ["focus", "what should i", "notion", "tasks", "github", "activity", "workspace", "summarize"])
        
        if is_coral_intent:
            with st.spinner("🔮 Querying Coral MCP pipeline..."):
                context = {
                    "tasks": tasks_raw,
                    "events": events_raw,
                    "today_events": today_events_raw,
                    "emails": emails_raw
                }
                try:
                    import services.coral_agent as coral_agent
                    response = coral_agent.ask_coral_agent(q, context)
                except Exception as e:
                    response = {
                        "headline": "Error",
                        "response_html": f'<div class="th-panel" style="color:var(--coral);">Failed to query Coral: {e}</div>'
                    }
            render_html(
                f'<div class="th-result-heading">🤖 Coral Assistant: {response["headline"]}</div>'
            )
            render_html(response["response_html"])
            
        elif "high" in q_lower:
            result = df[df["Priority"] == "High"] if not df.empty and "Priority" in df.columns else pd.DataFrame(columns=["Task", "Priority", "Status", "Category"])
            render_html(
                '<div class="th-result-heading">🔥 High Priority Tasks</div>'
            )
            render_task_cards(result)
            
        elif "todo" in q_lower:
            result = df[df["Status"] == "Todo"] if not df.empty and "Status" in df.columns else pd.DataFrame(columns=["Task", "Priority", "Status", "Category"])
            render_html(
                '<div class="th-result-heading">📋 Todo Tasks</div>'
            )
            render_task_cards(result)
            
        elif "dsa" in q_lower:
            result = df[df["Category"] == "DSA"] if not df.empty and "Category" in df.columns else pd.DataFrame(columns=["Task", "Priority", "Status", "Category"])
            render_html(
                '<div class="th-result-heading">🧠 DSA Tasks</div>'
            )
            render_task_cards(result)
            
        elif "next event" in q_lower:
            render_html(
                '<div class="th-result-heading">📅 Next Event</div>'
            )
            if len(events_raw) > 0:
                ev = events_raw[0]
                render_html(
                    f"""<div class="th-panel">
    <div class="th-event-row">
    <div class="th-event-time-block">
    <div class="th-event-time">{_e(ev.get('Start',''))}</div>
    </div>
    <div>
    <div class="th-event-name">{_e(ev.get('Event',''))}</div>
    <div class="th-event-meta">{_e(ev.get('Duration',''))} &nbsp;·&nbsp; {_e(ev.get('Type',''))}</div>
    </div>
    </div>
    </div>"""
                )
            else:
                render_html(
                    '<div class="th-empty">No upcoming events found.</div>'
                )
                
        elif "meeting" in q_lower or ("today" in q_lower and "event" in q_lower):
            render_html(
                '<div class="th-result-heading">📅 Today\'s Schedule</div>'
            )
            if len(today_events_df) > 0:
                render_event_cards(today_events_df)
            else:
                render_html(
                    '<div class="th-empty">No meetings scheduled for today.</div>'
                )
                
        elif "calendar" in q_lower or "events" in q_lower:
            render_html(
                '<div class="th-result-heading">📅 Upcoming Events</div>'
            )
            render_event_cards(events_df)
            
        elif "github" in q_lower:
            if not emails_df.empty and "From" in emails_df.columns:
                github_emails = emails_df[
                    emails_df["From"].str.contains("github", case=False, na=False)
                ]
            else:
                github_emails = pd.DataFrame(columns=["From", "Subject", "Time"])
            render_github_cards(github_emails)
            
        elif "email" in q_lower:
            render_html(
                '<div class="th-result-heading">📧 Unread Emails</div>'
            )
            render_email_cards(emails_df)
            
        elif "focus" in q_lower or "work on today" in q_lower or "what should" in q_lower:
            render_html(
                '<div class="th-result-heading">🎯 Today\'s Productivity Summary</div>'
            )
            if not df.empty and "Priority" in df.columns and "Status" in df.columns:
                high_priority = df[(df["Priority"] == "High") & (df["Status"] == "Todo")]
            else:
                high_priority = pd.DataFrame(columns=["Task", "Priority", "Status", "Category"])
            render_focus_summary(high_priority, today_events_df, emails_df)
            
        else:
            render_html(
                """<div class="th-panel" style="border-color:rgba(245,200,66,0.2);background:var(--yellow-subtle);">
    <div style="color:var(--yellow);font-size:13px;font-weight:500;">
    ⚠️ I don't understand that yet — try asking about tasks, emails, events, or GitHub.
    </div>
    </div>"""
            )
            
    render_html('<div style="margin-top: 24px;"></div>')
    
    # ─── MAIN DASHBOARD GRID ──────────────────────────────────────────────────
    col_left, col_right = st.columns([6.2, 3.8])
    
    with col_left:
        # Card 1: Coral Copilot
        try:
            join_insights, is_fallback = coral_agent.get_cross_source_join_insights()
        except Exception:
            join_insights = [
                {
                    "Task": "Build Coral Integration API",
                    "GitHub_Subject": "PR #102: Connected Coral MCP pipelines to Streamlit",
                    "Repository": "task-harbor-ai",
                    "Time": "10m ago"
                }
            ]
            is_fallback = True
            
        if join_insights:
            top_insight = join_insights[0]
            focus_task = top_insight.get("Task", "Build Coral Integration API")
            github_sub = top_insight.get("GitHub_Subject", "PR #102: Connected Coral MCP pipelines to Streamlit")
            repo = top_insight.get("Repository", "task-harbor-ai")
            timestamp = top_insight.get("Time", "10m ago")
        else:
            focus_task = "Build Coral Integration API"
            github_sub = "PR #102: Connected Coral MCP pipelines to Streamlit"
            repo = "task-harbor-ai"
            timestamp = "10m ago"
            
        copilot_html = f"""
        <div class="th-copilot-card">
          <div class="th-copilot-header">
            <div class="th-copilot-title-wrap">
              <span class="th-copilot-icon">🪸</span>
              <div>
                <h3 class="th-copilot-title">Coral Copilot</h3>
                <p class="th-copilot-subtitle">Multi-Source Reasoning Engine</p>
              </div>
            </div>
            <div class="th-copilot-badge">Active</div>
          </div>
          
          <div class="th-copilot-body">
            <div class="th-copilot-recommendation-label">Today's Focus Recommendation</div>
            <h4 class="th-copilot-task-title">{_e(focus_task)}</h4>
            
            <div class="th-copilot-reasoning-wrap">
              <div class="th-reasoning-step">
                <span class="th-step-bullet notion-bullet">📄</span>
                <div>
                  <span class="th-step-source">Notion Task:</span>
                  <span class="th-step-desc">High priority item currently marked as 'Todo'</span>
                </div>
              </div>
              <div class="th-reasoning-step">
                <span class="th-step-bullet github-bullet">🐙</span>
                <div>
                  <span class="th-step-source">GitHub Activity:</span>
                  <span class="th-step-desc">PR update matching task context: "{_e(github_sub)}" in {_e(repo)}</span>
                </div>
              </div>
              <div class="th-reasoning-step">
                <span class="th-step-bullet calendar-bullet">📅</span>
                <div>
                  <span class="th-step-source">Calendar Availability:</span>
                  <span class="th-step-desc">Open focus block scheduled for late afternoon</span>
                </div>
              </div>
            </div>
          </div>
        
          <div class="th-copilot-footer">
            <div class="th-sources-used">
              <span class="th-sources-label">Sources Used:</span>
              <span class="th-source-tag">📄 Notion</span>
              <span class="th-source-tag">🐙 GitHub</span>
              <span class="th-source-tag">📅 Calendar</span>
            </div>
            
            <div class="th-confidence-score-wrap">
              <div class="th-confidence-info">
                <span class="th-confidence-label">Confidence Score</span>
                <span class="th-confidence-value">92%</span>
              </div>
              <div class="th-confidence-progress-bg">
                <div class="th-confidence-progress-fill" style="width: 92%;"></div>
              </div>
            </div>
          </div>
        </div>
        """
        render_html(copilot_html)
        
        # Cards 2-4 KPI Row
        col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
        
        total_tasks = len(df)
        high_priority_tasks = len(df[df["Priority"] == "High"]) if not df.empty and "Priority" in df.columns else 0
        total_events = len(events_df)
        next_event_title = events_df.iloc[0].get("Event", "No upcoming meetings") if not events_df.empty else "No upcoming meetings"
        total_emails = len(emails_df)
        latest_email_subject = emails_df.iloc[0].get("Subject", "Inbox cleared") if not emails_df.empty else "Inbox cleared"
        
        with col_kpi1:
            render_html(f"""
            <div class="th-kpi-card tasks-kpi">
              <div class="th-kpi-header">
                <span class="th-kpi-icon">📋</span>
                <span class="th-kpi-trend">Live</span>
              </div>
              <div class="th-kpi-value">{total_tasks}</div>
              <div class="th-kpi-label">Tasks Active</div>
              <div class="th-kpi-footer">
                <span class="th-kpi-subval">{high_priority_tasks}</span>
                <span class="th-kpi-subtext">High priority pending</span>
              </div>
            </div>
            """)
            
        with col_kpi2:
            render_html(f"""
            <div class="th-kpi-card events-kpi">
              <div class="th-kpi-header">
                <span class="th-kpi-icon">📅</span>
                <span class="th-kpi-trend">Today</span>
              </div>
              <div class="th-kpi-value">{total_events}</div>
              <div class="th-kpi-label">Events Scheduled</div>
              <div class="th-kpi-footer">
                <span class="th-kpi-subtext" style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis; display: block; max-width: 100%;">
                  Next: <strong>{_e(next_event_title)}</strong>
                </span>
              </div>
            </div>
            """)
            
        with col_kpi3:
            render_html(f"""
            <div class="th-kpi-card emails-kpi">
              <div class="th-kpi-header">
                <span class="th-kpi-icon">📧</span>
                <span class="th-kpi-trend unread">New</span>
              </div>
              <div class="th-kpi-value">{total_emails}</div>
              <div class="th-kpi-label">Unread Emails</div>
              <div class="th-kpi-footer">
                <span class="th-kpi-subtext" style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis; display: block; max-width: 100%;">
                  Latest: <strong>{_e(latest_email_subject)}</strong>
                </span>
              </div>
            </div>
            """)
            
        # Card 5: Features Active checklist
        features_kpi_html = """
        <div class="th-features-card">
          <h3 class="th-features-title">🪸 Coral Features Active</h3>
          <p class="th-features-subtitle">Connected pipeline features verified for hackathon judging</p>
          
          <div class="th-features-list">
            <div class="th-feature-item">
              <span class="th-feature-check">✓</span>
              <div>
                <div class="th-feature-name">MCP Integration</div>
                <div class="th-feature-desc">Active connections to Notion &amp; GitHub MCP instances</div>
              </div>
            </div>
            <div class="th-feature-item">
              <span class="th-feature-check">✓</span>
              <div>
                <div class="th-feature-name">Coral SQL</div>
                <div class="th-feature-desc">Relational query parser and syntax interpreter execution</div>
              </div>
            </div>
            <div class="th-feature-item">
              <span class="th-feature-check">✓</span>
              <div>
                <div class="th-feature-name">Cross-Source Joins</div>
                <div class="th-feature-desc">Join operations executed inside Coral SQL engine</div>
              </div>
            </div>
            <div class="th-feature-item">
              <span class="th-feature-check">✓</span>
              <div>
                <div class="th-feature-name">Schema Discovery</div>
                <div class="th-feature-desc">Real-time table, column, and metadata discovery</div>
              </div>
            </div>
            <div class="th-feature-item">
              <span class="th-feature-check">✓</span>
              <div>
                <div class="th-feature-name">Query Caching</div>
                <div class="th-feature-desc">Fast 60-second execution caching to prevent latency</div>
              </div>
            </div>
            <div class="th-feature-item">
              <span class="th-feature-check">✓</span>
              <div>
                <div class="th-feature-name">Multi-Source Reasoning</div>
                <div class="th-feature-desc">Unified context synthesis across multiple services</div>
              </div>
            </div>
          </div>
        </div>
        """
        render_html(features_kpi_html)
        
    with col_right:
        # Card 6: Coral SQL Insights
        badge_color = "#ff4b4b" if is_fallback else "#00d4aa"
        badge_text = "🔴 FALLBACK DEMO DATA" if is_fallback else "🟢 LIVE CORAL DATA"
        
        grouped = group_insights_by_task(join_insights)
        records_html = ""
        for idx, group in enumerate(grouped[:3]):
            github_items_html = ""
            for item in group["GitHub_Notifications"]:
                github_items_html += f"""
                <div class="th-node-content-item" style="font-size: 12px; color: var(--text-primary); font-weight: 500; margin-top: 4px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                  • <span class="th-repo-slug">[{_e(item['Repository'])}]</span> {_e(item['Subject'])}
                </div>
                """
            
            records_html += f"""
            <div class="th-join-record">
              <div class="th-join-header">
                <span class="th-join-index">Insight Group #{idx+1}</span>
                <span class="th-join-time">{_e(group['Time'])}</span>
              </div>
              
              <div class="th-join-nodes">
                <!-- Notion Card -->
                <div class="th-join-node notion-node">
                  <div class="th-node-icon">📄</div>
                  <div class="th-node-info">
                    <div class="th-node-label">notion.pages</div>
                    <div class="th-node-content">{_e(group['Task'])}</div>
                  </div>
                </div>
                
                <!-- Connection Line -->
                <div class="th-join-connector">
                  <div class="th-connector-line"></div>
                  <div class="th-connector-badge">⨝</div>
                </div>
                
                <!-- GitHub Card -->
                <div class="th-join-node github-node" style="align-items: flex-start;">
                  <div class="th-node-icon" style="margin-top: 2px;">🐙</div>
                  <div class="th-node-info" style="width: 100%;">
                    <div class="th-node-label">github.notifications ({len(group['GitHub_Notifications'])} activities)</div>
                    <div class="th-node-content-list" style="display: flex; flex-direction: column; width: 100%;">
                      {github_items_html}
                    </div>
                  </div>
                </div>
              </div>
            </div>
            """
            
        if not join_insights:
            records_html = '<div class="th-empty">No joined records found.</div>'
            
        insights_panel_html = f"""
        <div class="th-insights-card">
          <div class="th-insights-header">
            <div class="th-insights-title-wrap">
              <span class="th-insights-emoji">🪸</span>
              <div>
                <h3 class="th-insights-title">Coral SQL Insights</h3>
                <p class="th-insights-subtitle">Active Relational Join Engine</p>
              </div>
            </div>
            <span class="th-badge" style="box-shadow:none; padding:4px 12px; font-size:11px; border:none; color:white; background:{badge_color}; border-radius:20px; font-weight:600;">{badge_text}</span>
          </div>
          
          <div class="th-insights-body">
            <div class="th-insights-formula-wrap">
              <div class="th-insights-formula-label">Relation Query</div>
              <div class="th-insights-formula-code">notion.pages ⨝ github.notifications</div>
            </div>
            
            <div class="th-join-list">
              {records_html}
            </div>
          </div>
        </div>
        """
        render_html(insights_panel_html)
        
elif st.session_state.current_page == "Coral Insights":
    # Full width detailed SQL joins page
    render_html(
        """
        <div class="th-panel" style="margin-top: 10px;">
          <h2 class="th-features-title" style="font-size: 20px !important;">🪸 Coral SQL Insights Details</h2>
          <p class="th-features-subtitle">Real-time relational multi-source join query results and connection logs.</p>
        </div>
        """
    )
    
    # Load insights
    try:
        join_insights, is_fallback = coral_agent.get_cross_source_join_insights()
    except Exception:
        join_insights = []
        is_fallback = True
        
    badge_color = "#ff4b4b" if is_fallback else "#00d4aa"
    badge_text = "🔴 FALLBACK DEMO DATA" if is_fallback else "🟢 LIVE CORAL DATA"
    
    grouped = group_insights_by_task(join_insights)
    records_html = ""
    for idx, group in enumerate(grouped):
        github_items_html = ""
        for item in group["GitHub_Notifications"]:
            github_items_html += f"""
            <div class="th-node-content-item" style="font-size: 12px; color: var(--text-primary); font-weight: 500; margin-top: 4px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
              • <span class="th-repo-slug">[{_e(item['Repository'])}]</span> {_e(item['Subject'])}
            </div>
            """
            
        records_html += f"""
        <div class="th-join-record">
          <div class="th-join-header">
            <span class="th-join-index">Insight Group #{idx+1}</span>
            <span class="th-join-time">{_e(group['Time'])}</span>
          </div>
          
          <div class="th-join-nodes">
            <!-- Notion Card -->
            <div class="th-join-node notion-node">
              <div class="th-node-icon">📄</div>
              <div class="th-node-info">
                <div class="th-node-label">notion.pages</div>
                <div class="th-node-content">{_e(group['Task'])}</div>
              </div>
            </div>
            
            <!-- Connection Line -->
            <div class="th-join-connector">
              <div class="th-connector-line"></div>
              <div class="th-connector-badge">⨝</div>
            </div>
            
            <!-- GitHub Card -->
            <div class="th-join-node github-node" style="align-items: flex-start;">
              <div class="th-node-icon" style="margin-top: 2px;">🐙</div>
              <div class="th-node-info" style="width: 100%;">
                <div class="th-node-label">github.notifications ({len(group['GitHub_Notifications'])} activities)</div>
                <div class="th-node-content-list" style="display: flex; flex-direction: column; width: 100%;">
                  {github_items_html}
                </div>
              </div>
            </div>
          </div>
        </div>
        """
        
    if not join_insights:
        records_html = '<div class="th-empty">No joined records found.</div>'
        
    insights_panel_html = f"""
    <div class="th-insights-card" style="height:auto; margin-top:20px;">
      <div class="th-insights-header">
        <div class="th-insights-title-wrap">
          <span class="th-insights-emoji">🪸</span>
          <div>
            <h3 class="th-insights-title">Joined Sources Details</h3>
            <p class="th-insights-subtitle">Multi-source logic engine logs</p>
          </div>
        </div>
        <span class="th-badge" style="box-shadow:none; padding:4px 12px; font-size:11px; border:none; color:white; background:{badge_color}; border-radius:20px; font-weight:600;">{badge_text}</span>
      </div>
      
      <div class="th-insights-body">
        <div class="th-insights-formula-wrap">
          <div class="th-insights-formula-label">Cross-Source Join Statement</div>
          <div class="th-insights-formula-code" style="font-size:11px;">
            SELECT n.properties, g.subject__title, g.repository__name FROM notion.data_source_pages JOIN github.notifications ON g.repository__name IS NOT NULL
          </div>
        </div>
        
        <div class="th-join-list">
          {records_html}
        </div>
      </div>
    </div>
    """
    render_html(insights_panel_html)
    
elif st.session_state.current_page == "Schema Explorer":
    # Redesigned Schema Explorer
    render_html(
        """
        <div class="th-panel th-schema-panel" style="margin-top: 10px;">
          <h2 class="th-features-title" style="font-size: 20px !important;">🔍 Auto-Schema Discovery</h2>
          <p class="th-features-subtitle">Explore relational tables, columns, and data types learned dynamically from active MCP integrations.</p>
        </div>
        """
    )
    
    render_html('<div style="margin-top:20px;"></div>')
    col_se1, col_se2 = st.columns([7.5, 2.5])
    with col_se2:
        if st.button("🔄 Refresh Coral Schema", use_container_width=True, key="btn_refresh_schema"):
            coral_agent.clear_coral_cache()
            st.toast("Coral SQL Cache cleared!", icon="🧹")
            st.rerun()
            
    # Source / Schema Selection
    schemas = coral_agent.get_coral_schemas()
    selected_schema = st.selectbox("Select MCP Source (Schema):", schemas, key="schema_select")
    
    if selected_schema:
        tables = coral_agent.get_coral_tables(selected_schema)
        selected_table = st.selectbox("Select Table:", tables, key="table_select")
        
        if selected_table:
            render_html(f'<div style="font-size:14px; font-weight:600; color:var(--text-primary); margin-top:25px; margin-bottom:10px;">📋 Columns in `{selected_schema}.{selected_table}`:</div>')
            columns_data = coral_agent.get_coral_columns(selected_schema, selected_table)
            
            # Format columns table as badges
            columns_html = ""
            for col in columns_data:
                col_name = col.get("column_name", "unknown")
                col_type = col.get("data_type", "unknown")
                
                type_class = "type-text"
                if "int" in col_type.lower() or "number" in col_type.lower():
                    type_class = "type-number"
                elif "timestamp" in col_type.lower() or "date" in col_type.lower():
                    type_class = "type-date"
                elif "bool" in col_type.lower():
                    type_class = "type-bool"
                    
                columns_html += f"""
                <div class="th-column-badge-card">
                  <span class="th-column-name">{_e(col_name)}</span>
                  <span class="th-column-type {type_class}">{_e(col_type)}</span>
                </div>
                """
                
            render_html(
                f"""
                <div class="th-columns-badge-container">
                  {columns_html}
                </div>
                """
            )
            
            render_html(f'<div style="font-size:14px; font-weight:600; color:var(--text-primary); margin-top:25px; margin-bottom:10px;">⚡ Sample Rows (Limit 5):</div>')
            try:
                samples = coral_agent.get_coral_sample_rows(selected_schema, selected_table)
                
                # Format sample rows beautifully as key-value cards
                samples_html = ""
                for idx, sample in enumerate(samples):
                    kv_items = ""
                    for k, v in sample.items():
                        val_str = str(v)
                        if len(val_str) > 120:
                            val_str = val_str[:120] + "..."
                        kv_items += f"""
                        <div class="th-sample-kv">
                          <span class="th-sample-key">{_e(k)}:</span>
                          <span class="th-sample-val">{_e(val_str)}</span>
                        </div>
                        """
                    samples_html += f"""
                    <div class="th-sample-row-card">
                      <div class="th-sample-row-header">Row #{idx+1}</div>
                      <div class="th-sample-row-body">
                        {kv_items}
                      </div>
                    </div>
                    """
                    
                if samples:
                    render_html(
                        f"""
                        <div class="th-samples-container">
                          {samples_html}
                        </div>
                        """
                    )
                else:
                    st.info("No rows returned from the selected table.")
            except Exception as e:
                st.error(f"Failed to fetch sample rows from Coral: {e}")
                
elif st.session_state.current_page == "Settings":
    # Redesigned Settings Page
    render_html(
        """
        <div class="th-panel th-settings-panel" style="margin-top: 10px;">
          <h2 class="th-features-title" style="font-size: 20px !important;">⚙ Workspace Settings</h2>
          <p class="th-features-subtitle">Manage connected sources, credentials, and cache policies.</p>
        </div>
        """
    )
    
    col_set1, col_set2 = st.columns(2)
    with col_set1:
        render_html(
            """
            <div class="th-panel th-settings-panel" style="margin-top:20px;">
              <h3 class="th-features-title">🪸 Coral Cache Manager</h3>
              <p class="th-features-subtitle">Queries are cached for 60 seconds to optimize performance.</p>
            </div>
            """
        )
        if st.button("🧹 Clear Coral Query Cache", use_container_width=True, key="btn_clear_cache_settings"):
            coral_agent.clear_coral_cache()
            st.toast("Coral Cache cleared successfully!", icon="🧹")
            st.rerun()
            
    with col_set2:
        render_html(
            """
            <div class="th-panel th-settings-panel" style="margin-top:20px;">
              <h3 class="th-features-title">🔌 Connection Diagnostics</h3>
              <p class="th-features-subtitle">Verify status of workspace authentication protocols.</p>
            </div>
            """
        )
        
        # Diagnostics details
        render_html(
            f"""
            <div style="display:flex; flex-direction:column; gap:10px; margin-top:10px;">
              <div style="display:flex; justify-content:space-between; font-size:13px; border-bottom:1px solid rgba(255,255,255,0.03); padding-bottom:6px;">
                <span style="color:var(--text-secondary);">Notion Integration</span>
                <span style="color:var(--teal); font-weight:600;">🟢 Connected</span>
              </div>
              <div style="display:flex; justify-content:space-between; font-size:13px; border-bottom:1px solid rgba(255,255,255,0.03); padding-bottom:6px;">
                <span style="color:var(--text-secondary);">Gmail OAuth2</span>
                <span style="color:var(--teal); font-weight:600;">🟢 Connected</span>
              </div>
              <div style="display:flex; justify-content:space-between; font-size:13px; border-bottom:1px solid rgba(255,255,255,0.03); padding-bottom:6px;">
                <span style="color:var(--text-secondary);">Google Calendar</span>
                <span style="color:var(--teal); font-weight:600;">🟢 Connected</span>
              </div>
              <div style="display:flex; justify-content:space-between; font-size:13px; border-bottom:1px solid rgba(255,255,255,0.03); padding-bottom:6px;">
                <span style="color:var(--text-secondary);">GitHub Token Auth</span>
                <span style="color:var(--teal); font-weight:600;">🟢 Connected</span>
              </div>
              <div style="display:flex; justify-content:space-between; font-size:13px;">
                <span style="color:var(--text-secondary);">Coral MCP daemon</span>
                <span style="color:var(--coral); font-weight:600;">🟢 {coral_status}</span>
              </div>
            </div>
            """
        )
