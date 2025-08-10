# virual env name is vagent: vagent\Scripts\activate

# from dotenv import load_dotenv
from typing import Annotated, Literal
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field
from typing_extensions import TypedDict
from langchain_huggingface import HuggingFaceEndpoint,ChatHuggingFace
from huggingface_hub import login
import os
from openai import OpenAI



class State(TypedDict):
    """ 
    1-State is dict type in nature. {"messages": [], "message_type": None}
    2- messages: list which can hold add_mesges format
    3- message_type:  it can hold str var
    """
    messages: Annotated[list, add_messages]
    message_type: str | None
    summary:str|None


client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ["HF_TOKEN"],
)

def router(state: State):
    message_type = state.get("message_type", "logical")
    print("inside router function")
    print("state inside router finction is:-------------------------------------------", state)
    if message_type == "emotional":
        return {"next": "therapist"}
    return {"next": "logical"}

def LLM_Call(state: State):
    last_message = state["messages"][-1]
    print("before llm call, msg is:",last_message.content)
    completion= client.chat.completions.create(
        model="openai/gpt-oss-20b:fireworks-ai",
        messages=[
            {
            "role": "system",
            "content": """Classify the user message as either:
            - 'emotional': if it asks for emotional support, therapy, deals with feelings, or personal problems
            - 'logical': if it asks for facts, information, logical analysis, or practical solutions
            """
        },
            {
                "role": "user",
                "content": str(last_message.content)
            }])
    print("llm replies as:",completion.choices[0].message.content)
    state["messages"].append({"role": "assistant", "content":"1-for given input symantic type is: "+completion.choices[0].message.content})
    state["message_type"]= completion.choices[0].message.content
    print("state variable output after first decision taken by llm is :----------------", state)
    print("llm call ends")
    return state


def action_by_emotion(state: State):
    last_message = state["messages"][-1]
    # perform some action here
    print("action_by_emotion agent worked--------------------------------")
    state["messages"].append({"role": "assistant", "content":"Full of love, affection and glory of gods creationa and work. No fact and figures "})
    return state


def action_by_logical(state: State):
    last_message = state["messages"][-1]
    # perform some action here
    print("action_by_logical agent worked--------------------------------")
    state["messages"].append({"role": "assistant", "content":" Some action we could perform as given input was logicall as it cintains fact and figures "})
    return state


def conclusion(state: State):
    final_text=""
    for i in state["messages"]:
        final_text+=i.content
    print("****************", )
    print("before llm call, msg is:",final_text)
    print("****************", )
    completion= client.chat.completions.create(
        model="openai/gpt-oss-20b:fireworks-ai",
        messages=[
            {
            "role": "system",
            "content": """Summarize it the full text in one line
            """
        },
            {
                "role": "user",
                "content": str(final_text)+"Summarize it the full text in one line only "
            }])
    print("llm replies as:",completion.choices[0].message.content)
    state["messages"].append({"role": "assistant", "content":"summarized data is: "+completion.choices[0].message.content})
    print("llm call ends with state:", state)
    return state

graph_builder = StateGraph(State)

graph_builder.add_node("classifier", LLM_Call)
graph_builder.add_node("router", router)
graph_builder.add_node("therapist", action_by_emotion)
graph_builder.add_node("logical", action_by_logical)
graph_builder.add_node("cocnclusion", conclusion)

graph_builder.add_edge(START, "classifier")
graph_builder.add_edge("classifier", "router")
# graph_builder.add_edge("router", END)

graph_builder.add_conditional_edges(
    "router",
    lambda state: state.get("next"),
    {"therapist": "therapist", "logical": "logical"}
)

graph_builder.add_edge("therapist", "cocnclusion")
graph_builder.add_edge("logical", "cocnclusion")
graph_builder.add_edge("cocnclusion", END)

graph = graph_builder.compile()


def run_chatbot():
    state = {"messages": [], "message_type": None}

    while True:
        print("Give exit if you want to exit it from the process. Thanks")
        user_input ="Hey Artificial intelligenc, do you think that sai pallvi is a cute heroine! "
        if user_input == "exit":
            print("Bye")
            break
        
        state["messages"] = state.get("messages", []) + [
            {"role": "user", "content": user_input}
        ]
        print("User input is:",user_input)
        print("Graph state is:",state)
        state = graph.invoke(state)

        if state.get("messages") and len(state["messages"]) > 0:
            last_message = state["messages"][-1]
            print(f"last  state msg: ",last_message)
        print("updated full Graph state is:",state)
        break

if __name__ == "__main__":
    
    """
    OBSERVATIONS:
    1-LangGraph expects each node to return the full updated state, not just a partial one. If you return a new dict, it assumes that’s the new state and discards the rest.
    2-output of every node must be state var, if you will retwun a new dict as state from a node then , graph will start considering that new dict as new state variable and will discard prev one!
    """
    run_chatbot()


