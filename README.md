# Claim Process Assessment

## Setup
```bash
curl -sSL https://install.python-poetry.org | python3 -
poetry install
```
## Add a dependency
```bash
poetry add 'package_name'
```

## Start server
```bash
cp .env.example .env
docker compose up -d --build
# Run the migrations
docker compose exec web alembic upgrade head
```

## Notes
The following features have been implemented:
* Used docker compose and dockerfile for one command standup the environment
* Used SQLModel, Pydantic v2 for typing gallore end to end
* Used Alembic to manage SQL migrations
* Tried to setup async with asyncpg as well but SQLModel is still needs some work for better support
* Tried to support the non-standard api names but SQLModel has an ongoing bug that prevents to use that feature in FastAPI. I have still created a stub class at this link with more details: https://github.com/SiddharthPant/claim_process/blob/01f069eb3de0f7edcf74ee52541d2d69be5bc032/server/models.py#L104
* Used postgres latest version for database
* Used pre-commit-config.yaml for improved developer commit workflow
* Used Poetry to manage prod and dev dependencies
* Used a production ready dir structure for the project that is flexible and can be easily expanded
* Used pydantic_settings package to support 12-factor app methodology for maintaining env vars

## Sample endpoint that API will accept for `POST /claims`
for explanation on keys please go to above shared link:
```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/claims/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "records": [
    {
      "allowed_fees": "$100.00 ",
      "member_coinsurance": "$0.00 ",
      "member_copay": "$0.00 ",
      "group_plan": "GRP-1000",
      "provider_fees": "$100.00 ",
      "provider_npi": "1497775530",
      "quadrant": "",
      "service_date": "3\/28\/18 0:00",
      "submitted_procedure": "D0180",
      "subscriber_id": "3730189502"
    }
  ]
}'

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
