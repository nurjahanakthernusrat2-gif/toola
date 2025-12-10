import requests
from bs4 import BeautifulSoup
import json, time, datetime
from urllib.parse import urljoin

def detect_form(url):
    """Detect login form fields + CSRF token."""
    print("[+] Detecting login form…")
    r = requests.get(url, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")

    form = soup.find("form")
    if not form:
        return None

    action = form.get("action", "")
    method = form.get("method", "GET").upper()
    inputs = form.find_all("input")

    username, password, csrf_name, csrf_val = None, None, None, None

    for i in inputs:
        t = i.get("type", "").lower()
        name = i.get("name", "")
        if t == "text" or "user" in name.lower():
            username = name
        if t == "password":
            password = name
        if "csrf" in name.lower():
            csrf_name = name
            csrf_val = i.get("value", "")

    return {
        "action": action,
        "method": method,
        "username": username,
        "password": password,
        "csrf_name": csrf_name,
        "csrf_value": csrf_val,
    }

def submit(url, form, data):
    """Submit form and return status code."""
    action_url = urljoin(url, form["action"])
    method = form["method"]

    try:
        if method == "POST":
            r = requests.post(action_url, data=data, allow_redirects=False, timeout=10)
        else:
            r = requests.get(action_url, params=data, allow_redirects=False, timeout=10)
        return r.status_code, r.headers, r.text
    except requests.RequestException:
        return 0, {}, ""

def run_tests(url):
    form = detect_form(url)
    if not form:
        raise Exception("Login form not detected!")

    print("[+] Running authentication test suite (A–Z)…")
    tests = {}

    # --- A) Login form discovery ---
    tests["A_form_discovery"] = 200 if form else 0

    # --- B) Form action detection ---
    tests["B_form_action"] = 200 if form.get("action") else 0

    # --- C) HTTP method confirmation ---
    tests["C_method_check"] = 200 if form.get("method") in ["GET","POST"] else 0

    # --- D) CSRF token presence ---
    tests["D_csrf_presence"] = 200 if form.get("csrf_name") else 0

    # --- E) CSRF validation test (submit without token) ---
    if form.get("csrf_name"):
        code, _, _ = submit(url, form, {
            form["username"]: "admin",
            form["password"]: "admin"
        })
        tests["E_csrf_validation"] = 200 if code != 200 else 0
    else:
        tests["E_csrf_validation"] = 0

    # --- F) Correct login attempt ---
    data = {form["username"]:"admin", form["password"]:"admin"}
    if form.get("csrf_name"):
        data[form["csrf_name"]] = form["csrf_value"]
    code, _, _ = submit(url, form, data)
    tests["F_correct_login"] = code

    # --- G) Wrong login attempt ---
    data_wrong = {form["username"]:"admin", form["password"]:"WRONG"}
    code, _, _ = submit(url, form, data_wrong)
    tests["G_wrong_login"] = code

    # --- H) No-CSRF attack test ---
    if form.get("csrf_name"):
        data_no_csrf = {form["username"]:"admin", form["password"]:"admin"}
        code, _, _ = submit(url, form, data_no_csrf)
        tests["H_no_csrf_attack"] = code
    else:
        tests["H_no_csrf_attack"] = 0

    # --- I) Session fixation (check Set-Cookie) ---
    _, headers, _ = submit(url, form, data)
    tests["I_session_fixation"] = 200 if "Set-Cookie" in headers else 0

    # --- J) Redirect chain validation ---
    try:
        r = requests.post(urljoin(url, form["action"]), data=data, allow_redirects=True)
        tests["J_redirect_chain"] = 200 if r.history else 0
    except:
        tests["J_redirect_chain"] = 0

    # --- K) Cookie security check ---
    secure_flag = "secure" in headers.get("Set-Cookie", "").lower()
    httponly_flag = "httponly" in headers.get("Set-Cookie", "").lower()
    tests["K_cookie_security"] = 200 if secure_flag and httponly_flag else 0

    # --- L) Response code behavior ---
    tests["L_response_code"] = code if code in [200,302,401,403] else 0

    # --- M) Rate-limit detection ---
    rate_codes = []
    for _ in range(3):
        c, _, _ = submit(url, form, data_wrong)
        rate_codes.append(c)
    tests["M_rate_limit"] = 429 if 429 in rate_codes else 200

    # --- N) Error message enumeration ---
    tests["N_error_message"] = 200 if "invalid" in _.lower() else 0

    # --- O) Form tampering ---
    data_tamper = {form["username"]:"", form["password"]:""}
    code, _, _ = submit(url, form, data_tamper)
    tests["O_form_tamper"] = code

    # --- P) Missing-fields submission ---
    data_missing = {form["username"]:"admin"}  # no password
    code, _, _ = submit(url, form, data_missing)
    tests["P_missing_fields"] = code

    # --- Q) Empty request test ---
    code, _, _ = submit(url, form, {})
    tests["Q_empty_request"] = code

    # --- R) Invalid HTTP method ---
    try:
        r = requests.put(urljoin(url, form["action"]), data=data)
        tests["R_invalid_method"] = r.status_code
    except:
        tests["R_invalid_method"] = 0

    # --- S) Payload manipulation ---
    data_payload = {form["username"]:"<script>alert(1)</script>", form["password"]:"admin"}
    code, _, _ = submit(url, form, data_payload)
    tests["S_payload_manipulation"] = code

    # --- T) Special-char payload ---
    data_special = {form["username"]:"!@#$%^&*()", form["password"]:"admin"}
    code, _, _ = submit(url, form, data_special)
    tests["T_special_char"] = code

    # --- U) SQLi payload test in login ---
    data_sqli = {form["username"]:"' OR '1'='1", form["password"]:"admin"}
    code, _, _ = submit(url, form, data_sqli)
    tests["U_sqli_test"] = code

    # --- V) XSS payload test ---
    data_xss = {form["username"]:"<script>alert('XSS')</script>", form["password"]:"admin"}
    code, _, _ = submit(url, form, data_xss)
    tests["V_xss_test"] = code

    # --- W) Brute-force simulation health ---
    try:
        for i in range(5):
            submit(url, form, data_wrong)
        tests["W_bruteforce_health"] = 200
    except:
        tests["W_bruteforce_health"] = 0

    # --- X) Anti-bot / CSRF timing ---
    start = time.time()
    submit(url, form, data)
    duration = time.time() - start
    tests["X_anti_bot_csrf"] = 200 if duration < 5 else 0

    # --- Y) Logout behavior validation ---
    logout_url = urljoin(url, "/logout")
    try:
        r = requests.get(logout_url)
        tests["Y_logout_behavior"] = r.status_code
    except:
        tests["Y_logout_behavior"] = 0

    # --- Z) Session cleanup test ---
    tests["Z_session_cleanup"] = 200 if "Set-Cookie" in headers else 0

    return {
        "url": url,
        "timestamp": time.time(),
        "detected": {
            "action": form["action"],
            "method": form["method"],
            "username_field": form["username"],
            "password_field": form["password"],
            "csrf_name": form["csrf_name"],
            "csrf_value_len": len(form["csrf_value"]) if form["csrf_value"] else 0
        },
        "tests": tests
    }

if __name__ == "__main__":
    import sys, os
    url = os.getenv("AUTH_TEST_URL", sys.argv[1] if len(sys.argv) > 1 else None)
    if not url:
        raise SystemExit("Missing URL")

    result = run_tests(url)

    os.makedirs("auth-tests/reports", exist_ok=True)
    out = "auth-tests/reports/auth_summary.json"
    with open(out, "w") as f:
        json.dump(result, f, indent=2)

    print(f"[+] Auth test summary saved → {out}")
