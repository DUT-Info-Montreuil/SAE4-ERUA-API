from config.db_connection import execute_query

def get_artists():
    query = "MATCH (Artist:Artist) RETURN Artist"
    results = execute_query(query=query)
    return [record['Artist'] for record in results]


def post_artist(
    Ar_FirstName: str,
    Ar_LastName: str,
    Ar_BirthDay: str,
    Ar_Nationality: str,
    Ar_Biography: str,
    Ar_ImageURL: str,
    Ar_DeathDay: str = "",
    Ar_CountryBirth: str = "",
    Ar_CountryDeath: str = "",
    Ar_Movement: list = None
):

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
        Ar_DeathDay: $Ar_DeathDay,
        Ar_CountryBirth: $Ar_CountryBirth,
        Ar_CountryDeath: $Ar_CountryDeath,
        Ar_Movement: $Ar_Movement
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
        'Ar_DeathDay': Ar_DeathDay,
        'Ar_CountryBirth': Ar_CountryBirth,
        'Ar_CountryDeath': Ar_CountryDeath,
        'Ar_Movement': Ar_Movement or []
    }
    results = execute_query(query=query, parameters=params)
    return results[0]['a'] if results else None


def delete_artist_by_id(Ar_ArtistID: int):
    query = """
    MATCH (a:Artist {Ar_ArtistID: $Ar_ArtistID})
    DETACH DELETE a
    RETURN COUNT(a) AS deletedCount
    """
    results = execute_query(query=query, parameters={'Ar_ArtistID': Ar_ArtistID})
    return results and results[0]['deletedCount'] > 0


def update_artist_by_id(Ar_ArtistID: int, fields: dict):
    query = """
    MATCH (a:Artist {Ar_ArtistID: $Ar_ArtistID})
    SET
        a.Ar_FirstName = coalesce($Ar_FirstName, a.Ar_FirstName),
        a.Ar_LastName = coalesce($Ar_LastName, a.Ar_LastName),
        a.Ar_BirthDay = coalesce($Ar_BirthDay, a.Ar_BirthDay),
        a.Ar_Nationality = coalesce($Ar_Nationality, a.Ar_Nationality),
        a.Ar_Biography = coalesce($Ar_Biography, a.Ar_Biography),
        a.Ar_ImageURL = coalesce($Ar_ImageURL, a.Ar_ImageURL),
        a.Ar_DeathDay = coalesce($Ar_DeathDay, a.Ar_DeathDay),
        a.Ar_DeathYear = coalesce($Ar_DeathYear, a.Ar_DeathYear),
        a.Ar_CountryBirth = coalesce($Ar_CountryBirth, a.Ar_CountryBirth),
        a.Ar_CountryDeath = coalesce($Ar_CountryDeath, a.Ar_CountryDeath),
        a.Ar_Movement = coalesce($Ar_Movement, a.Ar_Movement)
    RETURN a
    """
    params = {
        'Ar_ArtistID': Ar_ArtistID,
        'Ar_FirstName': fields.get('Ar_FirstName'),
        'Ar_LastName': fields.get('Ar_LastName'),
        'Ar_BirthDay': fields.get('Ar_BirthDay'),
        'Ar_Nationality': fields.get('Ar_Nationality'),
        'Ar_Biography': fields.get('Ar_Biography'),
        'Ar_ImageURL': fields.get('Ar_ImageURL'),
        'Ar_DeathDay': fields.get('Ar_DeathDay'),
        'Ar_DeathYear': fields.get('Ar_DeathYear'),
        'Ar_CountryBirth': fields.get('Ar_CountryBirth'),
        'Ar_CountryDeath': fields.get('Ar_CountryDeath'),
        'Ar_Movement': fields.get('Ar_Movement')
    }
    results = execute_query(query=query, parameters=params)
    return results[0]['a'] if results else None



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

def delete_relation(Ar_ArtistID: int, Art_ArtworkID: int):
    query = """
    MATCH (artist:Artist {Ar_ArtistID: $Ar_ArtistID})-[r:CREATED]->(artwork:Artwork {Art_ArtworkID: $Art_ArtworkID})
    DELETE r
    RETURN artist, artwork
    """
    params = {
        'Ar_ArtistID': Ar_ArtistID,
        'Art_ArtworkID': Art_ArtworkID
    }
    results = execute_query(query=query, parameters=params)
    return results[0] if results else None

def update_relation(old_artist_id: int, new_artist_id: int, artwork_id: int):
    query = """
    MATCH (old_artist:Artist {Ar_ArtistID: $old_artist_id})-[r:CREATED]->(artwork:Artwork {Art_ArtworkID: $artwork_id})
    DELETE r
    WITH artwork
    MATCH (new_artist:Artist {Ar_ArtistID: $new_artist_id})
    MERGE (new_artist)-[:CREATED]->(artwork)
    RETURN new_artist, artwork
    """
    params = {
        'old_artist_id': old_artist_id,
        'new_artist_id': new_artist_id,
        'artwork_id': artwork_id
    }
    results = execute_query(query=query, parameters=params)
    return results[0] if results else None





def get_artist_by_page(page_number: int, page_size: int = 16, recherche: str = ""):
    """
    Récupère les artistes par page avec recherche optionnelle incluant nom, nationalité, dates et mouvements.
    """
    if page_number < 1:
        raise ValueError("Le numéro de page doit être supérieur ou égal à 1")

    offset = (page_number - 1) * page_size

    if recherche:
        query = f"""
        MATCH (artist:Artist)
        WHERE toString(artist.Ar_BirthDay) CONTAINS toString($recherche)
           OR toString(artist.Ar_DeathYear) CONTAINS toString($recherche)
           OR any(mov IN artist.Ar_Movement WHERE toLower(mov) CONTAINS toLower($recherche))
           OR toLower(artist.Ar_LastName) CONTAINS toLower($recherche)
           OR toLower(artist.Ar_FirstName) CONTAINS toLower($recherche)
           OR toLower(artist.Ar_Nationality) CONTAINS toLower($recherche)
        RETURN artist
        ORDER BY artist.Ar_ArtistID
        SKIP {offset}
        LIMIT {page_size}
        """
        parameters = {"recherche": recherche}
    else:
        query = f"""
        MATCH (artist:Artist)
        RETURN artist
        ORDER BY artist.Ar_ArtistID
        SKIP {offset}
        LIMIT {page_size}
        """
        parameters = {}

    results = execute_query(query=query, parameters=parameters)
    artist_list = [record['artist'] for record in results]

    return artist_list




def get_total_artist_count(recherche: str = ""):
    """
    Récupère le nombre total d'artistes (avec ou sans filtre).
    """
    if recherche:
        query = """
        MATCH (artist:Artist)
        WHERE toLower(artist.nom) CONTAINS toLower($recherche)
           OR toLower(artist.prenom) CONTAINS toLower($recherche)
        RETURN count(artist) AS total
        """
        parameters = {"recherche": recherche}
    else:
        query = "MATCH (artist:Artist) RETURN count(artist) as total"
        parameters = {}

    results = execute_query(query=query, parameters=parameters)
    return results[0]['total'] if results else 0



def get_artist_pagination_info(page_number: int, page_size: int = 16, recherche: str = ""):
    """
    Récupère les artistes avec infos de pagination et filtre optionnel.
    """
    total_count = get_total_artist_count(recherche)
    total_pages = (total_count + page_size - 1) // page_size

    artist_list = get_artist_by_page(page_number, page_size, recherche)

    return {
        'artists': artist_list,
        'current_page': page_number,
        'page_size': page_size,
        'total_count': total_count,
        'total_pages': total_pages,
        'has_next': page_number < total_pages,
        'has_previous': page_number > 1
    }
