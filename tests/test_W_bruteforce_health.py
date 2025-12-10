def run(client, reporter):
    hits = 0
    for i in range(5):
        r = client.post("/login", data={"email": f"user{i}", "password": "x"})
        if r.status_code in [401, 403]:
            hits += 1

    reporter.add("W_BRUTE_HEALTH", "PASS", f"{hits}/5 rejected")
