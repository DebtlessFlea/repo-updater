import os
import requests
import zipfile
import tempfile
import shutil
import filecmp

GITHUB_USER = "debtlessflea"
REPO_NAME = "DebtlessFlea.github.io"
BRANCH = "main"

def move_current_to_old():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    old_dir = os.path.join(current_dir, ".old")
    os.makedirs(old_dir, exist_ok=True)

    for item in os.listdir(current_dir):
        if item in [".old", os.path.basename(__file__)]:
            continue
        src_path = os.path.join(current_dir, item)
        dst_path = os.path.join(old_dir, item)
        shutil.move(src_path, dst_path)
    print("Moved current files to .old")

def delete_old_folder():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    old_dir = os.path.join(current_dir, ".old")
    if os.path.exists(old_dir):
        shutil.rmtree(old_dir)
        print("Deleted .old folder")

def download_repo_zip():
    url = f"https://github.com/{GITHUB_USER}/{REPO_NAME}/archive/refs/heads/{BRANCH}.zip"
    response = requests.get(url)
    if response.status_code == 200:
        temp_zip = tempfile.NamedTemporaryFile(delete=False, suffix=".zip")
        temp_zip.write(response.content)
        temp_zip.close()
        return temp_zip.name
    else:
        raise Exception("Failed to download GitHub repo")

def extract_zip(zip_path):
    temp_dir = tempfile.mkdtemp()
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)
    return os.path.join(temp_dir, f"{REPO_NAME}-{BRANCH}")

def files_differ(src, dst):
    return not os.path.exists(dst) or not filecmp.cmp(src, dst, shallow=False)

def copy_updated_files(src_dir, dst_dir):
    for root, dirs, files in os.walk(src_dir):
        rel_path = os.path.relpath(root, src_dir)
        target_root = os.path.join(dst_dir, rel_path)
        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(target_root, file)
            if files_differ(src_file, dst_file):
                os.makedirs(target_root, exist_ok=True)
                shutil.copy2(src_file, dst_file)
                print(f"Updated: {os.path.relpath(dst_file, dst_dir)}")

def main():
    print("Moving current files to .old...")
    move_current_to_old()

    print("Checking for updates from GitHub...")
    zip_path = download_repo_zip()
    repo_dir = extract_zip(zip_path)
    local_dir = os.path.dirname(os.path.abspath(__file__))
    copy_updated_files(repo_dir, local_dir)

    os.remove(zip_path)
    shutil.rmtree(os.path.dirname(repo_dir))

    print("Deleting .old folder...")
    delete_old_folder()

    print("Update complete.")

if __name__ == "__main__":
    main()
