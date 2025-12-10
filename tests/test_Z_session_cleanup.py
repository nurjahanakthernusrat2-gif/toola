def run(client, reporter):
    before = dict(client.session.cookies)

    client.get("/logout")
    after = dict(client.session.cookies)

    if before == after:
        reporter.add("Z_SESSION_CLEANUP", "FAIL", "Session not cleared")
    else:
        reporter.add("Z_SESSION_CLEANUP", "PASS", "Session cleared")
