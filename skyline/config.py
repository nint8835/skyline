from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="skyline_", env_file=".env")

    db_path: str = "skyline.sqlite"
    db_log_queries: bool = False

    bind_host: str = "0.0.0.0"
    bind_port: int = 8000
    behind_reverse_proxy: bool = False
    session_secret: str = "change_me"

    github_client_id: str
    github_client_secret: str
    github_machine_user_pat: str

    log_level: str = "INFO"

    @property
    def async_db_connection_uri(self) -> str:
        return f"sqlite+aiosqlite:///{self.db_path}"

    @property
    def sync_db_connection_uri(self) -> str:
        return f"sqlite:///{self.db_path}"


config = Config()  # type: ignore - Pyright doesn't know about pydantic_settings

__all__ = ["config"]
