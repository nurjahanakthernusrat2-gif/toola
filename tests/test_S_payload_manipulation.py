def run(client, reporter):
    payload = {"email": "a", "password": '{"admin":true}'}
    r = client.post("/login", data=payload)
    if r.status_code in [400, 403]:
        reporter.add("S_PAYLOAD", "PASS", "Blocked JSON-injection")
    else:
        reporter.add("S_PAYLOAD", "FAIL", "Accepted manipulated payload")
