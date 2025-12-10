import json
from datetime import datetime

class Reporter:
    def __init__(self):
        self.results = {}

    def add(self, test_id, status, details=None):
        self.results[test_id] = {
            "status": status,
            "details": details
        }

    def save_json(self, path="reports/results.json"):
        with open(path, "w") as f:
            json.dump({
                "generated": str(datetime.utcnow()),
                "results": self.results
            }, f, indent=2)

    def save_html(self, path="reports/report.html"):
        html = "<html><body><h1>Authentication Test Report</h1>"
        html += "<table border=1><tr><th>Test</th><th>Status</th><th>Details</th></tr>"
        for k, v in self.results.items():
            html += f"<tr><td>{k}</td><td>{v['status']}</td><td>{v.get('details','')}</td></tr>"
        html += "</table></body></html>"
        with open(path, "w") as f:
            f.write(html)
