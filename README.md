# SystemID_and_BIN_Parse
## Setup

Install the Python dependencies:

```bash
python -m pip install -r requirements.txt
```

`Scripts/ParseBin.py` also installs them automatically the first time it is run directly.

## Usage

```bash
python Scripts/ParseBin.py <log.BIN> ATT IMU
```

```python
from ParseBin import parse_bin
att, imu = parse_bin("00000020.BIN", ["ATT", "IMU"])
```

## Flight logs

`.BIN` logs are stored with [Git LFS](https://git-lfs.com). Run `git lfs install` once before cloning to download them.
