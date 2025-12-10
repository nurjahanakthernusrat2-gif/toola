def ok(v): return {"status": "PASS", "details": v}
def fail(v): return {"status": "FAIL", "details": v}

SQLI_PAYLOAD = "' OR 1=1 --"
XSS_PAYLOAD = "<script>alert(1)</script>"
SPECIAL_CHARS = "!@#$%^&*()_+=-{}[];:'\",.<>/?"
