def run(client, reporter):
    r = client.get("/login")
    if r.status_code not in [200, 302]:
        reporter.add("A_BASIC", "FAIL", f"Login page returned {r.status_code}")
        return

    from core.detector import Detector
    d = Detector(r.text)

    form = d.find_login_form()
    if not form:
        reporter.add("A_BASIC", "FAIL", "Login form not detected")
        return

    fields = d.extract_fields(form)
    csrf = d.detect_csrf(form)

    reporter.add("A_BASIC", "PASS", {
        "fields": list(fields.keys()),
        "csrf_token": csrf
    })
