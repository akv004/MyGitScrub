from setuptools import setup

APP = ['githubscrub_gui.py']
DATA_FILES = ['resources/patterns.txt']  # You can add more if needed
OPTIONS = {
    'argv_emulation': False,  # ← disable to avoid Carbon
    'packages': ['PySide6'],
    'includes': [
        'PySide6.QtWidgets',
        'PySide6.QtCore',
        'PySide6.QtGui',
    ],
    'iconfile': 'resources/icon.icns',
}

setup(
    app=APP,
    name='GitScrub',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
