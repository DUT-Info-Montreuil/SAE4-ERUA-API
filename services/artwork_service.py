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


def post_artwork(Art_Title: str, Art_Year: int, Art_Description: str, Art_ImageURL: str, Art_Medium: str,
                 Art_Dimensions: str):
    query = """
    MERGE (c:Counter {name: 'Art_ArtworkID'})
    ON CREATE SET c.count = 0
    SET c.count = c.count + 1
    WITH c.count AS new_id
    CREATE (aw:Artwork {Art_ArtworkID: new_id, Art_Title: $Art_Title, Art_Year: $Art_Year, 
    Art_Description: $Art_Description, Art_ImageURL: $Art_ImageURL, Art_Medium: $Art_Medium, Art_Dimensions: 
    $Art_Dimensions})
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


def get_artwork_by_page(page_number: int, page_size: int = 16):
    """
    Récupère les artworks par page avec pagination.

    Args:
        page_number (int): Numéro de la page (commence à 1)
        page_size (int): Nombre d'artworks par page (par défaut 16)

    Returns:
        list: Liste des artworks pour la page demandée
    """
    if page_number < 1:
        raise ValueError("Le numéro de page doit être supérieur ou égal à 1")

    offset = (page_number - 1) * page_size

    query = f"""
    MATCH (artwork:Artwork) 
    RETURN artwork 
    ORDER BY artwork.id 
    SKIP {offset} 
    LIMIT {page_size}
    """
    results = execute_query(query=query)
    artwork_list = [record['artwork'] for record in results]

    return artwork_list


def get_total_artwork_count():
    """
    Récupère le nombre total d'artworks pour calculer le nombre de pages.

    Returns:
        int: Nombre total d'artworks
    """
    query = "MATCH (artwork:Artwork) RETURN count(artwork) as total"
    results = execute_query(query=query)
    return results[0]['total'] if results else 0


def get_artwork_pagination_info(page_number: int, page_size: int = 16):
    """
    Récupère les artworks avec des informations de pagination.

    Args:
        page_number (int): Numéro de la page
        page_size (int): Nombre d'artworks par page

    Returns:
        dict: Dictionnaire contenant les artworks et les infos de pagination
    """
    total_count = get_total_artwork_count()
    total_pages = (total_count + page_size - 1) // page_size

    artwork_list = get_artwork_by_page(page_number, page_size)

    return {
        'artworks': artwork_list,
        'current_page': page_number,
        'page_size': page_size,
        'total_count': total_count,
        'total_pages': total_pages,
        'has_next': page_number < total_pages,
        'has_previous': page_number > 1
    }

