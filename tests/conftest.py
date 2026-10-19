from pathlib import Path

import duckdb
import pytest

from mealmeter.build import build_clean, load_raw

FIXTURE = Path(__file__).parent / "fixtures" / "archive"


@pytest.fixture(scope="session")
def built(tmp_path_factory):
    """Baza izgrađena iz fixture-arhive (stvarni retci iz arhive 2026-10-19)."""
    db = tmp_path_factory.mktemp("db") / "test.duckdb"
    c = duckdb.connect(str(db))
    load_raw(c, FIXTURE, "2026-10-19")
    stats = build_clean(c)
    yield c, stats
    c.close()


@pytest.fixture
def con(built):
    return built[0]
