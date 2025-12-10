def run(client, reporter):
    count_403 = 0
    for _ in range(8):
        r = client.post("/login", data={"email": "x", "password": "x"})
        if r.status_code in [403, 429]:
            count_403 += 1

    if count_403 >= 2:
        reporter.add("M_RATE_LIMIT", "PASS", "Rate-limit triggered")
    else:
        reporter.add("M_RATE_LIMIT", "FAIL", "No rate limiting")
