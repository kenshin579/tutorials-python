"""Settings 관리 - BaseSettings, .env 파일, env_prefix"""

import os
from pathlib import Path
from unittest.mock import patch

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class TestBaseSettings:
    """BaseSettings 기본 사용법"""

    def test_settings_from_env(self):
        """환경변수에서 설정 로딩"""

        class AppSettings(BaseSettings):
            app_name: str = "default"
            debug: bool = False
            port: int = 8000

        with patch.dict(os.environ, {"APP_NAME": "MyApp", "DEBUG": "true", "PORT": "3000"}):
            settings = AppSettings()

        assert settings.app_name == "MyApp"
        assert settings.debug is True
        assert settings.port == 3000

    def test_settings_with_defaults(self):
        """환경변수 없으면 기본값 사용"""

        class DbSettings(BaseSettings):
            host: str = "localhost"
            port: int = 5432
            name: str = "mydb"

        with patch.dict(os.environ, {}, clear=True):
            settings = DbSettings()

        assert settings.host == "localhost"
        assert settings.port == 5432


class TestEnvPrefix:
    """env_prefix 설정"""

    def test_env_prefix(self):
        """환경변수 접두사 설정"""

        class Settings(BaseSettings):
            model_config = SettingsConfigDict(env_prefix="MYAPP_")

            api_key: str = "default-key"
            debug: bool = False

        with patch.dict(os.environ, {"MYAPP_API_KEY": "secret-123", "MYAPP_DEBUG": "true"}):
            settings = Settings()

        assert settings.api_key == "secret-123"
        assert settings.debug is True

    def test_env_nested_delimiter(self):
        """중첩 설정을 환경변수로 표현"""

        class DatabaseConfig(BaseModel):
            host: str = "localhost"
            port: int = 5432

        class Settings(BaseSettings):
            model_config = SettingsConfigDict(
                env_prefix="APP_",
                env_nested_delimiter="__",
            )

            db: DatabaseConfig = DatabaseConfig()

        with patch.dict(os.environ, {"APP_DB__HOST": "db.prod.com", "APP_DB__PORT": "5433"}):
            settings = Settings()

        assert settings.db.host == "db.prod.com"
        assert settings.db.port == 5433


class TestEnvFile:
    """.env 파일 로딩"""

    def test_load_from_env_file(self, tmp_path: Path):
        """.env 파일에서 설정 로딩"""
        env_file = tmp_path / ".env"
        env_file.write_text("APP_NAME=FromEnvFile\nDEBUG=true\nSECRET_KEY=my-secret\n")

        class Settings(BaseSettings):
            model_config = SettingsConfigDict(env_file=str(env_file))

            app_name: str = "default"
            debug: bool = False
            secret_key: str = "no-secret"

        settings = Settings()

        assert settings.app_name == "FromEnvFile"
        assert settings.debug is True
        assert settings.secret_key == "my-secret"

    def test_env_var_overrides_env_file(self, tmp_path: Path):
        """환경변수가 .env 파일보다 우선"""
        env_file = tmp_path / ".env"
        env_file.write_text("APP_NAME=FromFile\n")

        class Settings(BaseSettings):
            model_config = SettingsConfigDict(env_file=str(env_file))

            app_name: str = "default"

        with patch.dict(os.environ, {"APP_NAME": "FromEnvVar"}):
            settings = Settings()

        assert settings.app_name == "FromEnvVar"


class TestMultiEnvironment:
    """다중 환경 설정 관리 패턴"""

    def test_multi_environment_pattern(self, tmp_path: Path):
        """dev/staging/prod 환경별 설정"""

        def create_env_file(path: Path, content: str):
            path.write_text(content)
            return str(path)

        dev_env = create_env_file(tmp_path / ".env.dev", "MY_DATABASE_URL=sqlite:///dev.db\nMY_DEBUG=true\n")
        prod_env = create_env_file(tmp_path / ".env.prod", "MY_DATABASE_URL=postgresql://prod-db:5432/app\nMY_DEBUG=false\n")

        class Settings(BaseSettings):
            model_config = SettingsConfigDict(env_prefix="MY_", env_file=dev_env)

            database_url: str = "sqlite:///default.db"
            debug: bool = False

        # dev 환경
        dev_settings = Settings()
        assert "dev.db" in dev_settings.database_url
        assert dev_settings.debug is True

        # prod 환경 - env_file을 변경하여 다른 설정 로딩
        class ProdSettings(Settings):
            model_config = SettingsConfigDict(env_prefix="MY_", env_file=prod_env)

        prod_settings = ProdSettings()
        assert "prod-db" in prod_settings.database_url
        assert prod_settings.debug is False
