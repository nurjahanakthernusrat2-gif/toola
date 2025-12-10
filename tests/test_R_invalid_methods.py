def run(client, reporter):
    r = client.custom("PUT", "/login")
    if r.status_code in [400, 405]:
        reporter.add("R_INVALID_METHOD", "PASS", "PUT blocked")
    else:
        reporter.add("R_INVALID_METHOD", "FAIL", f"Accepted PUT {r.status_code}")
