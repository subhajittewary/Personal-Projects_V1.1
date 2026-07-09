# Chain Of Thought Prompting
from dotenv import load_dotenv
import google.generativeai as genai
import requests
import json
from pydantic import BaseModel, Field, ValidationError
from typing import Optional
from google.api_core import exceptions

load_dotenv()

genai.configure(
    api_key="PLACEHOLDER-KEY")
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

class MyOutputFormat(BaseModel):
    step: str = Field(..., description="The id of step. Example: PLAN, OUTPUT, TOOL etc.")
    content: Optional[str] = Field(None, description="The optional string content for the step.")
    tool: Optional[str] = Field(None, description="The id of the tool to call.")
    input: Optional[str] = Field(None, description="The input params for the tool.")


message_history = [
    {"role": "user", "parts": [SYSTEM_PROMPT]},
]
while True:
    user_query = input("👉🏻 ")
    message_history.append({"role": "user", "parts": [user_query]})

    while True:
        try:
            response = client.generate_content(
                contents=message_history,
                generation_config=genai.types.GenerationConfig(
                    response_mime_type="application/json",
                )
            )
        except exceptions.ResourceExhausted as exc:
            print("⚠️ Gemini quota exceeded. Please wait a bit and try again later.")
            print(exc)
            break

        raw_result = response.text
        message_history.append({"role": "model", "parts": [raw_result]})

        try:
            parsed_result = MyOutputFormat.model_validate_json(raw_result)
        except ValidationError:
            print("⚠️ The model response was not valid JSON. Trying once more...")
            continue

        if parsed_result.step == "START":
            print("🔥", parsed_result.content)
            continue

        if parsed_result.step == "TOOL":
            tool = parsed_result.tool
            input_value = parsed_result.input
            print(f"⚙️: {tool} ({input_value})")

            tool_response = available_tools[tool](input_value)
            print(f"⚙️: {tool}({input_value}) = {tool_response}")
            message_history.append({"role": "user", "parts": [json.dumps(
                {
                    "step": "OBSERVE",
                    "tool": tool,
                    "input": input_value,
                    "output": tool_response
                }
            )]})
            continue

        if parsed_result.step == "PLAN":
            print("🧠", parsed_result.content)
            continue

        if parsed_result.step == "OUTPUT":
            print("🤖", parsed_result.content)
            break

    print("\n\n\n")
