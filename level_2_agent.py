# level_2_agent.py
from fastapi.middleware.cors import CORSMiddleware
from agno.agent import Agent
from agno.models.groq import Groq
from agno.playground import Playground
from agno.storage.sqlite import SqliteStorage
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools
import os 
import uvicorn

os.makedirs("tmp", exist_ok=True)
port = int(os.environ.get("PORT", 8080))  # Usa 8080 por defecto

agent_storage: str = "tmp/agents.db"
groq_model = Groq(
    id="llama-3.3-70b-versatile",
    api_key="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"
)
GROQ_API_KEY= "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"


# Configuración de los agentes
web_agent = Agent(
    name="Jus Agent",
    model=groq_model,
    tools=[DuckDuckGoTools()],
    instructions=["Always include sources"],
    storage=SqliteStorage(table_name="web_agent", db_file=agent_storage),
    add_datetime_to_instructions=True,
    add_history_to_messages=True,
    num_history_responses=5,
    markdown=True,
)

finance_agent = Agent(
    name="ANGENCIA JUSTIN",
    model=groq_model,
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True, company_news=True)],
    instructions=["Always use tables to display data"],
    storage=SqliteStorage(table_name="finance_agent", db_file=agent_storage),
    add_datetime_to_instructions=True,
    add_history_to_messages=True,
    num_history_responses=5,
    markdown=True,
)



# Crear la aplicación Playground
playground_app = Playground(agents=[web_agent, finance_agent])

# Obtener la aplicación ASGI
app = playground_app.get_app()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://frontend-480864689577.europe-west1.run.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


