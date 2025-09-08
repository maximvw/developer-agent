import yaml
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from typing import Any, Tuple

load_dotenv()


def yaml_config_settings_source() -> dict[str, Any]:
    try:
        with open("configs/config.yaml", "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        print(
            "Предупреждение: Файл 'config.yaml' не найден. Используются значения по умолчанию и из .env."
        )
        return {}


class Settings(BaseSettings):
    # model_config = SettingsConfigDict(
    #     env_file='configs/.env',
    #     env_file_encoding='utf-8'
    # )

    WORKSPACE_DIR: str = "workspace"
    CONTEXT_WINDOW_SIZE: int = 30
    LLM_MODEL_NAME: str = "gemini-2.0-flash"
    MAX_TOKENS: int = 1024
    TEMPERATURE: float = 0

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls,
        init_settings,
        env_settings,
        dotenv_settings,
        file_secret_settings,
    ) -> Tuple[Any, ...]:
        return (
            env_settings,
            dotenv_settings,
            file_secret_settings,
            init_settings,
            yaml_config_settings_source,  # Добавляем наш источник
        )


settings = Settings()
