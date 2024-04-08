from typing import Union, List

import os
from dotenv import load_dotenv
from langchain.agents import tool
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import AgentAction, AgentFinish
from langchain.tools import Tool
from langchain.tools.render import render_text_description

load_dotenv()

@tool
def get_text_length(text: str) -> int:
    """Return the length of the input text by characters."""
    return len(text)


if __name__ == "__main__":
    tools = [get_text_length]

    template = """
    Answer the following questions as best you can. You have access to the following tools:

    {tools}

    Use the following format:

    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question

    Begin!

    Question: {input}
    Thought
    """

    prompt = PromptTemplate.from_template(
        template=template
    ).partial(
        tools=render_text_description(tools),
        tool_names=", ".join([t.name for t in tools])
    )

    llm = ChatOpenAI(
        organization=os.getenv('OPENAI_ORG'),
        temperature=0,
        stop=["\nObservation"]
    )

    agent = {"input": lambda x: x["input"]} | prompt | llm
    res = agent.invoke({
        "input": "What is the length of the text 'Hello world' in characters?"
    })

    print(res)
