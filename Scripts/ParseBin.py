"""Read selected message types from an ArduPilot DataFlash .BIN log.

Python port of parseBIN.m. Uses pymavlink to decode the log and numpy to
store each message field as an array.

Each message is returned as a "table": a dict mapping field name to a numpy
array, one entry per logged sample. Every table also has a ``Time`` column,
in seconds since boot (from ``TimeUS``), to match MATLAB's timetable.

Example
-------
    from ParseBin import parse_bin

    att, imu = parse_bin("00000020.BIN", ["ATT", "IMU"])

    plt.plot(att["Time"], att["Roll"], att["Time"], att["DesRoll"])
    imu0 = imu[0]                  # first IMU instance
    plt.plot(imu0["Time"], imu0["GyrX"])

Requires numpy and pymavlink, installed into the project virtual
environment by setup_env.ps1 (Windows) or setup_env.sh (bash).
"""

import importlib.util
import sys
import warnings
from collections import defaultdict

# Packages this script needs (import names, as listed in requirements.txt)
REQUIRED_PACKAGES = ["numpy", "pymavlink"]


def check_dependencies():
    """Stop with a clear message if any required package is missing."""
    missing = [
        name for name in REQUIRED_PACKAGES
        if importlib.util.find_spec(name) is None
    ]
    if not missing:
        return

    in_venv = sys.prefix != sys.base_prefix
    hint = (
        "Install them into this environment with:\n"
        "    python -m pip install -r requirements.txt"
        if in_venv else
        "You are not in the project virtual environment. From the repo root, "
        "run setup_env.ps1 (PowerShell) or setup_env.sh (Git Bash), then "
        "activate .venv or select it as the interpreter in VS Code."
    )
    raise ImportError(
        f"Missing packages: {', '.join(missing)}\n"
        f"Python in use: {sys.executable}\n{hint}"
    )


check_dependencies()

import numpy as np  # noqa: E402  (imported after the dependency check)
from pymavlink import DFReader  # noqa: E402

# A table is {field name: numpy array of that field's values}
Table = dict[str, np.ndarray]


def parse_bin(filename, msg_names):
    """Read selected message types from an ArduPilot .BIN log.

    Parameters
    ----------
    filename : str or Path
        Path to the .BIN log, e.g. "00000020.BIN".
    msg_names : str or list of str
        Message names to read, e.g. ["ATT", "CTUN", "IMU"].

    Returns
    -------
    list, in the same order as msg_names, where each entry is:
        - single-instance message (ATT, CTUN, ...) -> a Table
        - multi-instance message (IMU, BARO, GPS, XKF1, ...) -> a list of
          Tables, one per instance, ordered by instance number
        - message not present in the log -> None
    """
    if isinstance(msg_names, str):
        msg_names = [msg_names]
    msg_names = list(msg_names)

    log = DFReader.DFReader_binary(str(filename))

    # Skip any requested names the log doesn't contain
    available = {fmt.name for fmt in log.formats.values()}
    present = [name for name in msg_names if name in available]
    missing = [name for name in msg_names if name not in available]
    if missing:
        warnings.warn(f"Not in log, skipped: {', '.join(missing)}")
    if not present:
        return [None] * len(msg_names)

    # Decode all requested messages in one pass through the file
    samples = _read_samples(log, present)

    data = []
    for name in msg_names:
        if name not in samples:
            data.append(None)
            continue

        instances = samples[name]
        tables = [_to_table(instances[i]) for i in sorted(instances)]

        if len(tables) == 1:
            data.append(tables[0])
        else:
            data.append(tables)

    return data


def _read_samples(log, msg_names):
    """Collect every sample of the requested messages from the log.

    Returns a nested dict: samples[msg name][instance] -> list of dicts,
    where each dict is one logged sample {field: value}. Messages without
    an instance field are all stored under instance 0.
    """
    samples = defaultdict(lambda: defaultdict(list))

    while True:
        msg = log.recv_match(type=msg_names)
        if msg is None:
            break  # end of file

        fields = msg.to_dict()
        name = fields.pop("mavpackettype")

        # Multi-instance messages say which field holds the instance number
        # (e.g. "I" for IMU, "C" for XKF1); None for single-instance messages
        instance_field = msg.fmt.instance_field
        instance = fields[instance_field] if instance_field else 0

        samples[name][instance].append(fields)

    return samples


def _to_table(rows):
    """Turn a list of samples [{field: value}, ...] into a Table."""
    field_names = rows[0].keys()
    table = {field: np.array([row[field] for row in rows]) for field in field_names}

    if "TimeUS" in table:
        table["Time"] = table["TimeUS"] * 1e-6  # microseconds -> seconds

    return table


if __name__ == "__main__":
    # Quick check from the command line:
    #   python ParseBin.py 00000020.BIN ATT IMU
    if len(sys.argv) < 3:
        sys.exit("Usage: python ParseBin.py <log.BIN> <MSG> [<MSG> ...]")

    log_file, *names = sys.argv[1:]
    for name, result in zip(names, parse_bin(log_file, names)):
        if result is None:
            print(f"{name}: not in log")
            continue
        tables = result if isinstance(result, list) else [result]
        for i, table in enumerate(tables):
            n_samples = len(next(iter(table.values())))
            print(f"{name}[{i}]: {n_samples} samples | {', '.join(table)}")
