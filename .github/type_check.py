from pathlib import Path
import subprocess

config = Path(__file__).parent / "ruff.toml"

command = ("ruff", "--config", str(config), "check")
print(" ".join(command))

try:
    result = subprocess.run(command)
except FileNotFoundError as e:
    print(f"{e} - Is ruff installed?")
    exit(1)

exit(result.returncode)
