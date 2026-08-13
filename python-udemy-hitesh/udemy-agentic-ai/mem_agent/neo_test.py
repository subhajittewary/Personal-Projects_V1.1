import os
from pathlib import Path

import certifi
from dotenv import load_dotenv
from neo4j import GraphDatabase

os.environ["SSL_CERT_FILE"] = certifi.where()

load_dotenv(
    dotenv_path=Path(__file__).with_name(".env"),
    override=True,
)

uri = os.getenv("NEO_CONNECTION_URI")
username = os.getenv("NEO_USERNAME")
password = os.getenv("NEO_PASSWORD")

print("URI:", uri)
print("USERNAME:", username)
print("PASSWORD:", "***" if password else None)

driver = GraphDatabase.driver(
    uri,
    auth=(username, password),
)

driver.verify_connectivity()

print("✅ Neo4j Aura connection successful!")

with driver.session(database="c062c31b") as session:
    result = session.run("RETURN 1 AS result")
    print(result.single()["result"])

    from langchain_neo4j import Neo4jGraph

graph = Neo4jGraph(
    url=uri,
    username=username,
    password=password,
    database="c062c31b",
    driver_config={"notifications_min_severity": "OFF"},
)

print("✅ LangChain Neo4j connection works!")

print(graph.query("RETURN 1 AS result"))

driver.close()
