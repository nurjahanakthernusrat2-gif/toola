import re
from bs4 import BeautifulSoup

class Detector:
    def __init__(self, html):
        self.html = html
        self.soup = BeautifulSoup(html, "html.parser")

    def find_login_form(self):
        forms = self.soup.find_all("form")
        for f in forms:
            inputs = f.find_all("input")
            names = [i.get("name") for i in inputs]
            if any("pass" in str(n).lower() for n in names):
                return f
        return None

    def extract_fields(self, form):
        inputs = form.find_all("input")
        fields = {}
        for inp in inputs:
            fields[inp.get("name")] = inp.get("value") or ""
        return fields

    def detect_csrf(self, form):
        for inp in form.find_all("input"):
            if "csrf" in str(inp.get("name")).lower():
                return inp.get("name")
        return None
