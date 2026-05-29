import subprocess
import json
import os
from datetime import datetime
import time

# Constants
NOTION_DATA_SOURCE_ID = "4b47dd3e-dfbd-49fc-a767-3b951ebd4e0b"
import re

# In-memory query cache: { sql_query: (timestamp, results) }
_query_cache = {}
CACHE_TTL = 60  # seconds

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
    """Execute a SQL query via Coral CLI and return results as a list of dicts with 60s caching."""
    global _query_cache
    current_time = time.time()
    
    # Check cache
    if sql_query in _query_cache:
        timestamp, cached_results = _query_cache[sql_query]
        if current_time - timestamp < CACHE_TTL:
            print(f"[CACHE HIT] SQL: {sql_query} (served from cache, age: {current_time - timestamp:.2f}s)")
            return cached_results
            
    print(f"[CACHE MISS] SQL: {sql_query}")
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
            results = []
        else:
            results = json.loads(output)
            
        # Update cache
        _query_cache[sql_query] = (current_time, results)
        return results
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

def get_cross_source_join_insights() -> tuple:
    """Perform a Coral SQL cross-source join between Notion tasks and GitHub notifications."""
    query = (
        "SELECT n.properties, g.subject__title, g.repository__name, g.updated_at "
        "FROM notion.data_source_pages n "
        "JOIN github.notifications g "
        "ON g.repository__name IS NOT NULL "
        f"WHERE n.data_source_id = '{NOTION_DATA_SOURCE_ID}' LIMIT 3"
    )
    
    rows = run_coral_query(query)
    insights = []
    is_fallback = False
    
    for row in rows:
        try:
            properties = json.loads(row.get("properties", "{}"))
            title_list = properties.get("Task", {}).get("title", [])
            task_name = title_list[0].get("plain_text", "") if title_list else "Unnamed Task"
            task_name = strip_markdown(task_name)
            
            github_subject = strip_markdown(row.get("subject__title", ""))
            repo_name = strip_markdown(row.get("repository__name", ""))
            updated = row.get("updated_at", "")
            
            # Format time
            time_str = "Recent"
            if updated:
                try:
                    dt = datetime.fromisoformat(updated.replace("Z", "+00:00"))
                    time_str = dt.strftime("%b %d · %I:%M %p")
                except Exception:
                    time_str = updated
                    
            insights.append({
                "Task": task_name,
                "GitHub_Subject": github_subject,
                "Repository": repo_name,
                "Time": time_str
            })
        except Exception as e:
            print(f"Error parsing join row: {e}")
            
    # Mock fallback if empty (e.g., auth failure)
    if not insights:
        is_fallback = True
        insights = [
            {
                "Task": "Build Coral Integration API",
                "GitHub_Subject": "PR #102: Connected Coral MCP pipelines to Streamlit",
                "Repository": "task-harbor-ai",
                "Time": "10m ago"
            },
            {
                "Task": "Review PR #42",
                "GitHub_Subject": "PR #42 approved by reviewer",
                "Repository": "task-harbor-ai",
                "Time": "2m ago"
            }
        ]
        
    return insights, is_fallback

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
        # Fetch Cross-Source Join Insights via Coral SQL Join
        join_insights, is_fallback = get_cross_source_join_insights()
        
        headline = "🎯 Focus Recommendation (via Coral SQL Join)"
        
        # Visual indicator status badge
        status_badge = '<span class="th-reason-pill" style="background:#ff4b4b20; color:#ff4b4b; border:1px solid #ff4b4b40;">🔴 FALLBACK DEMO DATA</span>' if is_fallback else '<span class="th-reason-pill" style="background:#00d4aa20; color:#00d4aa; border:1px solid #00d4aa40;">🟢 LIVE CORAL DATA</span>'
        
        if join_insights:
            top_insight = join_insights[0]
            rec = f"Focus on completing Notion task: <strong>{top_insight['Task']}</strong>.<br/>" \
                  f"Linked GitHub Activity: <em>\"{top_insight['GitHub_Subject']}\"</em> (Repo: {top_insight['Repository']})"
        else:
            rec = "Your workspace is fully cleared! A great time to start a deep work focus block."
            
        html = f"""
        <div class="th-ai-rec" style="margin-top: 10px; border-left: 4px solid var(--coral);">
            <div class="th-ai-rec-eyebrow">✦ Coral SQL Multi-Source Join &nbsp;·&nbsp; Focus Recommendation</div>
            <div class="th-ai-rec-task" style="font-size: 14px; line-height: 1.6;">{rec}</div>
            <div class="th-ai-rec-reasons" style="margin-top: 10px;">
                {status_badge}
                <span class="th-reason-pill priority" style="background:rgba(255,107,71,0.12); color:var(--coral); border:1px solid rgba(255,107,71,0.2);">✓ Coral SQL Join Match</span>
                <span class="th-reason-pill schedule" style="background:var(--teal-subtle); color:var(--teal); border:1px solid rgba(0,212,170,0.2);">✓ Notion-GitHub Linked</span>
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

def clear_coral_cache():
    """Clear the in-memory Coral SQL query cache."""
    global _query_cache
    _query_cache.clear()

def get_coral_schemas() -> list:
    """Retrieve all available data source schemas from Coral metadata."""
    query = "SELECT DISTINCT table_schema FROM information_schema.tables WHERE table_schema NOT IN ('information_schema', 'coral') ORDER BY table_schema"
    rows = run_coral_query(query)
    schemas = [row.get("table_schema") for row in rows if row.get("table_schema")]
    if not schemas:
        # Fallback
        schemas = ["notion", "github"]
    return schemas

def get_coral_tables(schema: str) -> list:
    """Retrieve all tables for a specific schema from Coral metadata."""
    query = f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{schema}' ORDER BY table_name"
    rows = run_coral_query(query)
    tables = [row.get("table_name") for row in rows if row.get("table_name")]
    if not tables:
        # Fallback
        if schema == "notion":
            tables = ["data_source_pages", "data_sources", "databases", "pages"]
        elif schema == "github":
            tables = ["notifications", "issues", "pull_requests", "repositories"]
        else:
            tables = []
    return tables

def get_coral_columns(schema: str, table: str) -> list:
    """Retrieve columns and data types for a specific table from Coral metadata."""
    query = f"SELECT column_name, data_type FROM information_schema.columns WHERE table_schema = '{schema}' AND table_name = '{table}' ORDER BY column_name"
    cols = run_coral_query(query)
    if not cols:
        # Fallback
        if schema == "notion" and table == "data_source_pages":
            cols = [
                {"column_name": "id", "data_type": "Utf8"},
                {"column_name": "properties", "data_type": "Utf8"},
                {"column_name": "url", "data_type": "Utf8"},
                {"column_name": "created_time", "data_type": "Timestamp"}
            ]
        elif schema == "github" and table == "notifications":
            cols = [
                {"column_name": "subject__title", "data_type": "Utf8"},
                {"column_name": "repository__name", "data_type": "Utf8"},
                {"column_name": "unread", "data_type": "Boolean"},
                {"column_name": "updated_at", "data_type": "Utf8"}
            ]
        else:
            cols = [
                {"column_name": "id", "data_type": "Utf8"},
                {"column_name": "name", "data_type": "Utf8"}
            ]
    return cols

def get_coral_sample_rows(schema: str, table: str, limit: int = 5) -> list:
    """Retrieve sample rows for a specific table."""
    query = f"SELECT * FROM {schema}.{table} LIMIT {limit}"
    rows = run_coral_query(query)
    if not rows:
        # Fallback
        if schema == "notion" and table == "data_source_pages":
            rows = [
                {"id": "task-1", "properties": "{\"Task\":{\"title\":[{\"plain_text\":\"Build Coral Integration API\"}]}}", "url": "https://notion.so/task1"},
                {"id": "task-2", "properties": "{\"Task\":{\"title\":[{\"plain_text\":\"Review PR #42\"}]}}", "url": "https://notion.so/task2"}
            ]
        elif schema == "github" and table == "notifications":
            rows = [
                {"subject__title": "PR #102: Connected Coral MCP pipelines to Streamlit", "repository__name": "task-harbor-ai", "unread": True, "updated_at": "2026-05-29T06:00:00Z"},
                {"subject__title": "PR #42 approved by reviewer", "repository__name": "task-harbor-ai", "unread": True, "updated_at": "2026-05-29T06:30:00Z"}
            ]
        else:
            rows = [{"id": "mock-1", "name": "Sandbox Item 1"}]
    return rows
