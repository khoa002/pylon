"""Mechanical enforcement of the architectural constraints.

These are not style checks. Each one encodes a decision recorded in
docs/DECISIONS/. If one fails, either the code is wrong or the ADR needs
revisiting. Do not weaken a test here without writing the ADR first.
"""

import ast
import pathlib

import pytest

SRC = pathlib.Path(__file__).parent.parent / "src" / "pylon"

ENGINE_PACKAGES = ("graph", "rules")


def _imported_modules(path: pathlib.Path) -> set[str]:
    """Every module name imported by a Python file, flattened."""
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    found: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            found.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            found.add(node.module)
    return found


def _python_files(package: str) -> list[pathlib.Path]:
    return sorted((SRC / package).rglob("*.py"))


@pytest.mark.parametrize("package", ENGINE_PACKAGES)
def test_engine_does_not_import_adapters(package: str) -> None:
    """ADR-002: adapters are the only place that knows about upstream formats.

    If a new source seems to require the engine to know about it, stop and write
    an ADR. The Milestone 2 definition of done depends on this holding.
    """
    offenders = [
        (path.name, module)
        for path in _python_files(package)
        for module in _imported_modules(path)
        if module.startswith("pylon.adapters")
    ]
    assert not offenders, f"pylon/{package}/ must not import adapters: {offenders}"


@pytest.mark.parametrize("package", ENGINE_PACKAGES)
def test_engine_is_pure(package: str) -> None:
    """The solver and evaluator take loaded data and return answers.

    No ORM session, no HTTP, no filesystem. This is what lets the solver be
    tested exhaustively without Postgres, and it keeps the hot path memoizable.
    """
    banned_roots = {"sqlalchemy", "httpx", "requests", "psycopg", "alembic"}
    banned_prefixes = ("pylon.api", "pylon.models")
    offenders = [
        (path.name, module)
        for path in _python_files(package)
        for module in _imported_modules(path)
        if module.split(".")[0] in banned_roots or module.startswith(banned_prefixes)
    ]
    assert not offenders, f"pylon/{package}/ must stay pure: {offenders}"


def test_no_llm_client_in_the_engine() -> None:
    """ADR-001: the LLM never decides what is required.

    Model clients belong in ``agent/`` only. If this fails, reasoning has leaked
    into the solver, which is the one thing the whole design exists to prevent.
    """
    banned_roots = {"anthropic", "openai", "langchain", "llama_index", "litellm"}
    offenders = [
        (str(path.relative_to(SRC)), module)
        for package in (*ENGINE_PACKAGES, "models", "adapters")
        for path in _python_files(package)
        for module in _imported_modules(path)
        if module.split(".")[0] in banned_roots
    ]
    assert not offenders, f"model clients belong in agent/ only: {offenders}"


def test_every_adr_referenced_in_code_exists() -> None:
    """Catches an ADR number cited in a docstring that was never written."""
    decisions = pathlib.Path(__file__).parent.parent / "docs" / "DECISIONS"
    existing = {p.name.split("-")[1] for p in decisions.glob("ADR-*.md")}

    cited: set[str] = set()
    for path in SRC.rglob("*.py"):
        for token in path.read_text(encoding="utf-8").split():
            stripped = token.strip(".,;:()[]")
            if stripped.startswith("ADR-") and len(stripped) >= 7:
                cited.add(stripped[4:7])

    missing = cited - existing
    assert not missing, f"code cites ADRs that do not exist: {sorted(missing)}"
