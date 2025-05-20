import configparser
from neo4j import GraphDatabase

config = configparser.ConfigParser()
config.read('config/config.ini')

URI = config['URI']['iut']
AUTH = (config['credentials']['user'], config['credentials']['pwd'])

with GraphDatabase.driver(URI, auth = AUTH) as driver:
    driver.verify_connectivity()


def execute_query(query: str, parameters: dict = None):
    try:
        with driver.session() as session:
            result: str = session.run(query, parameters or {})
            print(result)
            return [record.data() for record in result]
    except Exception as e:
        return None