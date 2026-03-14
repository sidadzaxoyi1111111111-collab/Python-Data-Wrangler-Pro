from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import random

app = FastAPI()

# ئەڤ بەشە داتایێن داشبۆردێ ئامادە دکەت
@app.get("/api/metrics")
async def get_metrics():
    return {
        "latency": f"{random.randint(40, 50)}ms",
        "throughput": f"{round(random.uniform(1.0, 1.5), 1)}k req/s",
        "accuracy": f"{round(random.uniform(98.0, 99.5), 1)}%"
    }

# ڕێکا سەرەکی بۆ نیشاندانا لاپەرەی
@app.get("/", response_class=HTMLResponse)
async def read_dashboard(request: Request):
    return """
    <html>
        <head>
            <title>Sidad AI Dashboard</title>
            <style>
                body { background-color: #0b1e2d; color: white; font-family: sans-serif; text-align: center; }
                .container { display: flex; justify-content: center; gap: 20px; margin-top: 50px; }
                .card { border: 1px solid #1e3a5f; padding: 20px; border-radius: 10px; width: 200px; background: #112a40; }
                h1 { color: #4db8ff; }
                .value { font-size: 2em; font-weight: bold; }
            </style>
        </head>
        <body>
            <h1>TECHNICAL ENGINEERING PROFILE 🚀</h1>
            <p>Candidate: Sidad Ahmad | Location: Zakho</p>
            <div class="container">
                <div class="card"><div>API LATENCY</div><div class="value" id="latency">45ms</div></div>
                <div class="card"><div>DB THROUGHPUT</div><div class="value" id="throughput">1.2k</div></div>
                <div class="card"><div>AI ACCURACY</div><div class="value" id="accuracy">98.4%</div></div>
            </div>
            <script>
                setInterval(async () => {
                    const res = await fetch('/api/metrics');
                    const data = await res.json();
                    document.getElementById('latency').innerText = data.latency;
                    document.getElementById('throughput').innerText = data.throughput;
                    document.getElementById('accuracy').innerText = data.accuracy;
                }, 2000);
            </script>
        </body>
    </html>
    """
