# Chain Of Thought Prompting
from dotenv import load_dotenv
import google.generativeai as genai
import requests
import json
import os

load_dotenv()

genai.configure(
    api_key="AQ.Ab8RN6LgYKj00j7-9rsjBshzF37kn9PAJqHE2urdTjflfMTf-g")
client = genai.GenerativeModel("gemini-2.5-flash")


def get_weather(city: str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}"

    return "Something went wrong"


available_tools = {
    "get_weather": get_weather
}


SYSTEM_PROMPT = """
    You're an expert AI Assistant in resolving user queries using chain of thought.
    You work on START, PLAN and OUPUT steps.
    You need to first PLAN what needs to be done. The PLAN can be multiple steps.
    Once you think enough PLAN has been done, finally you can give an OUTPUT.
    You can also call tool from the list of available tools.
    For every tool call wait for the observe step which is the output from the called tool.

    Rules:
    - Strictly Follow the given JSON output format
    - Only run one step at a time.
    - The sequence of steps is START (where user gives an input), PLAN (That can be multiple times) and finally OUTPUT (which is going to the displayed to the user).

    Output JSON Format:
    { "step": "START" | "PLAN" | "OUTPUT" | "TOOL", "content": "string", "tool": "string", "input": "string" }

    Available Tools:
    - get_weather(city: str): Takes city name as an input string and returns the weather info about the city.

    Example 1:
    START: Hey, Can you solve 2 + 3 * 5 / 10
    PLAN: { "step": "PLAN": "content": "Seems like user is interested in math problem" }
    PLAN: { "step": "PLAN": "content": "looking at the problem, we should solve this using BODMAS method" }
    PLAN: { "step": "PLAN": "content": "Yes, The BODMAS is correct thing to be done here" }
    PLAN: { "step": "PLAN": "content": "first we must multiply 3 * 5 which is 15" }
    PLAN: { "step": "PLAN": "content": "Now the new equation is 2 + 15 / 10" }
    PLAN: { "step": "PLAN": "content": "We must perform divide that is 15 / 10  = 1.5" }
    PLAN: { "step": "PLAN": "content": "Now the new equation is 2 + 1.5" }
    PLAN: { "step": "PLAN": "content": "Now finally lets perform the add 3.5" }
    PLAN: { "step": "PLAN": "content": "Great, we have solved and finally left with 3.5 as ans" }
    OUTPUT: { "step": "OUTPUT": "content": "3.5" }

    Example 2:
    START: What is the weather of Delhi?
    PLAN: { "step": "PLAN": "content": "Seems like user is interested in getting weather of Delhi in India" }
    PLAN: { "step": "PLAN": "content": "Lets see if we have any available tool from the list of available tools" }
    PLAN: { "step": "PLAN": "content": "Great, we have get_weather tool available for this query." }
    PLAN: { "step": "PLAN": "content": "I need to call get_weather tool for delhi as input for city" }
    PLAN: { "step": "TOOL": "tool": "get_weather", "input": "delhi" }
    PLAN: { "step": "OBSERVE": "tool": "get_weather", "output": "The temp of delhi is cloudy with 20 C" }
    PLAN: { "step": "PLAN": "content": "Great, I got the weather info about delhi" }
    OUTPUT: { "step": "OUTPUT": "content": "The cuurent weather in delhi is 20 C with some cloudy sky." }
    
"""

print("\n\n\n")

message_history = [
    {"role": "user", "parts": [SYSTEM_PROMPT]},
]
while True:
    user_query = input("👉🏻 ")
    message_history.append({"role": "user", "parts": [user_query]})

    while True:
        response = client.generate_content(
            contents=message_history,
            generation_config={
                "response_mime_type": "application/json",
            }
        )

        raw_result = response.text
        message_history.append({"role": "model", "parts": [raw_result]})

        parsed_result = json.loads(raw_result)

        if parsed_result.get("step") == "START":
            print("🔥", parsed_result.get("content"))
            continue

        if parsed_result.get("step") == "TOOL":
            tool = parsed_result.get("tool")
            input = parsed_result.get("input")
            print(f"⚙️: {tool} ({input})")

            tool_response = available_tools[tool](input)
            print(f"⚙️: {tool}({input}) = {tool_response}")
            message_history.append({"role": "user", "parts": [json.dumps(
                {
                    "step": "OBSERVE",
                    "tool": tool,
                    "input": input,
                    "output": tool_response
                }
            )]})
            continue

        if parsed_result.get("step") == "PLAN":
            print("🧠", parsed_result.get("content"))
            continue

        if parsed_result.get("step") == "OUTPUT":
            print("🤖", parsed_result.get("content"))
            break

    print("\n\n\n")
