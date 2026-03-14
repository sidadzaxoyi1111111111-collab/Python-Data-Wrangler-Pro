from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import sqlite3

app = FastAPI()

# Database Initialization (SQL)
def init_db():
    conn = sqlite3.connect("tech_hub.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects 
        (id INTEGER PRIMARY KEY, name TEXT, tech TEXT, status TEXT)
    """)
    # Seed data
    sample_data = [
        (1, 'Backend Engine', 'Python / FastAPI', 'Running'),
        (2, 'Data Storage', 'SQL / SQLite', 'Secure'),
        (3, 'Web Services', 'PHP / HTML / CSS', 'Responsive'),
        (4, 'AI Integration', 'Python / Async', 'Active')
    ]
    cursor.executemany("INSERT OR IGNORE INTO projects VALUES (?,?,?,?)", sample_data)
    conn.commit()
    conn.close()

init_db()

@app.get("/api/status")
async def get_tech_status():
    conn = sqlite3.connect("tech_hub.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM projects")
    rows = cursor.fetchall()
    conn.close()
    return {"projects": rows}

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Sidad Ahmad | Tech Dashboard</title>
        <style>
            :root { --accent: #00ffcc; --bg: #0d1117; }
            body { background-color: var(--bg); color: white; font-family: 'Segoe UI', sans-serif; margin: 0; padding: 20px; }
            .container { max-width: 1000px; margin: auto; }
            header { border-bottom: 2px solid var(--accent); padding-bottom: 10px; margin-bottom: 30px; }
            .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; }
            .card { background: #161b22; border: 1px solid #30363d; padding: 20px; border-radius: 12px; transition: 0.3s; }
            .card:hover { border-color: var(--accent); box-shadow: 0 0 15px rgba(0, 255, 204, 0.1); }
            h3 { color: var(--accent); margin-top: 0; }
            .badge { background: #238636; padding: 4px 10px; border-radius: 20px; font-size: 12px; }
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>Sidad Ahmad - Engineering Profile</h1>
                <p>Status: Multi-Platform Tech Hub (Mobile & PC)</p>
            </header>
            <div class="grid">
                <div class="card"><h3>Backend</h3><p>FastAPI Service</p><span class="badge">ONLINE</span></div>
                <div class="card"><h3>Database</h3><p>SQL - SQLite3</p><span class="badge">CONNECTED</span></div>
                <div class="card"><h3>Frontend</h3><p>Responsive HTML/CSS</p><span class="badge">STABLE</span></div>
                <div class="card"><h3>Integration</h3><p>PHP/Python Bridge</p><span class="badge">READY</span></div>
            </div>
        </div>
    </body>
    </html>
    """
