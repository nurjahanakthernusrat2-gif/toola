from core.detector import Detector

def run(client, reporter):
    page = client.get("/login")
    d = Detector(page.text)

    form = d.find_login_form()
    fields = d.extract_fields(form)

    for k in fields:
        if "pass" in k: fields[k] = "WRONGPASS"
        if "mail" in k: fields[k] = "wrong@example.com"

    r = client.post("/login", data=fields)

    if r.status_code in [200, 401, 403]:
        reporter.add("G_LOGIN_WRONG", "PASS", "Rejected wrong creds")
    else:
        reporter.add("G_LOGIN_WRONG", "FAIL", f"Code {r.status_code}")
