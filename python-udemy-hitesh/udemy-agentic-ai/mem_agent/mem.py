from mem0 import Memory
import os

OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")

config = {
    "version": "v1.1",
    "embedder": {
        "provider": "openai",
        "config": {
            "api_key": OPEN_AI_API_KEY,
            "model": "text-embedding-3-small"
        }
    },
    "llm": {
        "provider": "openai",
        "config": {
                    "api_key": OPEN_AI_API_KEY,
                    "model": "gpt-4.1"
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
