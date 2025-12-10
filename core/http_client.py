import requests

class HTTPClient:
    def __init__(self, base_url):
        self.base = base_url
        self.session = requests.Session()

    def get(self, url, **kwargs):
        return self.session.get(self.base + url, allow_redirects=False, **kwargs)

    def post(self, url, data=None, headers=None, **kwargs):
        return self.session.post(
            self.base + url,
            data=data,
            headers=headers,
            allow_redirects=False,
            **kwargs
        )

    def custom(self, method, url, **kwargs):
        return self.session.request(
            method=method,
            url=self.base + url,
            allow_redirects=False,
            **kwargs
        )

    def set_cookie(self, name, val):
        self.session.cookies.set(name, val)

    def clear(self):
        self.session.cookies.clear()
