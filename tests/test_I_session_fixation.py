def run(client, reporter):
    # Set session cookie manually
    client.set_cookie("PHPSESSID", "FAKESESSION123")

    r = client.get("/login")
    
    if "FAKESESSION123" in str(client.session.cookies):
        reporter.add("I_SESSION_FIX", "FAIL", "Server re-used attacker session")
    else:
        reporter.add("I_SESSION_FIX", "PASS", "Server issued new session")
