> [!WARNING]
> Script does not support repositories with folders in them (working on a fix).

## 📋 Description
**repo-updater** is a Python script that updates/fetches the files by downloading and extracting the latest version of a GitHub repository. It compares each file in the repository with the local version and replaces only the files that have changed or are missing.

## ❓ How to Use

### Prerequisites:
- Windows operating system.
- Python 3.x 

### Steps:

1. Open the `repo-updater.py` file and change GitHub info at the top:
```python
GITHUB_USER = "your_username"
REPO_NAME = "your_repository"
BRANCH = "main"  # or "master" if that's your default branch
```

2. Place both `repo-updater.py` and `run.bat` inside the folder containing the files you want to update.

3. Run the file by double-clicking `run.bat` or by opening terminal and running
```bash
python repo-updater.py
```

## 🌐 Statistics
![Alt](https://repobeats.axiom.co/api/embed/8eb1e488e7418d03f443e817f7bbb31dc39cccca.svg "Repobeats analytics image")
