from agents.coder_agent import coder_agent as agent
from langchain_core.messages import HumanMessage
from mcp.server.fastmcp import FastMCP
from threading import Thread
import gradio as gr

mcp = FastMCP("CodeIt")

@mcp.tool()
def coder_agent(project_name: str, task_description: str, private: bool=False):
    """Coder Agent, used as a tool for any coding tasks, it creates project, tests it and saves to GitHub.

    :param project_name: The name of the GitHub repository and directory for the project.
    :param task_description: A detailed description of the project for the coder to create.
    :param private: Whether or not the repository is private.
    :return:
    """
    Thread(target=agent.invoke, args=[{'messages': [HumanMessage(content=task_description)], 'project_name': project_name, 'private': private},]).start()
    return "Coder agent in progress — results will be posted to GitHub once complete."

demo = gr.Interface(
    fn=coder_agent,
    inputs=[
        gr.Textbox(label="Project Name", placeholder="my-new-repo"),
        gr.Textbox(label="Task Description", placeholder="Build a FastAPI app with CRUD and tests", lines=6),
        gr.Checkbox(label="Private repository?", value=False),
    ],
    outputs=gr.Textbox(label="Status"),
    title="CodeIt — Coder Agent",
    description="Kick off a coding task. The agent runs asynchronously and will push to GitHub when done.",
)


if __name__ == "__main__":
    demo.launch(mcp_server=True, show_error=True)