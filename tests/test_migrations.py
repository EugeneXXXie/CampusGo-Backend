from pathlib import Path


def test_alembic_files_exist() -> None:
    assert Path("alembic.ini").exists()
    assert Path("alembic/versions/20260424_000001_init_tables.py").exists()
