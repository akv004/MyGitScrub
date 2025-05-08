import subprocess
import os


def clone_repo(repo_url: str, clone_path: str) -> tuple[bool, str]:
    try:
        if not os.path.exists(clone_path):
            os.makedirs(clone_path)
        command = ["git", "clone", "--mirror", repo_url, clone_path]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return True, f"✅ Clone successful: {clone_path}"
    except subprocess.CalledProcessError as e:
        return False, f"❌ Clone failed: {e.stderr.strip()}"
    except Exception as ex:
        return False, f"❌ Unexpected error during clone: {str(ex)}"

def clean_repo(clone_path: str, pattern_file: str) -> tuple[bool, str]:
    try:
        if not os.path.exists(os.path.join(clone_path, "config")):
            return False, "❌ Not a valid mirror repo. Missing 'config' file."
        command = ["git", "-C", clone_path, "filter-repo", "--replace-text", pattern_file]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return True, "✅ Cleanup completed."
    except subprocess.CalledProcessError as e:
        return False, f"❌ Cleanup failed: {e.stderr.strip()}"
    except Exception as ex:
        return False, f"❌ Unexpected error during cleanup: {str(ex)}"

def push_repo(clone_path: str, repo_url: str) -> tuple[bool, str]:
    try:
        # Check if 'origin' exists, add it if not
        subprocess.run(
            ["git", "-C", clone_path, "remote", "add", "origin", repo_url],
            capture_output=True, text=True, check=False
        )

        # Update the remote URL
        subprocess.run(
            ["git", "-C", clone_path, "remote", "set-url", "origin", repo_url],
            capture_output=True, text=True, check=True
        )

        # Push all branches and tags
        commands = [
            ["git", "-C", clone_path, "push", "--force", "--all"],
            ["git", "-C", clone_path, "push", "--force", "--tags"],
        ]

        for cmd in commands:
            subprocess.run(cmd, capture_output=True, text=True, check=True)

        return True, "✅ Repo pushed successfully."
    except subprocess.CalledProcessError as e:
        return False, f"❌ Push failed: {e.stderr.strip()}"
    except Exception as ex:
        return False, f"❌ Unexpected error during push: {str(ex)}"