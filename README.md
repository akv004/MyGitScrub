# 🧼 GitScrub — Secure Your Git History

**GitScrub** is a lightweight desktop app for macOS that helps developers permanently remove sensitive data from their Git repositories using a clean graphical interface.

Built with [PySide6](https://doc.qt.io/qtforpython/) and powered by [git-filter-repo](https://github.com/newren/git-filter-repo), GitScrub makes it easy to scrub API keys, secrets, tokens, and credentials from Git history — no command-line required.

---

## 🚀 Features

- 🔗 **Clone GitHub repositories** in mirror mode
- 📁 **Select or reuse** existing local cloned mirrors
- 🧹 **Run cleanup** using pattern files (`literal:` and `regex:` support)
- 🧪 **Copyable logs** with error details for debugging
- 📄 **Help panel** with documentation and usage examples
- 🧠 No Python or Git knowledge required

---

## 🖥️ Installation (macOS)

1. Clone the repo:
   ```bash
   git clone https://github.com/your-username/GitScrub.git
   cd GitScrub
   ```
2.	Create a virtual environment:
   ```bash
      python3 -m venv .venv
      source .venv/bin/activate
      pip install -r requirements.txt
    ```
3. Build the standalone.app
   ```bash
   python setup.py py2app
   open dist/GitScrub.app
   ```
4. Pattern File Format (patterns.txt)
   ```txt
   # Literal match (entire string will be replaced with ***)
literal:$http.defaults.headers.common.Authorization = 'Basic Ymasdfasd';

# Regex match (supports replacement)
regex:api\s*=\s*['\"]?[a-zA-Z0-9]+['\"]? ==>> api = "REDACTED"
```
