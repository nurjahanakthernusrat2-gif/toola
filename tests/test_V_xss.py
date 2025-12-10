from core.utils import XSS_PAYLOAD

def run(client, reporter):
    r = client.post("/login", data={"email": XSS_PAYLOAD, "password": XSS_PAYLOAD})
    if XSS_PAYLOAD in r.text:
        reporter.add("V_XSS", "FAIL", "Payload reflected")
    else:
        reporter.add("V_XSS", "PASS", "No XSS detected")
