"""应用配置：全部走环境变量，前缀 LLMWIKI_，本地用 .env 覆盖。"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="LLMWIKI_",
        extra="ignore",
    )

    # LLM（先用 OpenAI 兼容接口，DeepSeek / 通义 / 本地 vLLM 都能接）
    llm_api_key: str = ""
    llm_base_url: str = "https://api.deepseek.com/v1"
    llm_model: str = "deepseek-chat"

    # 存储
    database_url: str = "postgresql://postgres:postgres@localhost:5432/llmwiki"

    # 检索
    top_k: int = 6

    @property
    def llm_configured(self) -> bool:
        return bool(self.llm_api_key)


settings = Settings()
