from core.detector import Detector

def run(client, reporter):
    r = client.get("/login")
    d = Detector(r.text)
    form = d.find_login_form()

    csrf = d.detect_csrf(form)
    if csrf:
        reporter.add("D_CSRF_PRESENT", "PASS", csrf)
    else:
        reporter.add("D_CSRF_PRESENT", "FAIL", "CSRF token missing")
