from config.db_connection import execute_query


def get_artists():
    query: str = "MATCH (Artist: Artist) RETURN Artist"
    results: list = execute_query(query=query)
    artists: list = [record['Artist'] for record in results]

    return artists


def post_artist(Ar_FirstName: str, Ar_LastName: str, Ar_BirthDay: str):
    query = """
    CREATE (a:Artist {Ar_FirstName: $Ar_FirstName, Ar_LastName: $Ar_LastName, Ar_BirthDay: $Ar_BirthDay})
    RETURN a AS Artist
    """
    
    params = {
        'Ar_FirstName': Ar_FirstName,
        'Ar_LastName': Ar_LastName,
        'Ar_BirthDay': Ar_BirthDay
    }

    results = execute_query(query=query, parameters=params)
    if results:
        return results[0]['Artist']
    return None
