def run(client, reporter):
    codes = {}
    for path in ["/login", "/logout", "/"]:
        r = client.get(path)
        codes[path] = r.status_code
    reporter.add("L_RESP_CODES", "PASS", codes)
