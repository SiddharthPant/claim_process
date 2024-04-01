# Claim Process Assessment

## Setup
```bash
python3.11 -m venv --prompt . --upgrade-deps .venv
source .venv/bin/activate
python -m pip install -U pip setuptools wheel pip-tools
make venv
make up
```
## Add a dependency
Add the package in `pyproject.toml` file and then execute below make commands.
```bash
make requirements.txt
make venv
```

## Makefile commands

<!-- [[[cog
import cog
import subprocess
cog.out(
    "```shell\n" +
    subprocess.check_output(["make", "help"]).decode() +
    "```"
)
]]] -->
```shell
Available make commands:

README.md                  Update dynamic blocks in README.md
fix                        Fix linting errors
fmt                        Format Python code
lint                       Lint Python code
requirements.txt           Generate requirements.txt from pyproject.toml
run                        Stand up the environment
test                       Run tests
venv                       Install dev requirements in virtual env from pyproject.toml
```
<!-- [[[end]]] -->
