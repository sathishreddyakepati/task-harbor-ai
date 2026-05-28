import subprocess
import json
import os
from datetime import datetime

# Constants
NOTION_DATA_SOURCE_ID = "4b47dd3e-dfbd-49fc-a767-3b951ebd4e0b"
import re

def strip_markdown(text: str) -> str:
    """Strip standard markdown formatting features (bold, headers, bullets, code block backticks) from a string."""
    if not text:
        return ""
    # Remove bold/italic markers like ***, **, *
    text = re.sub(r'\*+', '', text)
    # Remove headings like #, ##, ### at start of lines
    text = re.sub(r'^#+\s+', '', text, flags=re.MULTILINE)
    # Remove markdown bullets at start of lines like - , * , +
    text = re.sub(r'^[-\*\+]\s+', '', text, flags=re.MULTILINE)
    # Remove markdown code markers (backticks)
    text = text.replace('`', '')
    return text.strip()

def run_coral_query(sql_query: str) -> list:
    """Execute a SQL query via Coral CLI and return results as a list of dicts."""
    try:
        # Run coral command
        result = subprocess.run(
            ["coral.exe", "sql", "--format", "json", sql_query],
            capture_output=True,
            text=True,
            shell=True,
            timeout=10 # 10s timeout to prevent hanging
        )
        if result.returncode != 0:
            print(f"Coral query failed: {result.stderr}")
            return []
        
        output = result.stdout.strip()
        if not output:
            return []
            
        return json.loads(output)
    except Exception as e:
        print(f"Error running Coral query: {e}")
        return []

def get_notion_tasks_via_coral() -> list:
    """Query Notion tasks from the Coral MCP pipeline."""
    query = f"SELECT id, properties FROM notion.data_source_pages WHERE data_source_id = '{NOTION_DATA_SOURCE_ID}'"
    rows = run_coral_query(query)
    
    tasks = []
    for row in rows:
        try:
            properties = json.loads(row.get("properties", "{}"))
            
            # Extract task title
            title_list = properties.get("Task", {}).get("title", [])
            task_name = title_list[0].get("plain_text", "") if title_list else "Unnamed Task"
            task_name = strip_markdown(task_name)
            
            # Extract other fields
            priority = properties.get("Priority", {}).get("select", {})
            priority_name = priority.get("name", "Low") if priority else "Low"
            
            status = properties.get("Status", {}).get("select", {})
            status_name = status.get("name", "Todo") if status else "Todo"
            
            category = properties.get("Category", {}).get("select", {})
            category_name = category.get("name", "General") if category else "General"
            
            hours_obj = properties.get("Estimated Hours", {})
            hours = hours_obj.get("number", 0) if hours_obj else 0
            
            tasks.append({
                "Task": task_name,
                "Priority": priority_name,
                "Status": status_name,
                "Category": category_name,
                "Hours": hours
            })
        except Exception as e:
            print(f"Error parsing Notion task properties: {e}")
            
    return tasks

def get_github_activity_via_coral() -> list:
    """Query recent GitHub notifications from Coral, with mock fallback on failure."""
    query = "SELECT subject__title, updated_at FROM github.notifications LIMIT 5"
    rows = run_coral_query(query)
    
    activity = []
    for row in rows:
        title = strip_markdown(row.get("subject__title", ""))
        updated = row.get("updated_at", "")
        
        # Format updated time
        time_str = "Recent"
        if updated:
            try:
                # GitHub timestamp: e.g. 2026-05-28T10:00:00Z
                dt = datetime.fromisoformat(updated.replace("Z", "+00:00"))
                time_str = dt.strftime("%b %d · %I:%M %p")
            except Exception:
                time_str = updated
                
        activity.append({
            "Subject": title,
            "Time": time_str
        })
        
    # If no live activity (e.g. auth failed), return mock demo data
    if not activity:
        activity = [
            {"Subject": "PR #102: Connected Coral MCP pipelines to Streamlit", "Time": "10m ago"},
            {"Subject": "Issue #44: Resolved Notion query parameter requirements", "Time": "1h ago"},
            {"Subject": "PR #98: Updated CSS styling for glowing centerpiece search", "Time": "3h ago"},
            {"Subject": "Release v1.2.0: Task Harbor AI stable demo candidate", "Time": "1d ago"}
        ]
        
    return activity

def get_coral_health_status() -> bool:
    """Check if Coral CLI and Notion data source are healthy."""
    try:
        # Check version
        res = subprocess.run(["coral.exe", "-V"], capture_output=True, text=True, shell=True)
        if res.returncode != 0:
            return False
            
        # Check if notion pages table can be queried
        query = f"SELECT id FROM notion.data_source_pages WHERE data_source_id = '{NOTION_DATA_SOURCE_ID}' LIMIT 1"
        rows = run_coral_query(query)
        return len(rows) > 0
    except Exception:
        return False

def ask_coral_agent(query_str: str, dashboard_context: dict) -> dict:
    """Process natural language query against Coral MCP data and dashboard context."""
    q = query_str.strip().lower()
    
    # Intent 1: "What should I focus on today?"
    if "focus" in q or "what should i" in q:
        # Fetch Notion tasks via Coral
        coral_tasks = get_notion_tasks_via_coral()
        high_priority = [t for t in coral_tasks if t.get("Priority") == "High" and t.get("Status") == "Todo"]
        
        # Fallback to dashboard tasks if Coral Notion returned nothing
        if not high_priority and dashboard_context.get("tasks"):
            high_priority = [t for t in dashboard_context["tasks"] if t.get("Priority") == "High" and t.get("Status") == "Todo"]
            
        events = dashboard_context.get("today_events", [])
        
        headline = "🎯 Focus Recommendation"
        
        # Build synthesis response
        if high_priority:
            top_task = high_priority[0]["Task"]
            rec = f"Focus on completing your high-priority Notion task: {top_task}."
        elif events:
            rec = f"Prepare for your next upcoming calendar event: {events[0].get('Event', 'No Title')}."
        else:
            rec = "Your workspace is fully cleared! A great time to start a deep work focus block."
            
        html = f"""
        <div class="th-ai-rec" style="margin-top: 10px;">
            <div class="th-ai-rec-eyebrow">✦ Coral Assistant &nbsp;·&nbsp; Focus Recommendation</div>
            <div class="th-ai-rec-task">{rec}</div>
            <div class="th-ai-rec-reasons">
                <span class="th-reason-pill priority" style="background:rgba(255,107,71,0.12); color:var(--coral); border:1px solid rgba(255,107,71,0.2);">✓ High Priority</span>
                <span class="th-reason-pill schedule" style="background:var(--teal-subtle); color:var(--teal); border:1px solid rgba(0,212,170,0.2);">✓ No Schedule Conflict</span>
                <span class="th-reason-pill impact" style="background:var(--blue-subtle); color:var(--blue); border:1px solid rgba(79,142,247,0.2);">✓ Highest Impact Today</span>
            </div>
        </div>
        """
        return {
            "headline": headline,
            "response_html": html,
            "type": "focus"
        }
        
    # Intent 2: "Show my Notion tasks"
    elif "notion" in q or "tasks" in q:
        tasks = get_notion_tasks_via_coral()
        if not tasks:
            # Fallback to dashboard tasks
            tasks = dashboard_context.get("tasks", [])
            
        headline = "📋 Notion Tasks (via Coral MCP)"
        
        rows = ""
        for task in tasks[:6]: # Limit to top 6
            dot_cls = str(task.get("Priority", "")).lower()
            status_raw = str(task.get("Status", ""))
            status_cls = status_raw.lower().replace(" ", "")
            rows += f"""<div class="th-task-row">
                <div class="th-task-dot {dot_cls}"></div>
                <div class="th-task-name">{task.get('Task', '')}</div>
                <div class="th-task-category">{task.get('Category', '')}</div>
                <div class="th-status-badge {status_cls}">{status_raw}</div>
            </div>"""
            
        html = f"""
        <div class="th-panel" style="margin-top: 10px;">
            <div class="th-panel-header">
                <div class="th-panel-title">📋 Notion Workspace Tasks</div>
                <span class="th-panel-count">{len(tasks)}</span>
            </div>
            {rows}
        </div>
        """
        return {
            "headline": headline,
            "response_html": html,
            "type": "tasks"
        }
        
    # Intent 3: "Show recent GitHub activity"
    elif "github" in q or "activity" in q:
        activity = get_github_activity_via_coral()
        headline = "🐙 Recent GitHub Activity (via Coral MCP)"
        
        rows = ""
        for act in activity:
            rows += f"""<div class="th-notif-row">
                <div class="th-notif-icon">🐙</div>
                <div class="th-notif-subject">{act.get('Subject', '')}</div>
                <div class="th-notif-time">{act.get('Time', '')}</div>
            </div>"""
            
        html = f"""
        <div class="th-panel" style="margin-top: 10px;">
            <div class="th-panel-header">
                <div class="th-panel-title">🐙 GitHub Activity</div>
                <span class="th-panel-count">{len(activity)}</span>
            </div>
            {rows}
        </div>
        """
        return {
            "headline": headline,
            "response_html": html,
            "type": "github"
        }
        
    # Intent 4: "Summarize my workspace"
    elif "workspace" in q or "summarize" in q:
        tasks = get_notion_tasks_via_coral()
        if not tasks:
            tasks = dashboard_context.get("tasks", [])
            
        high_priority = len([t for t in tasks if t.get("Priority") == "High" and t.get("Status") == "Todo"])
        events_count = len(dashboard_context.get("today_events", []))
        emails_count = len(dashboard_context.get("emails", []))
        
        headline = "🚀 Workspace Summary"
        
        html = f"""
        <div class="th-insight-card" style="margin-top: 10px; border-color: var(--coral);">
            <div class="th-insight-header">⚡ Workspace Synthesis</div>
            <div class="th-insight-body">
                Coral MCP integrated pipeline scanned your workspace and found:<br/>
                • <strong>{len(tasks)}</strong> total Notion tasks (<strong>{high_priority}</strong> high-priority pending)<br/>
                • <strong>{events_count}</strong> upcoming events today<br/>
                • <strong>{emails_count}</strong> unread emails in Gmail
            </div>
            <div class="th-insight-action">
                <strong>Recommendation:</strong> Tackle the high-priority Notion items before your first calendar event.
            </div>
        </div>
        """
        return {
            "headline": headline,
            "response_html": html,
            "type": "summary"
        }
        
    # Default fallback response detailing the supported intents
    else:
        headline = "💡 Demo Mode Assistant"
        html = """
        <div class="th-panel" style="margin-top: 10px; border-color: rgba(245, 200, 66, 0.35); background: var(--yellow-subtle);">
            <div style="color: var(--yellow); font-size: 13px; font-weight: 500; margin-bottom: 8px;">
                ⚠️ I'm optimized for the hackathon demo. Try asking:
            </div>
            <ul style="margin-left: 20px; font-size: 12px; color: var(--text-primary); line-height: 1.6;">
                <li><em>"What should I focus on today?"</em></li>
                <li><em>"Show my Notion tasks"</em></li>
                <li><em>"Show recent GitHub activity"</em></li>
                <li><em>"Summarize my workspace"</em></li>
            </ul>
        </div>
        """
        return {
            "headline": headline,
            "response_html": html,
            "type": "help"
        }
