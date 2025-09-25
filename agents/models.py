from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

load_dotenv()

llm = init_chat_model(
    model="groq:qwen/qwen3-32b",
    max_tokens=4000
)