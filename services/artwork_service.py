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


def get_artwork_by_page(page_number: int, page_size: int = 16):
    """
    Récupère les artworks par page avec pagination.

    Args:
        page_number (int): Numéro de la page (commence à 1)
        page_size (int): Nombre d'artworks par page (par défaut 16)

    Returns:
        list: Liste des artworks pour la page demandée
    """
    # Validation du numéro de page
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
    total_pages = (total_count + page_size - 1) // page_size  # Calcul du nombre total de pages

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

