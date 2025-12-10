def run(client, reporter):
    r = client.get("/login")

    if r.is_redirect:
        reporter.add("J_REDIRECT", "PASS", f"Redirect → {r.headers.get('Location')}")
    else:
        reporter.add("J_REDIRECT", "PASS", "No redirect (normal)")
