from langchain_google_genai import ChatGoogleGenerativeAI
from modules.settings.agent_config import settings

llm = ChatGoogleGenerativeAI(
    model=settings.LLM_MODEL_NAME,
    temperature=settings.TEMPERATURE,
    max_tokens=settings.MAX_TOKENS,
    transport="rest",
)
