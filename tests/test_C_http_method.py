def run(client, reporter):
    r = client.get("/login")
    if r.status_code in [200, 302]:
        reporter.add("C_HTTP_METHOD", "PASS", "GET allowed")
    else:
        reporter.add("C_HTTP_METHOD", "FAIL", f"Unexpected {r.status_code}")
