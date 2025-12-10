def run(client, reporter):
    r = client.post("/login", data={"email": "unknown", "password": "wrong"})
    if "invalid" in r.text.lower() or "wrong" in r.text.lower():
        reporter.add("N_ERROR_ENUM", "FAIL", "Detailed error leaks info")
    else:
        reporter.add("N_ERROR_ENUM", "PASS", "No sensitive error info")
