import sys
from pathlib import Path

import pytest
from peewee import SqliteDatabase

# 프로젝트 루트를 path에 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

from models import ALL_TABLES  # noqa: E402

test_db = SqliteDatabase(":memory:", pragmas={"foreign_keys": 1})


@pytest.fixture(autouse=True)
def setup_db():
    """각 테스트마다 인메모리 DB를 바인딩하고 테이블 생성/삭제."""
    test_db.bind(ALL_TABLES, bind_refs=False, bind_backrefs=False)
    test_db.connect()
    test_db.create_tables(ALL_TABLES)
    yield test_db
    test_db.drop_tables(ALL_TABLES)
    test_db.close()
