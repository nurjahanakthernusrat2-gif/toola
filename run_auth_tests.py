import os
from core.http_client import HTTPClient
from core.reporter import Reporter
from core.detector import Detector

import importlib

def main():
    BASE_URL = os.getenv("TARGET_URL")
    if not BASE_URL:
        print("TARGET_URL missing")
        return

    print(f"[+] Running tests on: {BASE_URL}")

    client = HTTPClient(BASE_URL)
    reporter = Reporter()

    # load test modules dynamically
    for f in os.listdir("tests"):
        if f.startswith("test_") and f.endswith(".py"):
            module_name = f"tests.{f[:-3]}"
            mod = importlib.import_module(module_name)
            print(f"  → Running {module_name}")
            mod.run(client, reporter)

    # save reports
    reporter.save_json()
    reporter.save_html()
    print("[+] Report generated!")

if __name__ == "__main__":
    main()
