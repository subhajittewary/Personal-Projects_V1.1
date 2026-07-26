from dotenv import load_dotenv

from typing_extensions import TypedDict
from typing import Optional, Literal
from langgraph.graph import StateGraph, START, END
from openai import OpenAI


load_dotenv()
client = OpenAI()


class State(TypedDict):
    user_query: str
    llm_output: Optional[str]
    is_good: Optional[bool]


def chatbot(state: State):
    print("inside chatbot", state)
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": state.get("user_query")}
        ]
    )

    state["llm_output"] = response.choices[0].message.content
    return state


def check_response(state: State):
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {
                "role": "user",
                "content": f"""
                    Judge the following answer.

                    Question:
                    {state.get("user_query")}

                    Answer:
                    {state.get("llm_output")}

                    Respond with exactly:
                    - good
                    - bad
                    """
            }
        ]
    )

    verdict = response.choices[0].message.content.strip().lower()

    if verdict == "good":
        state["is_good"] = True
    else:
        state["is_good"] = False

    print("Inside check_response", verdict)

    return verdict


def evalualate_response(state: State) -> Literal["chatbot_gemini", "endnode"]:
    verdict = check_response(state)
    if verdict:
        return "endnode"
    return "chatbot_gemini"


def chatbot_gemini(state: State):
    print("inside chatbot_gemini", state)
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": state.get("user_query")}
        ]
    )


def endnode(state: State):
    print("inside endnode", state)
    return state


graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("chatbot_gemini", chatbot_gemini)
graph_builder.add_node("endnode", endnode)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", evalualate_response)

graph_builder.add_edge("chatbot_gemini", "endnode")
graph_builder.add_edge("endnode", END)

graph = graph_builder.compile()
updated_state = graph.invoke({"user_query": "random"})
print("updated_state\n\n", updated_state)
