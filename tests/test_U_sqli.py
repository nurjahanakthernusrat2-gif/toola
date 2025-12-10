from core.utils import SQLI_PAYLOAD

def run(client, reporter):
    r = client.post("/login", data={"email": SQLI_PAYLOAD, "password": SQLI_PAYLOAD})
    if "sql" in r.text.lower() or r.status_code >= 500:
        reporter.add("U_SQLI", "FAIL", "SQL error triggered")
    else:
        reporter.add("U_SQLI", "PASS", f"Code {r.status_code}")
