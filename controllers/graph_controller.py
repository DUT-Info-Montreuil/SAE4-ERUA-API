from flask import Blueprint, Response, request
from typing import List, Optional

from services import graph_service
from utils.function import send_response

graph_controller = Blueprint('graphs', __name__, url_prefix='/graphs')


@graph_controller.route('', methods=['GET'])
def get_graph() -> tuple[Response, int]:
    """
    Endpoint pour récupérer le graphe avec filtres optionnels

    Paramètres de requête supportés:
    - nationalities: Liste de nationalités séparées par des virgules
    - mediums: Liste de médiums séparés par des virgules
    - movements: Liste de mouvements séparés par des virgules
    - yearMin: Année minimale (entier)
    - yearMax: Année maximale (entier)
    - excludeArtists: 'true' pour exclure les artistes
    - excludeArtworks: 'true' pour exclure les œuvres
    """
    try:
        nationalities_param = request.args.get('nationalities')
        mediums_param = request.args.get('mediums')
        movements_param = request.args.get('movements')
        year_min_param = request.args.get('yearMin')
        year_max_param = request.args.get('yearMax')
        exclude_artists_param = request.args.get('excludeArtists')
        exclude_artworks_param = request.args.get('excludeArtworks')

        nationalities: Optional[List[str]] = None
        if nationalities_param:
            nationalities = [nat.strip() for nat in nationalities_param.split(',') if nat.strip()]

        mediums: Optional[List[str]] = None
        if mediums_param:
            mediums = [med.strip() for med in mediums_param.split(',') if med.strip()]

        movements: Optional[List[str]] = None
        if movements_param:
            movements = [mov.strip() for mov in movements_param.split(',') if mov.strip()]

        year_min: Optional[str] = None
        if year_min_param:
            try:
                year_min = year_min_param
            except ValueError:
                return send_response(400,"Paramètre yearMin invalide. Doit être un entier.")

        year_max: Optional[str] = None
        if year_max_param:
            try:
                year_max = year_max_param
            except ValueError:
                return send_response(400,"Paramètre yearMax invalide. Doit être un entier.")

        exclude_artists: bool = exclude_artists_param == 'true'
        exclude_artworks: bool = exclude_artworks_param == 'true'

        if exclude_artists and exclude_artworks:
            return send_response(400,"Impossible d'exclure à la fois les artistes et les œuvres.")

        if year_min is not None and year_max is not None and year_min > year_max:
            return send_response(400,"L'année minimale ne peut pas être supérieure à l'année maximale.")

        graph_data = graph_service.get_graph(
            nationalities=nationalities,
            mediums=mediums,
            movements=movements,
            year_min=year_min,
            year_max=year_max,
            exclude_artists=exclude_artists,
            exclude_artworks=exclude_artworks
        )

        return send_response(data=graph_data)

    except Exception as e:
        print(f"Erreur lors de la récupération du graphe filtré: {e}")
        return send_response(500,"Erreur interne lors de la récupération du graphe.")

@graph_controller.route('/subgraph/<int:central_node_id>', methods=['GET'])
def get_subgraph(central_node_id: int) -> tuple[Response, int]:
    """
    Endpoint pour récupérer un sous-graphe centré sur un nœud spécifique avec filtres optionnels

    Paramètres de requête supportés:
    - nationalities: Liste de nationalités séparées par des virgules
    - mediums: Liste de médiums séparés par des virgules
    - movements: Liste de mouvements séparés par des virgules
    - yearMin: Année minimale (entier)
    - yearMax: Année maximale (entier)
    - excludeArtists: 'true' pour exclure les artistes
    - excludeArtworks: 'true' pour exclure les œuvres
    """
    try:
        # Récupération des paramètres de requête (même logique que get_graph)
        nationalities_param = request.args.get('nationalities')
        mediums_param = request.args.get('mediums')
        movements_param = request.args.get('movements')
        year_min_param = request.args.get('yearMin')
        year_max_param = request.args.get('yearMax')
        exclude_artists_param = request.args.get('excludeArtists')
        exclude_artworks_param = request.args.get('excludeArtworks')

        nationalities: Optional[List[str]] = None
        if nationalities_param:
            nationalities = [nat.strip() for nat in nationalities_param.split(',') if nat.strip()]

        mediums: Optional[List[str]] = None
        if mediums_param:
            mediums = [med.strip() for med in mediums_param.split(',') if med.strip()]

        movements: Optional[List[str]] = None
        if movements_param:
            movements = [mov.strip() for mov in movements_param.split(',') if mov.strip()]

        year_min: Optional[str] = None
        if year_min_param:
            try:
                year_min = year_min_param
            except ValueError:
                return send_response(400, "Paramètre yearMin invalide. Doit être un entier.")

        year_max: Optional[str] = None
        if year_max_param:
            try:
                year_max = year_max_param
            except ValueError:
                return send_response(400, "Paramètre yearMax invalide. Doit être un entier.")

        exclude_artists: bool = exclude_artists_param == 'true'
        exclude_artworks: bool = exclude_artworks_param == 'true'

        if exclude_artists and exclude_artworks:
            return send_response(400, "Impossible d'exclure à la fois les artistes et les œuvres.")

        if year_min is not None and year_max is not None and year_min > year_max:
            return send_response(400, "L'année minimale ne peut pas être supérieure à l'année maximale.")

        # Appel au service avec le nouvel ID de nœud central
        subgraph_data = graph_service.get_subgraph(
            central_node_id=central_node_id,
            nationalities=nationalities,
            mediums=mediums,
            movements=movements,
            year_min=year_min,
            year_max=year_max,
            exclude_artists=exclude_artists,
            exclude_artworks=exclude_artworks
        )

        return send_response(data=subgraph_data)

    except Exception as e:
        print(f"Erreur lors de la récupération du sous-graphe filtré: {e}")
        return send_response(500, "Erreur interne lors de la récupération du sous-graphe.")

@graph_controller.route('/filter-options', methods=['GET'])
def get_filter_options() -> tuple[Response, int]:
    """
    Endpoint pour récupérer toutes les options disponibles pour les filtres
    """
    try:
        options = graph_service.get_filter_options()
        return send_response(data=options)

    except Exception as e:
        print(f"Erreur lors de la récupération des options de filtres: {e}")
        return send_response(500,"Erreur interne lors de la récupération des options de filtres.")
