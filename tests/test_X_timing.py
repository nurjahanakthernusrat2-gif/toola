import time

def run(client, reporter):
    s = time.time()
    client.post("/login", data={"email": "a", "password": "b"})
    t1 = time.time() - s

    s = time.time()
    client.post("/login", data={"email": "invalid", "password": "wrong"})
    t2 = time.time() - s

    diff = abs(t1 - t2)

    if diff < 0.2:
        reporter.add("X_TIMING", "PASS", "Timing consistent")
    else:
        reporter.add("X_TIMING", "FAIL", f"Timing leak Δ={diff:.2f}s")
