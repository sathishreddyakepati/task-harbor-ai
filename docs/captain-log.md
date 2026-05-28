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
# Captain's Log – Day 4

## Problem Statement

Managing tasks, schedules, and important communications across different platforms creates context switching and reduces productivity.

## Solution

Task Harbor AI aims to unify productivity workflows by bringing together tasks, calendar events, and email updates into a single dashboard with intelligent recommendations.

## What We Built Today

* Integrated Google Calendar API
* Integrated Gmail API
* Added GitHub email notification filtering
* Built an AI Recommendation Engine
* Improved dashboard functionality
* Pushed Day 4 updates to GitHub

## Challenges

* Coral Notion source installation completed successfully
* Coral can access Notion metadata tables
* Encountered authentication issues while testing Notion search queries
* Currently investigating connector permissions and configuration

## Next Steps

* Improve dashboard UI and user experience
* Add smarter recommendation logic
* Record project demo video
* Finalize documentation and submission assets
* Continue Coral integration exploration

## Status

Day 4 Complete ✅

* Notion Integration
* Google Calendar Integration
* Gmail Integration
* AI Recommendations
* Coral Setup

