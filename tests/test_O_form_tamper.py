def run(client, reporter):
    r = client.post("/login", data={"admin": "1", "role": "super"})
    if r.status_code in [400, 403]:
        reporter.add("O_TAMPER", "PASS", "Blocked tampering")
    else:
        reporter.add("O_TAMPER", "FAIL", "Accepted tampered form")
