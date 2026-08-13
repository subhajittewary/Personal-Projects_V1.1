from openai import OpenAI
import json
from mem0 import Memory
from dotenv import load_dotenv
import os
import certifi
from pathlib import Path

# Configure TLS before importing Mem0, which imports the Neo4j driver.
# The Python.org macOS installation may not have a system CA bundle configured.
os.environ.setdefault("SSL_CERT_FILE", certifi.where())


# Always load this script's .env file, even when the app is started from a
# different working directory or stale Neo4j variables exist in the shell.
load_dotenv(dotenv_path=Path(__file__).with_name(".env"), override=True)
client = OpenAI()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NEO_CONNECTION_URI = os.getenv("NEO_CONNECTION_URI")
NEO_USERNAME = os.getenv("NEO_USERNAME")
NEO_PASSWORD = os.getenv("NEO_PASSWORD")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is missing. Add it to your .env file.")

if not all([NEO_CONNECTION_URI, NEO_USERNAME, NEO_PASSWORD]):
    raise ValueError(
        "Neo4j configuration is missing. Set NEO_CONNECTION_URI, NEO_USERNAME, "
        "and NEO_PASSWORD in your .env file."
    )

config = {
    "embedder": {
        "provider": "openai",
        "config": {
            "api_key": OPENAI_API_KEY,
            "model": "text-embedding-3-small"
        }
    },
    "llm": {
        "provider": "openai",
        "config": {
                    "api_key": OPENAI_API_KEY,
                    "model": "gpt-4.1"
        }
    },
    "graph_store": {
        "provider": "neo4j",
        "config": {
            "url": NEO_CONNECTION_URI,
            "username": NEO_USERNAME,
            "password": NEO_PASSWORD,
            "database": "c062c31b"
        }
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": "localhost",
            "port": 6333
        }
    }
}

mem_client = Memory.from_config(config)

while True:
    user_query = input("> ")
    search_memory = mem_client.search(
        query=user_query, filters={"user_id": "subhajit"})

    memories = [
        f"ID: {mem.get('id')}\nMemory: {mem.get('memory')}"
        for mem in search_memory.get("results", [])
    ]

    # print(f"found memories {memories}")

    SYSTEM_PROMPT = f"""
    Here is the context about the user:
    {json.dumps(memories)}
        """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_query}
        ]
    )

    ai_response = response.choices[0].message.content

    print("AI: ", ai_response)

    save_result = mem_client.add(
        user_id="subhajit",
        messages=[
            {"role": "user", "content": user_query},
            {"role": "assistant", "content": ai_response}
        ]
    )

    print("memory has been saved...")
    print("Neo4j relations:", save_result.get("relations"))
