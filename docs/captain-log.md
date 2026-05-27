# 🚀 Task Harbor AI - Captain's Log

## Project Overview

Task Harbor AI is an AI-powered productivity assistant that aims to bring together data from Notion, Google Calendar, and Gmail into a single workspace.

Users can ask natural language questions such as:

- What are my todo tasks?
- What are my high priority tasks?
- What meetings do I have today?
- What should I work on today?

---

# Day 3 - May 27, 2026

## Goals

- Start fresh with a clean codebase
- Connect Notion database
- Fetch real task data
- Build initial Streamlit UI
- Add natural language task queries

---

## Completed

### Project Setup

- Created fresh repository
- Initialized Git
- Set up Python virtual environment
- Installed Streamlit

### Notion Integration

- Created Notion integration
- Connected integration to database
- Retrieved database metadata
- Accessed task data through Notion API

### Streamlit UI

Built first interface with:

- Task display
- Question input
- Filtered task responses

### Natural Language Queries

Implemented:

- What are my todo tasks?
- What are my high priority tasks?
- Show my DSA tasks

---

## Challenges Faced

### Challenge 1

Issue:

DatabasesEndpoint object has no attribute query

Cause:

Latest Notion SDK version changed API behavior.

Solution:

Used:

data_sources.query()

instead of:

databases.query()

---

### Challenge 2

Issue:

ImportError involving calendar module

Cause:

Created:

services/calendar.py

which conflicted with Python's built-in calendar module.

Solution:

Renamed file to:

services/google_calendar.py

---

## Learnings

- Notion API fundamentals
- Notion SDK v3 changes
- Streamlit basics
- Environment variable management
- Debugging third-party APIs

---

## End of Day Status

Completed:

✅ Notion Integration
✅ Streamlit Interface
✅ Natural Language Queries
✅ GitHub Repository
✅ LinkedIn Update
✅ Discord Showcase

Upcoming:

📅 Google Calendar Integration
📧 Gmail Integration
🪸 Coral Integration
🎯 Smart Recommendations

---

## Screenshots

(Add screenshots here later)
