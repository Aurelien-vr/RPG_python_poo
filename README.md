# Mailbox TUI — Windows Quick Start

Very small guide to get the app running on Windows.

1) Install Python (choose one)

- Using winget (Windows 10/11):
  winget install --id=Python.Python.3 -e

- Or using Chocolatey:
  choco install python

- Or download & run the installer:
  https://www.python.org/downloads/windows
  (choose "Add Python to PATH" during install)

2) Open a terminal (Windows Terminal, PowerShell or cmd) and create a virtual environment
- Create venv:
  `python -m venv .venv`

3) Activate the venv
- PowerShell:
  `.\.venv\Scripts\Activate.ps1`

- cmd.exe:
  `.venv\Scripts\activate.bat`

(If activation is blocked in PowerShell, you can run the venv python directly:
   ```
   .venv\Scripts\python -m pip install --upgrade pip
  .venv\Scripts\python main.py
  ```
)

4) Upgrade pip (optional but recommended)
   ```
   python -m pip install --upgrade pip
   ```
  

6) Install dependencies one by one with pip
   ```
   pip install textual
   pip install pyfiglet
   ```

(pyfiglet is optional — if omitted the app will use a plain text banner)

6) Run the app
  `python main.py`

That's it — the TUI should open in your terminal. If you run into terminal rendering issues, try Windows Terminal or PowerShell 7+ for best results.
