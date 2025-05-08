import sys
import os
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QFileDialog, QVBoxLayout, QLabel,
    QLineEdit, QMessageBox, QHBoxLayout
)
from logic.repo_actions import clone_repo, clean_repo, push_repo

class GitScrubGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GitScrub - Secret Remover")
        self.setMinimumWidth(500)

        # --- Fields ---
        self.repo_url_input = QLineEdit()
        self.repo_url_input.setPlaceholderText("Enter GitHub repo URL (https://...)")

        self.dest_folder_button = QPushButton("Select Clone Destination")
        self.work_dir_input = QLineEdit()
        self.work_dir_input.setPlaceholderText("Optional: Work directory name if selected folder not empty")

        self.clone_button = QPushButton("Clone Repo (Mirror)")
        self.clone_button.setEnabled(False)

        self.pattern_button = QPushButton("Select Pattern File")
        self.pattern_button.setEnabled(False)

        self.run_button = QPushButton("Run Cleanup")
        self.run_button.setEnabled(False)

        self.push_button = QPushButton("Push Cleaned Repo")
        self.push_button.setEnabled(False)

        self.status_label = QLabel("Ready.")

        # --- Event Bindings ---
        self.dest_folder_button.clicked.connect(self.select_clone_destination)
        self.clone_button.clicked.connect(self.clone_repo)
        self.pattern_button.clicked.connect(self.select_pattern_file)
        self.run_button.clicked.connect(self.run_cleanup)
        self.push_button.clicked.connect(self.push_cleaned_repo)

        # --- Internal State ---
        self.clone_path = None
        self.pattern_path = None

        # --- Layout ---
        layout = QVBoxLayout()
        layout.addWidget(QLabel("GitHub Repo URL:"))
        layout.addWidget(self.repo_url_input)
        layout.addWidget(self.dest_folder_button)
        layout.addWidget(self.work_dir_input)
        layout.addWidget(self.clone_button)
        layout.addWidget(self.pattern_button)
        layout.addWidget(self.run_button)
        layout.addWidget(self.push_button)
        layout.addWidget(self.status_label)
        self.setLayout(layout)

    def select_clone_destination(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder to Clone Into")
        if folder:
            if os.listdir(folder):
                subdir = self.work_dir_input.text().strip()
                if not subdir:
                    QMessageBox.warning(self, "Folder Not Empty", "Folder is not empty. Please specify a work directory name.")
                    return
                folder = os.path.join(folder, subdir)
                try:
                    os.makedirs(folder, exist_ok=True)
                except Exception as e:
                    self.status_label.setText(f"❌ Error creating subfolder: {e}")
                    return
            self.clone_path = folder
            self.status_label.setText(f"Selected clone path: {self.clone_path}")
            self.clone_button.setEnabled(True)

    def clone_repo(self):
        url = self.repo_url_input.text().strip()
        if not url or not self.clone_path:
            self.status_label.setText("❌ Please provide both GitHub repo URL and clone path.")
            return
        self.status_label.setText("&#x1f504; Cloning repository...")
        try:
            success, msg = clone_repo(url, self.clone_path)
            self.status_label.setText(msg)
            if success:
                self.clone_button.setEnabled(False)
                self.pattern_button.setEnabled(True)
        except Exception as e:
            self.status_label.setText(f"❌ Clone failed: {e}")

    def select_pattern_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Pattern File", "", "Text Files (*.txt)")
        if path:
            self.pattern_path = path
            self.status_label.setText(f"Selected pattern file: {path}")
            self.run_button.setEnabled(True)

    def run_cleanup(self):
        if not self.clone_path or not self.pattern_path:
            self.status_label.setText("❌ Please clone the repo and select pattern file first.")
            return
        self.status_label.setText("&#x1f9f9; Running cleanup...")
        try:
            success, msg = clean_repo(self.clone_path, self.pattern_path)
            self.status_label.setText(msg)
            if success:
                self.push_button.setEnabled(True)
        except Exception as e:
            self.status_label.setText(f"❌ Cleanup failed: {e}")

    def push_cleaned_repo(self):
        if not self.clone_path:
            self.status_label.setText("❌ Repo not cloned.")
            return
        self.status_label.setText("&#x1f680; Pushing cleaned repo...")
        try:
            success, msg = push_repo(self.clone_path, self.repo_url_input.text().strip())
            self.status_label.setText(msg)
        except Exception as e:
            self.status_label.setText(f"❌ Push failed: {e}")


if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = GitScrubGUI()
    window.show()
    sys.exit(app.exec())
