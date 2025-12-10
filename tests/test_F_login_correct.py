from core.detector import Detector

def run(client, reporter):
    USER = "admin@phpreaction.com"
    PASS = "admin123"

    login = client.get("/login")
    d = Detector(login.text)
    form = d.find_login_form()
    fields = d.extract_fields(form)

    fields = {k: (USER if "mail" in k else v) for k, v in fields.items()}
    fields = {k: (PASS if "pass" in k else v) for k, v in fields.items()}

    r = client.post("/login", data=fields)

    if r.status_code in [302, 200]:
        reporter.add("F_LOGIN_OK", "PASS", "Login accepted")
    else:
        reporter.add("F_LOGIN_OK", "FAIL", f"Unexpected {r.status_code}")
