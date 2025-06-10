from config.db_connection import execute_query


def get_artists():
    query: str = "MATCH (Artist: Artist) RETURN Artist"
    results: list = execute_query(query=query)
    artists: list = [record['Artist'] for record in results]

    return artists


def post_artist(Ar_FirstName: str, Ar_LastName: str, Ar_BirthDay: str, Ar_Nationality: str, Ar_Biography: str,
                Ar_ImageURL: str, Ar_DeathDay: str = ""):
    query = """
    MERGE (c:Counter {name: 'Ar_ArtistID'})
    ON CREATE SET c.count = 0
    SET c.count = c.count + 1
    WITH c.count AS new_id
    CREATE (a:Artist {
        Ar_ArtistID: new_id,
        Ar_FirstName: $Ar_FirstName,
        Ar_LastName: $Ar_LastName,
        Ar_BirthDay: $Ar_BirthDay,
        Ar_Nationality: $Ar_Nationality,
        Ar_Biography: $Ar_Biography,
        Ar_ImageURL: $Ar_ImageURL,
        Ar_DeathDay: $Ar_DeathDay
    })
    RETURN a
    """

    params = {
        'Ar_FirstName': Ar_FirstName,
        'Ar_LastName': Ar_LastName,
        'Ar_BirthDay': Ar_BirthDay,
        'Ar_Nationality': Ar_Nationality,
        'Ar_Biography': Ar_Biography,
        'Ar_ImageURL': Ar_ImageURL,
        'Ar_DeathDay': Ar_DeathDay
    }

    results = execute_query(query=query, parameters=params)
    if results:
        return results[0]['a']
    return None


def get_artist_by_id(Ar_ArtistID: int):
    query = """
    MATCH (a:Artist {Ar_ArtistID: $Ar_ArtistID})
    RETURN a
    """
    results = execute_query(query=query, parameters={'Ar_ArtistID': Ar_ArtistID})
    if results:
        return results[0]['a']
    return None


def post_create_relation(Ar_ArtistID: int, Art_ArtworkID: int):
    """
    Crée une relation 'CREATE' entre un artiste et une œuvre
    """
    query = """
    MATCH (artist:Artist {Ar_ArtistID: $Ar_ArtistID})
    MATCH (artwork:Artwork {Art_ArtworkID: $Art_ArtworkID})
    MERGE (artist)-[r:CREATED]->(artwork)
    RETURN r, artist, artwork
    """

    params = {
        'Ar_ArtistID': Ar_ArtistID,
        'Art_ArtworkID': Art_ArtworkID
    }

    results = execute_query(query=query, parameters=params)
    return results[0] if results else None


def get_artist_with_artworks(Ar_ArtistID: int):
    """
    Récupère un artiste avec toutes ses œuvres
    """
    query = """
    MATCH (artist:Artist {Ar_ArtistID: $Ar_ArtistID})
    OPTIONAL MATCH (artist)-[:CREATED]->(artwork:Artwork)
    RETURN artist, COLLECT(artwork) AS artworks
    """

    results = execute_query(query=query, parameters={'Ar_ArtistID': Ar_ArtistID})
    if results:
        return {
            'artist': results[0]['artist'],
            'artworks': results[0]['artworks']
        }
    return None
