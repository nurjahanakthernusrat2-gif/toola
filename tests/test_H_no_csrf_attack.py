from core.detector import Detector

def run(client, reporter):
    page = client.get("/login")
    d = Detector(page.text)

    form = d.find_login_form()
    fields = d.extract_fields(form)

    # Remove CSRF
    for k in list(fields.keys()):
        if "csrf" in k.lower():
            del fields[k]

    r = client.post("/login", data=fields)

    if r.status_code in [400, 403]:
        reporter.add("H_NO_CSRF", "PASS", "Blocked missing CSRF")
    else:
        reporter.add("H_NO_CSRF", "FAIL", f"Accepted missing CSRF ({r.status_code})")
