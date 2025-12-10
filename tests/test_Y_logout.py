def run(client, reporter):
    r = client.get("/logout")
    if r.status_code in [200, 302]:
        reporter.add("Y_LOGOUT", "PASS", "Logout functional")
    else:
        reporter.add("Y_LOGOUT", "FAIL", f"{r.status_code}")
