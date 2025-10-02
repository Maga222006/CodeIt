from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

load_dotenv()

llm = init_chat_model(
    model="groq:moonshotai/kimi-k2-instruct-0905",
    max_tokens=4000
)