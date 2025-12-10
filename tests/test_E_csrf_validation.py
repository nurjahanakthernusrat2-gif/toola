from core.detector import Detector

def run(client, reporter):
    page = client.get("/login")
    d = Detector(page.text)
    form = d.find_login_form()
    csrf = d.detect_csrf(form)

    fields = d.extract_fields(form)
    if csrf:
        fields[csrf] = "INVALID"

    r = client.post("/login", data=fields)

    if r.status_code in [400, 403]:
        reporter.add("E_CSRF_VALIDATION", "PASS", "Rejected invalid token")
    else:
        reporter.add("E_CSRF_VALIDATION", "FAIL", f"Accepted invalid CSRF ({r.status_code})")
