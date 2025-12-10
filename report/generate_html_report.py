import os
import json
import argparse
from datetime import datetime

# -----------------------------------------------------------
# Helper to load JSON safely
# -----------------------------------------------------------
def load_json(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception:
        return {"error": f"Invalid JSON -> {path}"}


# -----------------------------------------------------------
# HTML Template (Base)
# -----------------------------------------------------------
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Auth Scan Report - {project}</title>
<style>
    body {{
        font-family: Arial, sans-serif;
        background: #f6f6f6;
        margin: 0;
        padding: 0;
    }}

    .container {{
        width: 90%;
        margin: auto;
        padding: 20px;
    }}

    h1, h2 {{
        color: #333;
    }}

    .summary-box {{
        background: #fff;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 25px;
        box-shadow: 0 0 5px rgba(0,0,0,0.1);
    }}

    table {{
        width: 100%;
        border-collapse: collapse;
        margin-top: 20px;
        background: #fff;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 0 5px rgba(0,0,0,0.1);
    }}

    th, td {{
        padding: 10px;
        border-bottom: 1px solid #ddd;
    }}

    th {{
        background: #333;
        color: #fff;
        text-align: left;
    }}

    tr.pass td {{
        background: #e8ffe8;
    }}
    tr.fail td {{
        background: #ffe8e8;
    }}
</style>
</head>
<body>

<div class="container">

<h1>Authentication Scan Report</h1>

<div class="summary-box">
    <h2>Summary</h2>
    <strong>Project:</strong> {project}<br>
    <strong>Target:</strong> {target}<br>
    <strong>Generated:</strong> {generated}<br>
    <strong>Total Tests:</strong> {total_tests}<br>
    <strong>Pass:</strong> {pass_count}<br>
    <strong>Fail:</strong> {fail_count}<br>
</div>

<h2>Test Results</h2>

<table>
<tr>
    <th>Test Name</th>
    <th>Status</th>
    <th>Attempts</th>
    <th>Payload Used</th>
    <th>Notes</th>
</tr>

{rows}

</table>

</div>

</body>
</html>
"""


# -----------------------------------------------------------
# Build HTML rows
# -----------------------------------------------------------
def build_row(test):

    name = test.get("name", "Unknown Test")
    status = test.get("status", "unknown")
    attempts = test.get("attempts", "N/A")
    payload = test.get("payload", "N/A")
    notes = test.get("notes", "N/A")

    row_class = "pass" if status.lower() == "pass" else "fail"

    return f"""
<tr class="{row_class}">
    <td>{name}</td>
    <td>{status}</td>
    <td>{attempts}</td>
    <td>{payload}</td>
    <td>{notes}</td>
</tr>
"""


# -----------------------------------------------------------
# Main Report Builder
# -----------------------------------------------------------
def generate_report(input_dir, output_file, project, target):
    tests = []
    rows = ""

    # Load all JSON result files
    for file in sorted(os.listdir(input_dir)):
        if file.endswith(".json"):
            data = load_json(os.path.join(input_dir, file))
            rows += build_row(data)
            tests.append(data)

    # Summary Stats
    total_tests = len(tests)
    pass_count = sum(1 for t in tests if t.get("status") == "PASS")
    fail_count = total_tests - pass_count

    # Final HTML build
    html = HTML_TEMPLATE.format(
        project=project,
        target=target,
        generated=datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        total_tests=total_tests,
        pass_count=pass_count,
        fail_count=fail_count,
        rows=rows
    )

    # Write output
    with open(output_file, "w") as out:
        out.write(html)

    print(f"[+] HTML Report Generated → {output_file}")


# -----------------------------------------------------------
# CLI
# -----------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Directory of JSON results")
    parser.add_argument("--output", required=True, help="HTML output file")
    parser.add_argument("--project", required=True)
    parser.add_argument("--target", required=True)
    args = parser.parse_args()

    generate_report(
        input_dir=args.input,
        output_file=args.output,
        project=args.project,
        target=args.target
    )
