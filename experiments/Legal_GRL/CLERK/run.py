from pathlib import Path
import subprocess
import sys
import os

# Adds path to 'dsl' code
root_dir = Path(__file__).resolve().parents[3]

# Ensure clerk.py exists
clerk_script = Path(__file__).resolve().parent / "clerk.py"
if not clerk_script.exists():
    raise FileNotFoundError(f"{clerk_script} does not exist!")

env = os.environ.copy()
existing_path = env.get("PYTHONPATH", "")
env["PYTHONPATH"] = f"{root_dir}{os.pathsep}{existing_path}" if existing_path else str(root_dir)

# Runs clerk.py
subprocess.run(
    [sys.executable, str(clerk_script)],
    env=env,
    check=True
)
