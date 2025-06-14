from config.db_connection import execute_query


def get_artwork():
    query: str = "MATCH (Artwork :Artwork) RETURN Artwork"
    results: list = execute_query(query=query)
    artwork: list = [record['Artwork'] for record in results]

    return artwork


def get_artwork_by_id(Art_ArtworkID: int):
    query = """
    MATCH (a:Artwork {Art_ArtworkID: $Art_ArtworkID})
    RETURN a
    """
    results = execute_query(query=query, parameters={'Art_ArtworkID': Art_ArtworkID})
    if results:
        return results[0]['a']
    return None


def post_artwork(Art_Title: str, Art_Year: int, Art_Description: str, Art_ImageURL: str, Art_Medium: str,
                 Art_Dimensions: str, Ar_ArtistID: int = ""):
    query = """
    MERGE (c:Counter {name: 'Art_ArtworkID'})
    ON CREATE SET c.count = 0
    SET c.count = c.count + 1
    WITH c.count AS new_id
    CREATE (aw:Artwork {Art_ArtworkID: new_id, Art_Title: $Art_Title, Art_Year: $Art_Year, 
    Art_Description: $Art_Description, Art_ImageURL: $Art_ImageURL, Art_Medium: $Art_Medium, Art_Dimensions: 
    $Art_Dimensions, Ar_ArtistID: $Ar_ArtistID})
    RETURN aw AS Artwork
    """
    params = {
        'Art_Title': Art_Title,
        'Art_Year': Art_Year,
        'Art_Description': Art_Description,
        'Art_ImageURL': Art_ImageURL,
        'Art_Medium': Art_Medium,
        'Art_Dimensions': Art_Dimensions,
        'Ar_ArtistID': Ar_ArtistID
    }

    results = execute_query(query=query, parameters=params)
    if results:
        return results[0]['Artwork']
    return None


def post_inspire_relation(source_artwork_id: int, inspired_artwork_id: int):
    """
    Crée une relation 'INSPIRE' entre deux œuvres
    source_artwork_id: l'œuvre qui inspire
    inspired_artwork_id: l'œuvre inspirée
    """
    query = """
    MATCH (source:Artwork {Art_ArtworkID: $source_artwork_id})
    MATCH (inspired:Artwork {Art_ArtworkID: $inspired_artwork_id})
    MERGE (source)-[r:INSPIRE]->(inspired)
    RETURN r, source, inspired
    """

    params = {
        'source_artwork_id': source_artwork_id,
        'inspired_artwork_id': inspired_artwork_id
    }

    results = execute_query(query=query, parameters=params)
    return results[0] if results else None


def get_artworks_inspired_by(Art_ArtworkID: int):
    """
    Récupère toutes les œuvres inspirées par une œuvre donnée
    """
    query = """
    MATCH (source:Artwork {Art_ArtworkID: $Art_ArtworkID})-[:INSPIRE]->(inspired:Artwork)
    RETURN inspired
    """

    results = execute_query(query=query, parameters={'Art_ArtworkID': Art_ArtworkID})
    return [record['inspired'] for record in results]


def get_artworks_that_inspired(Art_ArtworkID: int):
    """
    Récupère toutes les œuvres qui ont inspiré une œuvre donnée
    """
    query = """
    MATCH (source:Artwork)-[:INSPIRE]->(inspired:Artwork {Art_ArtworkID: $Art_ArtworkID})
    RETURN source
    """

    results = execute_query(query=query, parameters={'Art_ArtworkID': Art_ArtworkID})
    return [record['source'] for record in results]


def get_artwork_with_inspirations(Art_ArtworkID: int):
    """
    Récupère une œuvre avec ses inspirations et les œuvres qu'elle a inspirées
    """
    query = """
    MATCH (artwork:Artwork {Art_ArtworkID: $Art_ArtworkID})
    OPTIONAL MATCH (source:Artwork)-[:INSPIRE]->(artwork)
    OPTIONAL MATCH (artwork)-[:INSPIRE]->(inspired:Artwork)
    RETURN artwork, 
           COLLECT(DISTINCT source) AS inspirations,
           COLLECT(DISTINCT inspired) AS inspired_artworks
    """

    results = execute_query(query=query, parameters={'Art_ArtworkID': Art_ArtworkID})
    if results:
        return {
            'artwork': results[0]['artwork'],
            'inspirations': results[0]['inspirations'],
            'inspired_artworks': results[0]['inspired_artworks']
        }
    return None


def get_artist_of_artwork(Art_ArtworkID: int):
    """
    Récupère l'artiste qui a créé une œuvre
    """
    query = """
    MATCH (artist:Artist)-[:CREATED]->(artwork:Artwork {Art_ArtworkID: $Art_ArtworkID})
    RETURN artist
    """

    results = execute_query(query=query, parameters={'Art_ArtworkID': Art_ArtworkID})
    if results:
        return results[0]['artist']
    return None


def get_artwork_by_page(page_number: int, page_size: int = 16,recherche: str = ""):
    """
    Récupère les artworks par page avec un éventuel filtre de recherche.

    Args:
        page_number (int): Numéro de la page
        page_size (int): Taille de page
        recherche (str): Chaîne de recherche (par titre ou artiste)

    Returns:
        list: Liste des artworks paginés
    """
    if page_number < 1:
        raise ValueError("Le numéro de page doit être supérieur ou égal à 1")

    offset = (page_number - 1) * page_size

    if recherche:
        query = f"""
            MATCH (artwork:Artwork)
            WHERE toLower(artwork.Art_Title) CONTAINS toLower($recherche)
               OR toLower(artwork.artist) CONTAINS toLower($recherche)
            RETURN artwork
            ORDER BY artwork.Art_ArtworkID
            SKIP {offset}
            LIMIT {page_size}
            """
        parameters = {"recherche": recherche}
    else:
        query = f"""
            MATCH (artwork:Artwork)
            RETURN artwork
            ORDER BY artwork.Art_ArtworkID
            SKIP {offset}
            LIMIT {page_size}
            """
        parameters = {}

    results = execute_query(query=query, parameters=parameters)
    return [record['artwork'] for record in results]


def get_total_artwork_count(recherche: str = ""):
    """
    Retourne le nombre total d'artworks (filtré si nécessaire).
    """
    if recherche:
        query = """
        MATCH (artwork:Artwork)
        WHERE toLower(artwork.Art_Title) CONTAINS toLower($recherche)
           OR toLower(artwork.artist) CONTAINS toLower($recherche)
        RETURN count(artwork) AS total
        """
        parameters = {"recherche": recherche}
    else:
        query = "MATCH (artwork:Artwork) RETURN count(artwork) AS total"
        parameters = {}

    results = execute_query(query=query, parameters=parameters)
    return results[0]['total'] if results else 0



def get_artwork_pagination_info(page_number: int, page_size: int = 16, recherche: str = ""):
    """
    Récupère les artworks + infos de pagination, avec filtrage optionnel.
    """
    total_count = get_total_artwork_count(recherche)
    total_pages = (total_count + page_size - 1) // page_size

    artworks = get_artwork_by_page(page_number, page_size, recherche)

    return {
        'artworks': artworks,
        'current_page': page_number,
        'page_size': page_size,
        'total_count': total_count,
        'total_pages': total_pages,
        'has_next': page_number < total_pages,
        'has_previous': page_number > 1
    }

def delete_artwork(Art_ArtworkID: int) -> bool:
    query = """
    MATCH (a:Artwork {Art_ArtworkID: $Art_ArtworkID})
    DETACH DELETE a
    RETURN COUNT(a) AS deleted_count
    """
    results = execute_query(query=query, parameters={'Art_ArtworkID': Art_ArtworkID})
    return results and results[0]['deleted_count'] > 0

def update_artwork(Art_ArtworkID: int, data: dict):
    query = """
    MATCH (a:Artwork {Art_ArtworkID: $Art_ArtworkID})
    SET a.Art_Title = coalesce($Art_Title, a.Art_Title),
        a.Art_Year = coalesce($Art_Year, a.Art_Year),
        a.Art_Description = coalesce($Art_Description, a.Art_Description),
        a.Art_ImageURL = coalesce($Art_ImageURL, a.Art_ImageURL),
        a.Art_Medium = coalesce($Art_Medium, a.Art_Medium),
        a.Art_Dimensions = coalesce($Art_Dimensions, a.Art_Dimensions),
        a.Ar_ArtistID = coalesce($Ar_ArtistID, a.Ar_ArtistID)
    RETURN a AS Artwork
    """
    params = {
        'Art_ArtworkID': Art_ArtworkID,
        'Art_Title': data.get('Art_Title'),
        'Art_Year': data.get('Art_Year'),
        'Art_Description': data.get('Art_Description'),
        'Art_ImageURL': data.get('Art_ImageURL'),
        'Art_Medium': data.get('Art_Medium'),
        'Art_Dimensions': data.get('Art_Dimensions'),
        'Ar_ArtistID': data.get('Ar_ArtistID')
    }
    results = execute_query(query=query, parameters=params)
    return results[0]['Artwork'] if results else None

