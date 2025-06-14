from config.db_connection import execute_query
from typing import List, Optional, Dict, Any


def get_graph(
        nationalities: Optional[List[str]] = None,
        mediums: Optional[List[str]] = None,
        movements: Optional[List[str]] = None,
        year_min: Optional[str] = None,
        year_max: Optional[str] = None,
        exclude_artists: bool = False,
        exclude_artworks: bool = False
) -> List[Dict[str, Any]]:
    """
    Récupère les données du graphe avec filtres optionnels

    Args:
        nationalities: Liste des nationalités d'artistes à inclure
        mediums: Liste des médiums d'œuvres à inclure
        movements: Liste des mouvements artistiques à inclure
        year_min: Année minimale (pour œuvres et artistes)
        year_max: Année maximale (pour œuvres et artistes)
        exclude_artists: Exclure les artistes du résultat
        exclude_artworks: Exclure les œuvres du résultat

    Returns:
        Liste contenant les données du graphe filtré
    """

    # Construire les conditions de filtrage pour les artistes
    artist_conditions = []
    artist_params = {}

    if nationalities:
        artist_conditions.append("artist.Ar_Nationality IN $nationalities")
        artist_params['nationalities'] = nationalities

    if movements:
        artist_conditions.append("ANY(movement IN artist.Ar_Movement WHERE movement IN $movements)")
        artist_params['movements'] = movements

    if year_min is not None:
        artist_conditions.append("artist.Ar_BirthDay >= $year_min")
        artist_params['year_min'] = year_min + "-01-01"

    if year_max is not None:
        artist_conditions.append("artist.Ar_BirthDay <= $year_max")
        artist_params['year_max'] = year_max + "-01-01"

    # Construire les conditions de filtrage pour les œuvres
    artwork_conditions = []
    artwork_params = {}

    if mediums:
        artwork_conditions.append("artwork.Art_Medium IN $mediums")
        artwork_params['mediums'] = mediums

    if year_min is not None:
        artwork_conditions.append("artwork.Art_Year >= $year_min_art")
        artwork_params['year_min_art'] = year_min + "-01-01"

    if year_max is not None:
        artwork_conditions.append("artwork.Art_Year <= $year_max_art")
        artwork_params['year_max_art'] = year_max + "-01-01"

    # Construire les clauses WHERE
    artist_where = "WHERE " + " AND ".join(artist_conditions) if artist_conditions else ""
    artwork_where = "WHERE " + " AND ".join(artwork_conditions) if artwork_conditions else ""

    # Construire la requête principale
    query_parts = []

    # Partie artistes
    if not exclude_artists:
        artist_query = f"""
        CALL {{
          MATCH (artist:Artist)
          {artist_where}
          RETURN collect({{
                        data: artist,
                        id: id(artist),
                        type: 'Artist'
                      }}) AS artists
        }}"""
        query_parts.append(artist_query)
    else:
        query_parts.append("CALL { RETURN [] AS artists }")

    # Partie œuvres
    if not exclude_artworks:
        artwork_query = f"""
        CALL {{
          MATCH (artwork:Artwork)
          {artwork_where}
          RETURN collect({{
                        data: artwork,
                        id: id(artwork),
                        type: 'Artwork'
                      }}) AS artworks
        }}"""
        query_parts.append(artwork_query)
    else:
        query_parts.append("CALL { RETURN [] AS artworks }")

    # Partie relations - seulement entre nœuds non exclus
    relation_conditions = []
    if exclude_artists and exclude_artworks:
        # Si les deux sont exclus, pas de relations
        query_parts.append("CALL { RETURN [] AS relations }")
    else:
        # Construire les conditions pour les relations
        relation_filter = ""
        if exclude_artists:
            relation_filter = "WHERE NOT (n1:Artist OR n2:Artist)"
        elif exclude_artworks:
            relation_filter = "WHERE NOT (n1:Artwork OR n2:Artwork)"
        elif artist_conditions or artwork_conditions:
            # Si on a des filtres, on doit s'assurer que les nœuds dans les relations respectent les filtres
            relation_subqueries = []

            if artist_conditions:
                relation_subqueries.append(f"""
                    (NOT n1:Artist OR ({" AND ".join(n.replace("artist.", "n1.") for n in artist_conditions)}))
                    AND (NOT n2:Artist OR ({" AND ".join(n.replace("artist.", "n2.") for n in artist_conditions)}))
                """)

            if artwork_conditions:
                relation_subqueries.append(f"""
                    (NOT n1:Artwork OR ({" AND ".join(n.replace("artwork.", "n1.") for n in artwork_conditions)}))
                    AND (NOT n2:Artwork OR ({" AND ".join(n.replace("artwork.", "n2.") for n in artwork_conditions)}))
                """)

            if relation_subqueries:
                relation_filter = f"WHERE {' AND '.join(relation_subqueries)}"

        relations_query = f"""
        CALL {{
          MATCH (n1)-[relation]->(n2)
          {relation_filter}
          RETURN collect({{
                        source: id(n1),
                        target: id(n2)
                      }}) AS relations
        }}"""
        query_parts.append(relations_query)

    # Assembler la requête finale
    query = "\n".join(query_parts) + "\nRETURN artists, artworks, relations"

    # Combiner tous les paramètres
    all_params = {**artist_params, **artwork_params}

    # Exécuter la requête
    results = execute_query(query=query, parameters=all_params if all_params else None)

    return results


def get_filter_options() -> Dict[str, List[str]]:
    """
    Récupère toutes les options disponibles pour les filtres

    Returns:
        Dictionnaire contenant les listes d'options pour chaque filtre
    """

    # Récupérer les nationalités
    nationality_query = """
    MATCH (artist:Artist)
    WHERE artist.Ar_Nationality IS NOT NULL
    RETURN DISTINCT artist.Ar_Nationality AS nationality
    ORDER BY nationality
    """

    # Récupérer les médiums
    medium_query = """
    MATCH (artwork:Artwork)
    WHERE artwork.Art_Medium IS NOT NULL
    RETURN DISTINCT artwork.Art_Medium AS medium
    ORDER BY medium
    """

    # Récupérer les mouvements
    movement_query = """
    MATCH (artist:Artist)
    WHERE artist.Ar_Movement IS NOT NULL
    UNWIND artist.Ar_Movement AS movement
    RETURN DISTINCT movement
    ORDER BY movement
    """

    # Récupérer les plages d'années
    year_query = """
    CALL {
        MATCH (artist:Artist)
        WHERE artist.Ar_BirthDay IS NOT NULL
        RETURN artist.Ar_BirthDay AS year
        UNION
        MATCH (artwork:Artwork)
        WHERE artwork.Art_Year IS NOT NULL
        RETURN artwork.Art_Year AS year
    }
    RETURN MIN(year) AS min_year, MAX(year) AS max_year
    """

    try:
        # Exécuter les requêtes
        nationalities = [record['nationality'] for record in execute_query(nationality_query)]
        mediums = [record['medium'] for record in execute_query(medium_query)]
        movements = [record['movement'] for record in execute_query(movement_query)]
        year_range = execute_query(year_query)[0] if execute_query(year_query) else {'min_year': 1800, 'max_year': 2024}

        return {
            'nationalities': nationalities,
            'mediums': mediums,
            'movements': movements,
            'year_range': {
                'min': year_range['min_year'],
                'max': year_range['max_year']
            }
        }
    except Exception as e:
        print(f"Erreur lors de la récupération des options de filtres: {e}")
        return {
            'nationalities': [],
            'mediums': [],
            'movements': [],
            'year_range': {'min': 1800, 'max': 2024}
        }