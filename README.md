# UNMbooking

UNMbooking is a small desktop helper for the University of Nottingham Malaysia sport booking flow.

It opens the booking site with Playwright, lets the user choose account, court, date, and time from a simple GUI, and then fills most of the booking form automatically.

## What this project does

- Opens the UNM sport complex booking page
- Logs in with credentials from `.env` if the login page appears
- Opens `Other Facilities Online`
- Goes to `Booking Request` -> `New Booking`
- Lets the user choose:
  - account
  - facility
  - booking date
  - check-in time
  - check-out time
  - purpose
- Fills the booking form
- Optionally clicks `Complete` automatically

## Project files

- `main.py`: main application
- `requirements.txt`: Python dependencies
- `.env.example`: sample environment file
- `.env`: local secrets file with real account details
- `picklocator.txt`: locator notes collected during development

## Requirements

- Windows or macOS
- Python 3.11 or newer
- Internet access

## Important notes

- Use your own school account and follow school booking rules.
- Do not commit `.env`.
- The current recommended way to use this project is still `python main.py`.
- Packaging into `.exe` or `.app` is possible later, but source-based usage is simpler and more stable.

## Project root

In this README, `project root` means the folder that contains:

```text
main.py
requirements.txt
README.md
```

The folder name can be `UNMbooking`, but the instructions below do not depend on a fixed absolute path.

## Windows setup

1. Install Python

   Download Python 3.11 or newer from:

   ```text
   https://www.python.org/downloads/
   ```

   During installation, enable:

   ```text
   Add python.exe to PATH
   ```

2. Open a terminal in the project root

   The easiest way is:

   - open the project root in File Explorer
   - right-click inside the folder
   - open PowerShell or Terminal there

   Or use:

   ```powershell
   cd path\to\UNMbooking
   ```

3. Create a virtual environment

   ```powershell
   py -3.11 -m venv .venv
   ```

4. Activate the virtual environment

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks script execution, run this once:

   ```powershell
   Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
   ```

   Then activate `.venv` again.

5. Install dependencies

   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

6. Install Playwright Chromium

   ```powershell
   python -m playwright install chromium
   ```

7. Create your `.env`

   ```powershell
   Copy-Item .env.example .env
   ```

8. Edit `.env`

   ```powershell
   notepad .env
   ```

9. Run the app

   ```powershell
   python main.py
   ```

## macOS setup

1. Install Python 3.11 or newer

   Download it from:

   ```text
   https://www.python.org/downloads/macos/
   ```

2. Open Terminal in the project root

   Example:

   ```bash
   cd /path/to/UNMbooking
   ```

3. Create a virtual environment

   ```bash
   python3 -m venv .venv
   ```

4. Activate the virtual environment

   ```bash
   source .venv/bin/activate
   ```

5. Install dependencies

   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

6. Install Playwright Chromium

   ```bash
   python -m playwright install chromium
   ```

7. Create your `.env`

   ```bash
   cp .env.example .env
   ```

8. Edit `.env` with any text editor

9. Run the app

   ```bash
   python main.py
   ```

## Sample `.env`

Copy `.env.example` to `.env`, then replace all placeholder values with your own account details.

Single-account example:

```dotenv
ACCOUNT_IDS=MAIN

MAIN_LABEL=My Account
MAIN_USERNAME=your_nottingham_username
MAIN_PASSWORD=your_password
MAIN_CONTACT_NO=your_phone_number
MAIN_FULL_NAME=Your Full Name
```

Multi-account example:

```dotenv
ACCOUNT_IDS=MAIN,FRIEND

MAIN_LABEL=My Account
MAIN_USERNAME=your_nottingham_username
MAIN_PASSWORD=your_password
MAIN_CONTACT_NO=your_phone_number
MAIN_FULL_NAME=Your Full Name

FRIEND_LABEL=Friend Account
FRIEND_USERNAME=friends_nottingham_username
FRIEND_PASSWORD=friends_password
FRIEND_CONTACT_NO=friends_phone_number
FRIEND_FULL_NAME=Friend Full Name
```

## `.env` field reference

- `ACCOUNT_IDS`: comma-separated list of account IDs
- `LABEL`: display name shown in the GUI
- `USERNAME`: Nottingham username, without `@nottingham.edu.my`
- `PASSWORD`: login password
- `CONTACT_NO`: contact number used in the booking form
- `FULL_NAME`: stored in config for account metadata

If `ACCOUNT_IDS=MAIN,FRIEND`, then the file must include both `MAIN_...` and `FRIEND_...` variables.

## How to use the GUI

When you run `python main.py`, the app opens a small configuration window first.

1. `Account`: choose the account
2. `Facility`: choose the badminton court
3. `Booking Date`: choose the date from the date picker
4. `Check-in Time`: choose the start time from the drop-down list
5. `Check-out Time`: choose the end time from the drop-down list
6. `Purpose`: enter the booking purpose
7. `Auto click Complete`:
   - unchecked: pause before clicking `Complete`
   - checked: click `Complete` automatically
8. Click `Start Booking`

Current default values in the GUI:

```text
Booking date: today
Check-in time: 18:01
Check-out time: 20:00
```

## Time options in the GUI

- Check-in times: `07:01` to `21:01`
- Check-out times: `08:00` to `22:00`

If you want to change those ranges later, edit the time option constants near the top of `main.py`.

## Common issues

### `Missing ACCOUNT_IDS in .env`

`.env` is missing, empty, or not located in the project root.

Make sure the project root contains:

```text
.env
```

and that the file has at least:

```dotenv
ACCOUNT_IDS=MAIN
MAIN_USERNAME=your_nottingham_username
MAIN_PASSWORD=your_password
```

### `ModuleNotFoundError`

The virtual environment is not activated, or dependencies were not installed correctly.

Run:

```powershell
pip install -r requirements.txt
```

or on macOS:

```bash
pip install -r requirements.txt
```

### Playwright cannot find Chromium

Install it again:

```powershell
python -m playwright install chromium
```

or on macOS:

```bash
python -m playwright install chromium
```

### The page structure changes

This script depends on the current labels and structure of the booking website. If the site changes, some locators in `main.py` may need to be updated.

### The flow pauses before `Complete`

This is expected when `Auto click Complete` is not checked.

## Packaging later

Packaging is possible, but it is not the primary setup path for this repository.

### Windows `.exe`

In the project root:

```powershell
.\.venv\Scripts\python.exe -m pip install pyinstaller
$env:PLAYWRIGHT_BROWSERS_PATH="0"
.\.venv\Scripts\python.exe -m playwright install chromium
.\.venv\Scripts\pyinstaller.exe --noconfirm --onedir --windowed --name UNMBooking main.py
```

Typical output:

```text
dist\UNMBooking\UNMBooking.exe
```

### macOS `.app`

On macOS, package on a Mac:

```bash
python -m pip install pyinstaller
PLAYWRIGHT_BROWSERS_PATH=0 python -m playwright install chromium
pyinstaller --noconfirm --onedir --windowed --name UNMBooking main.py
```

Typical output:

```text
dist/UNMBooking.app
```

### Packaging caveat

The current code uses `load_dotenv()` and relies on the runtime working directory. That is fine for normal source-based usage from the project root.

If you later want a double-clickable packaged app that always finds `.env` next to the executable, `main.py` should be adjusted to resolve the config file relative to the executable or script location.
