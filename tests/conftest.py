import os
from pathlib import Path

import duckdb
import pytest

from mealmeter.build import build_clean, load_raw

FIXTURE = Path(__file__).parent / "fixtures" / "archive"
# stvarni sažetak koraka u GitHub Actionsu (pytest se tamo pokreće prije update.py); testovi u njega ne pišu
REAL_STEP_SUMMARY = os.environ.get("GITHUB_STEP_SUMMARY")
REAL_STEP_SUMMARY_SIZE = os.path.getsize(REAL_STEP_SUMMARY) if REAL_STEP_SUMMARY and os.path.exists(REAL_STEP_SUMMARY) else None


@pytest.fixture(autouse=True)
def step_summary(tmp_path, monkeypatch):
    """Svaki test: GITHUB_STEP_SUMMARY je privremena datoteka, a GITHUB_ACTIONS nije postavljen, pa ni test koji
    pokreće update.run() ne piše sintetičke tablice u stvarni sažetak workflowa. Test koji provjerava sažetak
    postavi GITHUB_ACTIONS=true i čita ovu datoteku."""
    path = tmp_path / "step_summary.md"
    monkeypatch.setenv("GITHUB_STEP_SUMMARY", str(path))
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
    return path


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
