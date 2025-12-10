import json, os, datetime
from pathlib import Path

def html_escape(x):
    return str(x).replace("<","&lt;").replace(">","&gt;")

# Test case descriptions in English
TEST_DESCRIPTIONS = {
    "A_form_discovery": "Check if the login form is present on the page",
    "B_form_action": "Verify that the form has an action attribute",
    "C_method_check": "Confirm the HTTP method used by the form (GET/POST)",
    "D_csrf_presence": "Check if a CSRF token is present",
    "E_csrf_validation": "Verify server blocks submission without CSRF token",
    "F_correct_login": "Attempt login with correct credentials",
    "G_wrong_login": "Attempt login with incorrect password",
    "H_no_csrf_attack": "Test login without CSRF token when it exists",
    "I_session_fixation": "Check if session cookies are properly assigned",
    "J_redirect_chain": "Verify login redirects function correctly",
    "K_cookie_security": "Check cookies for Secure and HttpOnly flags",
    "L_response_code": "Check server response codes (200, 302, 401, etc.)",
    "M_rate_limit": "Test if repeated requests trigger rate-limiting",
    "N_error_message": "Check for information leakage in error messages",
    "O_form_tamper": "Test server handling of tampered form data",
    "P_missing_fields": "Check submission with missing fields",
    "Q_empty_request": "Submit empty form and check server response",
    "R_invalid_method": "Test server handling of invalid HTTP methods",
    "S_payload_manipulation": "Attempt suspicious input injection",
    "T_special_char": "Test form with special characters in input",
    "U_sqli_test": "Attempt SQL injection in login fields",
    "V_xss_test": "Attempt XSS injection in login fields",
    "W_bruteforce_health": "Check server stability under multiple failed logins",
    "X_anti_bot_csrf": "Measure login response timing / Anti-bot check",
    "Y_logout_behavior": "Validate logout endpoint behavior",
    "Z_session_cleanup": "Ensure session is properly cleared after logout"
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
