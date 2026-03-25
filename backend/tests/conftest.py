import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from alembic import command
from alembic.config import Config

import tempfile

TEST_DB_FILE = Path(tempfile.gettempdir()) / "test_finhub.db"
TEST_DATABASE_URL = f"sqlite:///{TEST_DB_FILE}"


@pytest.fixture
def client():
    if TEST_DB_FILE.exists():
        TEST_DB_FILE.unlink()

    os.environ["DATABASE_URL"] = TEST_DATABASE_URL

    from app.settings import get_settings
    get_settings.cache_clear()

    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

    from app.main import app

    with TestClient(app) as test_client:
        yield test_client

    if TEST_DB_FILE.exists():
        TEST_DB_FILE.unlink()