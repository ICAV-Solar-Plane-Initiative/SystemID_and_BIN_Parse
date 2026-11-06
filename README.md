# SystemID_and_BIN_Parse

Tools for parsing ArduPilot DataFlash `.BIN` flight logs for system identification.

## Requirements

- Python 3.10 or newer
- [Git LFS](https://git-lfs.com), for the sample flight logs

## Setup

Clone the repo, then create the project virtual environment (`.venv`) and install the dependencies. You only need to do this once.

**PowerShell (Windows):**

```powershell
git lfs install
git clone https://github.com/ICAV-Solar-Plane-Initiative/SystemID_and_BIN_Parse.git
cd SystemID_and_BIN_Parse
.\setup_env.ps1
```

If PowerShell blocks the script, run `powershell -ExecutionPolicy Bypass -File .\setup_env.ps1` instead.

**Git Bash / macOS / Linux:**

```bash
./setup_env.sh
```

To use a specific Python, pass it in: `.\setup_env.ps1 -Python "C:\path\to\python.exe"` or `PYTHON=python3.13 ./setup_env.sh`.

### Activating the environment

| Shell      | Command                         |
|------------|---------------------------------|
| PowerShell | `.venv\Scripts\Activate.ps1`    |
| Git Bash   | `source .venv/Scripts/activate` |
| macOS/Linux| `source .venv/bin/activate`     |

**VS Code** picks up `.venv` automatically via `.vscode/settings.json`. If it doesn't, open the Command Palette and run **Python: Select Interpreter**, then choose `.venv`.

### Adding a dependency

Add it to `requirements.txt`, then re-run the setup script.

## Usage

From the command line (with `.venv` active):

```bash
python Scripts/ParseBin.py "Exmples/FMS Plane/Sample Flight Data (FMS Plane)/00000020.BIN" ATT IMU
```

From Python:

```python
from ParseBin import parse_bin

att, imu = parse_bin("00000020.BIN", ["ATT", "IMU"])
att["Roll"]     # numpy array
imu[0]["GyrX"]  # first IMU instance
```

Single-instance messages return a dict of numpy arrays, one per field, plus `Time` in seconds. Multi-instance messages (IMU, BARO, GPS, XKF1, ...) return a list of these, ordered by instance. Messages not present in the log return `None`.

## Flight logs

Sample `.BIN` logs are in `Exmples/` and are stored with Git LFS. If you cloned before installing Git LFS, run `git lfs install` then `git lfs pull` to download them.
