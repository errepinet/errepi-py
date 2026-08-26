# AGENTS.md

## Project

Pure-Python client bindings for Errepi Net microservices (gRPC, `grpcio`). No server code. Python >=3.10, deps: `pydantic>=2`, `grpcio>=1.60`.

- Package `errepi/`; subpackages: `errepi.cron` (client `CronConfigurator` + pydantic v2 models) and `errepi.regs` (client `GenericRegsClient` + pydantic v2 models). Shared `AppInfo` model in `errepi/models.py` (defined in both service protos).
- New microservice bindings = new subpackage under `errepi/`; packaging picks it up automatically (`MANIFEST.in` has `recursive-include errepi *`, `pyproject.toml` `include = ["errepi*"]`).
- `protos/` is a git submodule (`errepinet-sys-services-protos`) with the gRPC `.proto` defs. Generated Python stubs live in `errepi/gen/` (committed). Regenerate after a protos bump with `uv run python gen_protos.py` (requires `grpcio-tools`, in the dev group) and commit the regenerated stubs. Bump pointer with `git -C protos pull && git add protos && git commit`.
- Client interfaces mirror the RPCs of the proto services (same method names, snake_case; `tenant_id`/`namespace` params where the proto requests have them).
- Sphinx docs in `docs/` (autodoc from Google-style docstrings, version read from `pyproject.toml`).

## Commands / environment

- No test suite, no lint/typecheck config, no CI (`.github/` is empty; Actions workflow removed). Sanity-check by running `uv run python examples/cron_example.py` and `uv run python examples/regs_example.py` (both need a live gRPC service; without one, at least verify imports with `uv run python -c "import errepi.cron, errepi.regs"`).
- Environment managed with `uv` (Python 3.12 per `.python-version`, venv `.venv/`, lockfile `uv.lock` committed): `uv sync` installs runtime deps + dev group (`grpcio-tools`); run scripts with `uv run`. Old `pip` venv `.env/` is stale and gitignored; ignore it.
- Regenerate stubs after a protos bump with `uv run python gen_protos.py`.
- Build docs with `uv run sphinx-build -b html docs build/html` (sphinx + sphinx-rtd-theme in the dev group).
- `build/`, `errepi_py.egg-info/`, `__pycache__/` are stale gitignored artifacts; ignore them.

## Release

`./release.sh <semver> [--dry-run]` is the release flow:

- Requires: clean tree, on `main`, up to date with remote, tag `v<version>` must not exist.
- Bumps `version` in `pyproject.toml`, commits "Bump version to vX.Y.Z", creates annotated tag `vX.Y.Z`, pushes both. Docs are generated via GitHub Actions (workflow not currently in repo).

## Conventions

- **Always use the caveman skill** (`.agents/skills/caveman`) for responses — repo-local skill; adjust with `/caveman lite|full|ultra`, stop with "stop caveman". Keep code, errors, symbols exact.
- Pydantic v2 style: `model_dump(mode="json")`, `conint(ge=0)`, `RootModel`.
- Commit messages in Italian (per recent history).
- `CronConfigurator(config=CronClientConfiguration(host, port))` and `GenericRegsClient(config=RegsClientConfiguration(host, port))` take a client configuration (defaults `localhost:50051`). No env vars read by the library.
- Transient gRPC failures (`UNAVAILABLE`, `DEADLINE_EXCEEDED`) are retried with exponential backoff; `max_retries` and `retry_delay_secs` are configurable on the client configuration (defaults 3 retries, 1s base delay). Non-transient errors raise immediately.
