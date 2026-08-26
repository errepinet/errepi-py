# AGENTS.md

## Project

Pure-Python client bindings for Errepi Net microservices (REST, `requests`). No server code. Python >=3.10, deps: `pydantic>=2`, `requests>=2`.

- Package `errepi/`; only subpackage today is `errepi.cron` (client `CronConfigurator` + pydantic v2 models).
- New microservice bindings = new subpackage under `errepi/`; packaging picks it up automatically (`MANIFEST.in` has `recursive-include errepi *`, `pyproject.toml` `include = ["errepi*"]`).
- `protos/` is a git submodule (`errepinet-sys-services-protos`) with the gRPC `.proto` defs; the Python lib is REST-only, protos serve as API reference. Bump pointer with `git -C protos pull && git add protos && git commit`. `protoc` not needed here (only in the Rust apps).
- Sphinx docs in `docs/` (autodoc from Google-style docstrings, version read from `pyproject.toml`).

## Commands / environment

- No test suite, no lint/typecheck config, no CI (`.github/` is empty; Actions workflow removed). Sanity-check by running `examples/cron_example.py` with `python examples/cron_example.py`.
- Local venv lives in `.env/` (gitignored) — that is a Python venv, not a dotenv file: use `.env/bin/python`, `.env/bin/pip`.
- `build/`, `errepi_py.egg-info/`, `__pycache__/` are stale gitignored artifacts; ignore them.

## Release

`./release.sh <semver> [--dry-run]` is the release flow:

- Requires: clean tree, on `main`, up to date with remote, tag `v<version>` must not exist.
- Bumps `version` in `pyproject.toml`, commits "Bump version to vX.Y.Z", creates annotated tag `vX.Y.Z`, pushes both. Docs are generated via GitHub Actions (workflow not currently in repo).

## Conventions

- **Always use the caveman skill** (`.agents/skills/caveman`) for responses — repo-local skill; adjust with `/caveman lite|full|ultra`, stop with "stop caveman". Keep code, errors, symbols exact.
- Pydantic v2 style: `model_dump(mode="json")`, `conint(ge=0)`, `RootModel`.
- Commit messages in Italian (per recent history).
- Client methods mirror REST paths of the cron bridge service; `CronConfigurator.from_env()` reads `ERREPI_CRON_CONF_URL` (default `http://localhost:8080`).
