from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def get_dashboard():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Sidad Ahmad | Tech Dashboard</title>
        <style>
            :root { --bg: #0b1e2d; --card-bg: #112a40; --accent: #4db8ff; --green: #2ecc71; }
            body { background: var(--bg); color: white; font-family: 'Segoe UI', sans-serif; margin: 0; padding: 20px; }
            .container { max-width: 1000px; margin: auto; border: 1px solid #1e3a5f; padding: 30px; border-radius: 15px; background: rgba(17, 42, 64, 0.3); }
            
            .profile-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 40px; }
            .profile-info { text-align: right; }
            .profile-info h1 { color: var(--accent); margin: 0; font-size: 2rem; letter-spacing: 1px; }
            .profile-info p { margin: 5px 0; color: #cbd5e1; }

            .dashboard-title { text-align: center; color: var(--accent); font-size: 1.8rem; margin-bottom: 10px; font-weight: bold; }
            .sub-title { text-align: center; color: #94a3b8; margin-bottom: 30px; }

            .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; }
            .card { background: var(--card-bg); border: 1px solid #1e3a5f; padding: 25px; border-radius: 12px; text-align: center; position: relative; }
            
            .value { font-size: 3rem; font-weight: bold; margin: 5px 0; display: block; }
            .label { color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; font-size: 0.9rem; font-weight: 600; }
            .badge { position: absolute; top: 20px; right: 20px; background: rgba(46, 204, 113, 0.2); color: var(--green); padding: 4px 12px; border-radius: 6px; font-size: 0.8rem; }
            
            .footer-bar { margin-top: 30px; background: #081621; border: 1px solid #1e3a5f; padding: 15px; border-radius: 10px; text-align: center; color: var(--accent); font-weight: bold; font-size: 1.2rem; }
            .live-status { text-align: center; margin-top: 20px; color: #566573; font-size: 0.9rem; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="profile-header">
                <img src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" width="80" style="filter: brightness(0.8);">
                <div class="profile-info">
                    <h1>TECHNICAL ENGINEERING PROFILE 🚀</h1>
                    <p><strong>Candidate:</strong> Sidad Ahmad</p>
                    <p><strong>Expertise:</strong> Python (FastAPI, Async), Ruby, SQL, Data Analytics</p>
                    <p><strong>Location:</strong> Zakho / Remote</p>
                </div>
            </div>

            <div class="dashboard-title">高性能 Data & Metrics Dashboard 💻</div>
            <div class="sub-title">Real-time Data Processing & System Metrics Demonstration.</div>

            <div class="grid">
                <div class="card">
                    <span class="badge">-10ms</span>
                    <span class="value">45ms</span>
                    <span class="label">Python API Latency</span>
                </div>
                <div class="card">
                    <span class="badge">15%</span>
                    <span class="value">1.2k</span>
                    <span class="label">Ruby Service Throughput</span>
                </div>
                <div class="card">
                    <span class="badge">0.2%</span>
                    <span class="value">98.4%</span>
                    <span class="label">Data Accuracy Rate</span>
                </div>
            </div>

            <div class="footer-bar">📊 System Load Analysis 📊</div>
            <div class="live-status">Dashboard is Live and Fully Functional.</div>
        </div>
    </body>
    </html>
    """
