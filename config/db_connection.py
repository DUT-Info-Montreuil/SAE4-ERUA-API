import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

URI = os.getenv("NEO4J_URL")
AUTH = (os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD"))

driver = GraphDatabase.driver(URI, auth=AUTH)

try:
    driver.verify_connectivity()
    print("Connexion Neo4j établie avec succès")
except Exception as e:
    print(f"Erreur de connexion Neo4j : {e}")


def execute_query(query: str, parameters: dict = None):
    """
    Exécute une requête Neo4j avec gestion robuste des erreurs
    """
    max_retries = 3
    retry_count = 0

    while retry_count < max_retries:
        try:
            with driver.session() as session:
                result = session.run(query, parameters or {})
                return [record.data() for record in result]
        except Exception as e:
            retry_count += 1
            print(f"Erreur lors de l'exécution de la requête (tentative {retry_count}/{max_retries}) : {e}")

            if retry_count < max_retries and "connection" in str(e).lower():
                try:
                    driver.verify_connectivity()
                except:
                    pass
            else:
                return None

    return None
