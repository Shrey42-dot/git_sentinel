# Git-Sentinel 🔐 

[![Python 3.x](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)](#)

**Git-Sentinel** is a lightweight, pre-commit security scanner designed to prevent developers from accidentally leaking secrets—such as API keys, passwords, and tokens—into Git repositories.

By intercepting the `git commit` process, it scans only **staged changes**, acting as a silent security guard in your local development workflow before data ever leaves your machine.

---

## 🚀 Why Git-Sentinel?

Accidentally committing secrets is one of the most common and costly mistakes in modern software engineering. Git-Sentinel is built to solve this specifically for environments where heavy enterprise tools might be overkill or difficult to configure.

* **Zero Noise:** Scans only `git diff --cached` so you aren't nagged about old legacy code.
* **Dev-Friendly:** Provides clear, actionable warnings when a commit is blocked.
* **Built for Reality:** Works seamlessly across **Windows (Git Bash/VS Code)** and **CI/CD pipelines** where interactive prompts often fail.

---

## ✨ Key Features

* 🔍 **Smart Scanning:** Only inspects files currently in the staging area.
* 🧠 **Regex Detection:** Pre-configured for high-risk patterns (AWS, Stripe, Generic Auth).
* 🚫 **Hard Block:** Automatically aborts the commit process if a secret is found.
* 🔓 **Explicit Bypass:** Environment-variable based bypass for intentional commits (CI-safe).
* 🛠 **One-Step Setup:** Simple installation script to hook into any repository.

---

## 🧪 Detected Secret Types

Git-Sentinel is intentionally conservative to minimize false positives while catching the most critical leaks:

| Secret Type | Detection Pattern |
| :--- | :--- |
| **AWS Access Keys** | `AKIA...` prefixes |
| **Stripe Live Keys** | `sk_live_...` prefixes |
| **Generic Secrets** | `api_key`, `token`, `password` assignments |
| **Private Keys** | Headers like `-----BEGIN RSA PRIVATE KEY-----` |

---

## 📦 Installation

### Prerequisites
* Python 3.6+
* Git installed and initialized in your project

### Setup
Clone your repository and run the installer from the root directory:
      
      python install.py

This command installs Git-Sentinel as a local hook in .git/hooks/pre-commit.


---

## 🔒 How It Works
1. The Trigger: You run git commit -m "feat: add auth logic".

2. The Scan: Git-Sentinel intercepts the command and runs a regex scan on the staged changes.

3. The Verdict:

    * ✅ Clean: The commit proceeds normally.

    * ❌ Secret Found: The commit is blocked, and a report of the offending files/lines is displayed.


--- 

## 🔓 Intentional Bypass
In rare scenarios (e.g., using dummy tokens for testing), you may need to bypass the scanner. Git-Sentinel requires an explicit intent to ensure no secrets are leaked by accident:

    
    # Windows (CMD/PowerShell) or Linux/macOS
    GIT_SENTINEL_BYPASS=I_UNDERSTAND_THE_RISK git commit -m "your message"

[!NOTE]

This bypass method is designed to be non-interactive, making it compatible with automated CI/CD environments.

---

## ⚠️ Security Disclaimer
Git-Sentinel is a preventive safety tool. It is not a replacement for:

  1. Secret Rotation: If a secret is committed, it is compromised. Rotate it immediately.
  
  2. Secret Managers: Use Vault, AWS Secrets Manager, or .env files (added to .gitignore).
  
  3. Server-Side Scanning: Always use GitHub Secret Scanning or similar tools as a second line of defense.

--- 

## 📄 License
Distributed under the MIT License. See LICENSE for more information.

---

Built by [Shrey42-dot] Focused on Practical DevSecOps & Secure SDLC.


    ### Understanding the Hook Lifecycle
    To help visualize where Git-Sentinel sits in your development process, it functions as a gateway between your local code changes and the Git history:
    
    
    
    This ensures that the "Secret Found" state triggers a `sys.exit(1)`, which Git interprets as a failure, thereby stopping the commit before it ever gets a commit hash.
    
    **Would you like me to help you write the `install.py` script to automate the hook placement, or perhaps refine the Python regex logic for the scanner itself?**
