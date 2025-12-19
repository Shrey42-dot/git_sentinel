import subprocess
import sys
import re
import os

# ==========================
# Secret Detection Patterns
# ==========================
SECRET_PATTERNS = {
    "AWS Access Key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "Stripe Live Key": re.compile(r"sk_live_[0-9a-zA-Z]{24}"),
    "Generic Secret Assignment": re.compile(
        r"(?i)(api_key|secret|token|password)\s*=\s*['\"][^'\"]+['\"]"
    ),
}

# ==========================
# Bypass Configuration
# ==========================
BYPASS_ENV = "GIT_SENTINEL_BYPASS"
BYPASS_CODE = "I_UNDERSTAND_THE_RISK"

# ==========================
# Helpers
# ==========================
def get_staged_diff():
    result = subprocess.run(
        ["git", "diff", "--cached"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return result.stdout


def scan_for_secrets(diff_text):
    findings = []

    for line_number, line in enumerate(diff_text.splitlines(), start=1):
        # Ignore diff metadata
        if line.startswith(("+++", "---", "@@")):
            continue

        for name, pattern in SECRET_PATTERNS.items():
            if pattern.search(line):
                findings.append({
                    "type": name,
                    "line_number": line_number,
                    "content": line.strip()
                })

    return findings


# ==========================
# Main
# ==========================
def main():
    diff = get_staged_diff()

    # No staged changes → allow commit
    if not diff.strip():
        sys.exit(0)

    findings = scan_for_secrets(diff)

    if findings:
        print("\n\033[91m🚨 Git-Sentinel Security Blocker 🚨\033[0m")
        print("Potential secrets detected in staged changes:\n")

        for f in findings:
            print(f" - [{f['type']}] Line {f['line_number']}: {f['content']}")

        # Check bypass via environment variable
        bypass_value = os.environ.get(BYPASS_ENV, "")

        if bypass_value == BYPASS_CODE:
            print("\nBypass accepted via environment variable.")
            print("Proceeding with commit.\n")
            sys.exit(0)

        print("\nCommit aborted.")
        print("To bypass intentionally, run:\n")
        print(f"  {BYPASS_ENV}={BYPASS_CODE} git commit -m \"your message\"\n")
        sys.exit(1)

    # No secrets detected → allow commit
    sys.exit(0)


if __name__ == "__main__":
    main()
