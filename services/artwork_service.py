from config.db_connection import execute_query

def get_artwork():
    query: str = "MATCH (Artwork :Artwork) RETURN Artwork"
    results: list = execute_query(query=query)
    artwork: list = [record['Artwork'] for record in results]

    return artwork

def get_artwork_by_id(Ar_ArtworkID: int):
    query = """
    MATCH (a:Artwork {Ar_ArtworkID: $Ar_ArtworkID})
    RETURN a
    """
    results = execute_query(query=query, parameters={'Ar_ArtworkID': Ar_ArtworkID})
    if results:
        return results[0]['a']
    return None

def post_artwork(Art_Title: str, Art_Year: int, Art_Description: str, Art_ImageURL: str, Art_Medium: str, Art_Dimensions: str):
    query = """
    MERGE (c:Counter {name: 'Art_ArtworkID'})
    ON CREATE SET c.count = 0
    SET c.count = c.count + 1
    WITH c.count AS new_id
    CREATE (a)-[:CREATED]->(aw:Artwork {Art_ArtworkID: new_id, Art_Title: $Art_Title, Art_Year: $Art_Year, Art_Description: $Art_Description, Art_ImageURL: $Art_ImageURL, Art_Medium: $Art_Medium, Art_Dimensions: $Art_Dimensions})
    RETURN aw AS Artwork
    """
    params = {
        'Art_Title': Art_Title,
        'Art_Year': Art_Year,
        'Art_Description': Art_Description,
        'Art_ImageURL': Art_ImageURL,
        'Art_Medium': Art_Medium,
        'Art_Dimensions': Art_Dimensions
    }

    results = execute_query(query=query, parameters=params)
    if results:
        return results[0]['Artwork']
    return None
