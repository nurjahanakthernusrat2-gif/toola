import json, os, datetime
from pathlib import Path

def html_escape(x):
    return str(x).replace("<","&lt;").replace(">","&gt;")

# Test case descriptions
TEST_DESCRIPTIONS = {
    "A_form_discovery": "Login form উপস্থিত আছে কি না চেক করা",
    "B_form_action": "Form-এর action attribute আছে কি না চেক করা",
    "C_method_check": "Form কোন HTTP method ব্যবহার করছে (GET/POST) চেক করা",
    "D_csrf_presence": "CSRF token আছে কি না চেক করা",
    "E_csrf_validation": "CSRF token ছাড়া submit করলে block হচ্ছে কি না",
    "F_correct_login": "সঠিক credentials দিয়ে login চেষ্টা",
    "G_wrong_login": "ভুল password দিয়ে login চেষ্টা",
    "H_no_csrf_attack": "CSRF token বাদ দিয়ে login blocked কিনা চেক",
    "I_session_fixation": "Session cookie properly assign হচ্ছে কি না",
    "J_redirect_chain": "Login-এর পরে redirect ঠিকমতো কাজ করছে কি না",
    "K_cookie_security": "Cookie-তে Secure ও HttpOnly flags আছে কি না",
    "L_response_code": "Server response code (200, 302, 401, etc.)",
    "M_rate_limit": "Repeated requests-এ rate-limit 429 response চেক",
    "N_error_message": "Error message enumeration / sensitive info leakage",
    "O_form_tamper": "Form data intentionally change করা হলে server handle করছে কি না",
    "P_missing_fields": "কিছু field ছাড়া submit করলে server handle করছে কি না",
    "Q_empty_request": "পুরো ফর্ম খালি রেখে submit করলে server response",
    "R_invalid_method": "Invalid HTTP method (PUT/DELETE) block হচ্ছে কি না",
    "S_payload_manipulation": "Suspicious payload injection test",
    "T_special_char": "Special character input test",
    "U_sqli_test": "SQL Injection attempt check",
    "V_xss_test": "XSS payload injection test",
    "W_bruteforce_health": "Multiple failed attempts-এর পরে server health",
    "X_anti_bot_csrf": "Login response timing / Anti-bot check",
    "Y_logout_behavior": "Logout endpoint behavior validation",
    "Z_session_cleanup": "Session properly cleaned after logout"
}

def generate_html(infile, outfile):
    with open(infile) as f:
        data = json.load(f)

    ts = datetime.datetime.utcfromtimestamp(data["timestamp"]).strftime("%Y-%m-%d %H:%M UTC")

    html = f"""
<html>
<head>
<title>Authentication Report — {data['url']}</title>
<style>
    body {{ font-family: Arial; background: #f5f5f5; padding: 20px; }}
    .box {{ background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
    table {{ width: 100%; border-collapse: collapse; }}
    td, th {{ padding: 8px; border-bottom: 1px solid #ccc; font-size: 14px; }}
    h2 {{ margin-top: 0; }}
    .ok {{ color: green; font-weight: bold; }}
    .fail {{ color: red; font-weight: bold; }}
    .warn {{ color: orange; font-weight: bold; }}
</style>
</head>
<body>

<div class="box">
    <h2>Authentication Testing Report</h2>
    <p><b>URL:</b> {data["url"]}</p>
    <p><b>Generated:</b> {ts}</p>
</div>

<div class="box">
    <h2>Detection Summary</h2>
    <table>
        <tr><td>Form Action</td><td>{html_escape(data["detected"]["action"])}</td></tr>
        <tr><td>Method</td><td>{data["detected"]["method"]}</td></tr>
        <tr><td>Username Field</td><td>{data["detected"]["username_field"]}</td></tr>
        <tr><td>Password Field</td><td>{data["detected"]["password_field"]}</td></tr>
        <tr><td>CSRF Token Name</td><td>{data["detected"]["csrf_name"]}</td></tr>
        <tr><td>CSRF Value Length</td><td>{data["detected"]["csrf_value_len"]}</td></tr>
    </table>
</div>

<div class="box">
    <h2>Test Cases (A–Z)</h2>
    <table>
        <tr><th>Test</th><th>Description</th><th>Status</th></tr>
"""

    # Render all tests dynamically with description
    for key, value in data["tests"].items():
        description = TEST_DESCRIPTIONS.get(key, "")
        if isinstance(value, int):
            if value in (200, 301, 302):
                cls = "ok"
            elif value == 0:
                cls = "warn"
            else:
                cls = "fail"
            display = value
        else:
            cls = "warn"
            display = html_escape(str(value))

        html += f"<tr><td>{html_escape(key)}</td><td>{html_escape(description)}</td><td class='{cls}'>{display}</td></tr>\n"

    html += """
    </table>
</div>

<div class="box">
    <h2>Full Raw JSON</h2>
    <pre style="background:#222; color:#0f0; padding:15px; border-radius:6px; font-size:13px;">""" + \
        html_escape(json.dumps(data, indent=2)) + "</pre></div>"

    html += "</body></html>"

    with open(outfile, "w") as f:
        f.write(html)

    print(f"[+] HTML report saved at: {outfile}")

if __name__ == "__main__":
    Path("auth-tests/reports").mkdir(parents=True, exist_ok=True)
    generate_html("auth-tests/reports/auth_summary.json", "auth-tests/reports/auth_report.html")
