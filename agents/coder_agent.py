from agents.prompts import coder_instructions, researcher_instructions, coder_system_message
from langchain_core.messages import SystemMessage
from langgraph.prebuilt import create_react_agent
from agents.tools import coder_tools, web_search
from langgraph.constants import START, END
from agents.states import CoderState
from langgraph.graph import StateGraph
from agents.models import llm


research_agent = create_react_agent(
    llm,
    tools=[web_search],
    prompt=researcher_instructions,
    state_schema=CoderState,
)

code_agent = create_react_agent(
    llm,
    tools=coder_tools,
    prompt=coder_instructions,
    state_schema=CoderState,
)

def research_agent_node(state: dict):
    state['messages'].append(research_agent.invoke(state)['messages'][-1])
    return state

def code_agent_node(state: dict):
    state['messages'].append(SystemMessage(coder_system_message(state=state)))
    state = code_agent.invoke(state)
    return state

graph = StateGraph(dict)
graph.add_node("research_agent_node", research_agent_node)
graph.add_node("code_agent_node", code_agent_node)
graph.add_edge(START, "research_agent_node")
graph.add_edge("research_agent_node", "code_agent_node")
graph.add_edge("code_agent_node", END)

coder_agent = graph.compile(name="coder_agent")
