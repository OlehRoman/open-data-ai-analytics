import os
import json
from flask import Flask, render_template

app = Flask(__name__)

REPORTS_DIR = "/app/reports"
PLOTS_DIR = "/app/static/plots"


def load_report(filename):
    path = os.path.join(REPORTS_DIR, filename)
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            return {"error": f"Помилка читання: {e}"}
    return None


@app.route('/')
def index():
    quality = load_report("quality_report.json")
    research = load_report("research_report.json")

    plots = []
    if os.path.exists(PLOTS_DIR):
        plots = [f for f in os.listdir(PLOTS_DIR) if f.endswith('.png')]

    return render_template(
        'index.html',
        quality=quality,
        research=research,
        plots=plots
    )


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)