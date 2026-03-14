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
        <title>Technical Engineering Profile | Sidad Ahmad</title>
        <style>
            :root { --bg: #0b1e2d; --card-bg: #112a40; --accent: #4db8ff; --green: #2ecc71; }
            body { background: var(--bg); color: white; font-family: 'Segoe UI', sans-serif; margin: 0; padding: 20px; }
            .header { text-align: right; margin-bottom: 30px; border-bottom: 1px solid #1e3a5f; padding-bottom: 10px; }
            h1 { color: var(--accent); margin: 0; font-size: 1.8rem; }
            .expertise { color: #94a3b8; font-size: 0.9rem; }
            
            .dashboard-box { border: 2px solid #1e3a5f; border-radius: 15px; padding: 20px; background: rgba(17, 42, 64, 0.5); }
            .dashboard-title { text-align: center; color: var(--accent); font-size: 1.5rem; margin-bottom: 20px; font-weight: bold; }
            
            .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; }
            .card { background: var(--card-bg); border: 1px solid #1e3a5f; padding: 25px; border-radius: 12px; text-align: center; position: relative; }
            
            .value { font-size: 2.5rem; font-weight: bold; margin: 5px 0; }
            .label { color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; font-size: 0.8rem; }
            .badge { position: absolute; top: 20px; right: 20px; background: rgba(46, 204, 113, 0.2); color: var(--green); padding: 2px 8px; border-radius: 5px; font-size: 0.7rem; }
            
            .footer-bar { margin-top: 20px; background: #081621; border: 1px solid #1e3a5f; padding: 10px; border-radius: 8px; text-align: center; color: var(--accent); font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>TECHNICAL ENGINEERING PROFILE 🚀</h1>
            <div class="expertise">Candidate: Sidad Ahmad | Expertise: Python, Ruby, Data Analysis</div>
        </div>

        <div class="dashboard-box">
            <div class="dashboard-title">高性能 Data & Systems Dashboard 💻</div>
            <div class="grid">
                <div class="card">
                    <span class="badge">-10ms</span>
                    <div class="value">45ms</div>
                    <div class="label">PYTHON API LATENCY</div>
                </div>
                <div class="card">
                    <span class="badge">15%</span>
                    <div class="value">1.2k <small style="font-size: 1rem;">req/s</small></div>
                    <div class="label">RUBY SERVICE THROUGHPUT</div>
                </div>
                <div class="card">
                    <span class="badge">0.2%</span>
                    <div class="value">98.4%</div>
                    <div class="label">DATA PROCESSING ACCURACY</div>
                </div>
            </div>
            <div class="footer-bar">📊 System Load Analysis 📊</div>
        </div>
        <p style="text-align:center; color: #566573; margin-top: 20px;">Dashboard is Live and Fully Functional.</p>
    </body>
    </html>
    """
