import os
import sys
import shutil
import stat

REPO_ROOT = os.getcwd()
GIT_DIR = os.path.join(REPO_ROOT, ".git")
HOOKS_DIR = os.path.join(GIT_DIR, "hooks")
PRE_COMMIT_PATH = os.path.join(HOOKS_DIR, "pre-commit")
SOURCE_SCRIPT = os.path.join(REPO_ROOT, "git_sentinel.py")

SHEBANG = "#!/usr/bin/env python\n\n"


def fail(message):
    print(f"[Git-Sentinel] ERROR: {message}")
    sys.exit(1)


def main():
    # 1. Verify Git repository
    if not os.path.isdir(GIT_DIR):
        fail("This directory is not a Git repository (.git not found).")

    # 2. Verify source script exists
    if not os.path.isfile(SOURCE_SCRIPT):
        fail("git_sentinel.py not found in repository root.")

    # 3. Ensure hooks directory exists
    os.makedirs(HOOKS_DIR, exist_ok=True)

    # 4. Prevent silent overwrite
    if os.path.exists(PRE_COMMIT_PATH):
        print("[Git-Sentinel] A pre-commit hook already exists.")
        choice = input("Overwrite existing hook? (y/N): ").strip().lower()
        if choice != "y":
            print("[Git-Sentinel] Installation aborted.")
            sys.exit(0)

    # 5. Read scanner source
    with open(SOURCE_SCRIPT, "r", encoding="utf-8") as f:
        script_content = f.read()

    # 6. Write pre-commit hook with shebang
    with open(PRE_COMMIT_PATH, "w", encoding="utf-8") as f:
        f.write(SHEBANG)
        f.write(script_content)

    # 7. Make executable (important for Git Bash / Unix)
    st = os.stat(PRE_COMMIT_PATH)
    os.chmod(PRE_COMMIT_PATH, st.st_mode | stat.S_IEXEC)

    print("\n[Git-Sentinel] Installation successful.")
    print("Pre-commit hook installed at:")
    print(f"  {PRE_COMMIT_PATH}\n")
    print("Git-Sentinel is now protecting this repository.")


if __name__ == "__main__":
    main()
