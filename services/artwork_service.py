from config.db_connection import execute_query

def get_artwork():
    query: str = "MATCH (Artwork :Artwork) RETURN Artwork"
    results: list = execute_query(query=query)
    artwork: list = [record['Artwork'] for record in results]

    return artwork

def post_artwork(Art_Title: str, Art_Year: int, Art_Description: str, Ar_FirstName: str, Ar_LastName: str):
    query = """
    MATCH (a:Artist {Ar_FirstName: $Ar_FirstName, Ar_LastName: $Ar_LastName})
    CREATE (a)-[:CREATED]->(aw:Artwork {Art_Title: $Art_Title, Art_Year: $Art_Year, Art_Description: $Art_Description})
    RETURN aw AS Artwork
    """
    params = {
        'Art_Title': Art_Title,
        'Art_Year': Art_Year,
        'Art_Description': Art_Description,
        'Ar_FirstName': Ar_FirstName,
        'Ar_LastName': Ar_LastName
    }

    results = execute_query(query=query, parameters=params)
    if results:
        return results[0]['Artwork']
    return None
