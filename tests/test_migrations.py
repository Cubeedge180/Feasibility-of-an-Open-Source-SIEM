"""Static checks on db/migrations (applying them needs PostgreSQL; CI job `migrations` does)."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

MIGRATIONS = Path(__file__).resolve().parent.parent / "db" / "migrations"
FILES = sorted(MIGRATIONS.glob("*.sql"))


def test_migrations_are_numbered_without_gaps() -> None:
    numbers = [int(f.name[:4]) for f in FILES]
    assert numbers == list(range(1, len(FILES) + 1))
    assert all(re.fullmatch(r"\d{4}_[a-z0-9_]+\.sql", f.name) for f in FILES)


@pytest.mark.parametrize("path", FILES, ids=lambda p: p.name)
def test_migration_is_transactional_and_records_itself(path: Path) -> None:
    sql = path.read_text(encoding="utf-8")
    assert "BEGIN;" in sql and sql.rstrip().endswith("COMMIT;")
    assert f"INSERT INTO schema_migrations (version) VALUES ('{path.stem}');" in sql
