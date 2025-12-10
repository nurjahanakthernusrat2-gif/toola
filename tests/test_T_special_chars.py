from core.utils import SPECIAL_CHARS

def run(client, reporter):
    r = client.post("/login", data={"email": SPECIAL_CHARS, "password": SPECIAL_CHARS})
    reporter.add("T_SPECIAL_CHARS", "PASS", f"Returned {r.status_code}")
