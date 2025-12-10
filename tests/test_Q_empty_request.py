def run(client, reporter):
    r = client.custom("POST", "/login")
    if r.status_code in [400, 422]:
        reporter.add("Q_EMPTY", "PASS", "Server blocked empty POST")
    else:
        reporter.add("Q_EMPTY", "FAIL", f"{r.status_code}")
