"""FastAPI 入口。W1 只有健康检查，W2 开始加文档导入接口。"""

from fastapi import FastAPI

from . import __version__
from .config import settings

app = FastAPI(title="LLMWiki", version=__version__)


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "version": __version__,
        "llm_configured": settings.llm_configured,
    }
