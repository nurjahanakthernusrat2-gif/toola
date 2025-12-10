def run(client, reporter):
    r = client.get("/login")

    cookies = client.session.cookies

    issues = []
    for c in cookies:
        if not c.get("secure"):
            issues.append(f"{c.name}: missing Secure")
        if "httponly" not in str(c._rest).lower():
            issues.append(f"{c.name}: missing HttpOnly")

    if issues:
        reporter.add("K_COOKIE_SECURITY", "FAIL", issues)
    else:
        reporter.add("K_COOKIE_SECURITY", "PASS", "All cookies secure")
