import os
import json
import datetime
import subprocess

RESULT_FILE = "reports/results.json"

def run_tests():
    print("[+] Running authentication test suite")

    # ensure reports folder
    os.makedirs("reports", exist_ok=True)

    result = subprocess.run(
        ["pytest", "toola/tests", "-q", "--disable-warnings", "-s", "--maxfail=1"],
        capture_output=True,
        text=True
    )

    print(result.stdout)

    tests_output = {
        "generated": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        "tests": []
    }

    # Read temporary test outputs from each test file
    if os.path.exists("reports/tmp"):
        for f in os.listdir("reports/tmp"):
            if f.endswith(".json"):
                with open(f"reports/tmp/{f}", "r") as fp:
                    tests_output["tests"].append(json.load(fp))

    # Save final results.json
    with open(RESULT_FILE, "w") as fp:
        json.dump(tests_output, fp, indent=4)

    print(f"[+] Saved results to {RESULT_FILE}")


if __name__ == "__main__":
    run_tests()
