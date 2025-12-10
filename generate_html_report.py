import json
import os

RESULT_FILE = "reports/results.json"
OUTPUT_HTML = "reports/report.html"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<title>Authentication Scan Report</title>
<style>
body {{ font-family: Arial; background: #fafafa; }}
table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
th, td {{ padding: 10px; border-bottom: 1px solid #ccc; }}
th {{ background: #222; color: white; }}
.pass {{ color: green; font-weight: bold; }}
.fail {{ color: red; font-weight: bold; }}
</style>
</head>
<body>

<h1>Authentication Scan Report</h1>

<h2>Summary</h2>
<p><b>Generated:</b> {generated}</p>
<p><b>Total Tests:</b> {total}</p>
<p><b>Pass:</b> {passed}</p>
<p><b>Fail:</b> {failed}</p>

<h2>Test Results</h2>
<table>
<tr>
<th>Test Name</th>
<th>Status</th>
<th>Attempts</th>
<th>Payload</th>
<th>Notes</th>
</tr>
{rows}
</table>

</body>
</html>
"""

def load_results():
    if not os.path.exists(RESULT_FILE):
        return None

    with open(RESULT_FILE, "r") as fp:
        return json.load(fp)


def make_html():
    data = load_results()
    if not data:
        print("[-] No results.json found")
        return

    rows = ""

    for test in data["tests"]:
        status_class = "pass" if test["status"] == "PASS" else "fail"

        rows += f"""
        <tr>
            <td>{test['name']}</td>
            <td class="{status_class}">{test['status']}</td>
            <td>{test.get('attempts','-')}</td>
            <td>{test.get('payload','-')}</td>
            <td>{test.get('notes','')}</td>
        </tr>
        """

    html_content = HTML_TEMPLATE.format(
        generated=data["generated"],
        total=len(data["tests"]),
        passed=sum(1 for t in data["tests"] if t["status"] == "PASS"),
        failed=sum(1 for t in data["tests"] if t["status"] == "FAIL"),
        rows=rows
    )

    with open(OUTPUT_HTML, "w") as fp:
        fp.write(html_content)

    print(f"[+] HTML report generated → {OUTPUT_HTML}")


if __name__ == "__main__":
    make_html()
