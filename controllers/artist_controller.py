from flask import Blueprint, request, Response
import services.artist_service as artist_service
from utils.function import send_response, send_error, check_date

artist_controller = Blueprint('artists', __name__, url_prefix='/artists')


@artist_controller.route('', methods=['GET'])
def get_artists() -> tuple[Response, int]:
    artists = artist_service.get_artists()
    return send_response(data=artists)

@artist_controller.route('/<int:artist_id>', methods=['GET'])
def get_artist_by_id(artist_id: int) -> tuple[Response, int]:
    artist = artist_service.get_artist_by_id(artist_id)
    if artist:
        return send_response(data=artist)
    else:
        return send_error(status=404, message="Artist not found")



@artist_controller.route('', methods=['POST'])
def post_artist() -> tuple[Response, int]:

    # Required field : Ar_FirstName, Ar_LastName, Ar_BirthDay, Ar_Nationality, Ar_Biography, Ar_ImageURL
    # Optionnal field : Ar_DeathDay, Ar_CountryBirth, Ar_CountryDeath, Ar_Movement

    data = request.get_json()

    if not data or 'Ar_FirstName' not in data:
        return send_error(status=400, message="Ar_FirstName is required")
    
    if not data or 'Ar_LastName' not in data:
        return send_error(status=400, message="Ar_LastName is required")
    
    if not data or 'Ar_BirthDay' not in data:
        return send_error(status=400, message="Ar_BirthDay is required")
    
    if not data or 'Ar_Nationality' not in data:
        return send_error(status=400, message="Ar_Nationality is required")
    
    if not data or 'Ar_Biography' not in data:
        return send_error(status=400, message="Ar_Biography is required")
    
    if not data or 'Ar_ImageURL' not in data:
        return send_error(status=400, message="Ar_ImageURL is required")

    
    Ar_FirstName: str = data['Ar_FirstName']
    Ar_LastName: str = data['Ar_LastName']
    Ar_BirthDay: str = data['Ar_BirthDay']
    Ar_Nationality: str = data['Ar_Nationality']
    Ar_Biography: str = data['Ar_Biography']
    Ar_ImageURL: str = data['Ar_ImageURL']

    Ar_DeathDay = data.get('Ar_DeathDay', "")
    Ar_CountryBirth = data.get('Ar_CountryBirth', "")
    Ar_CountryDeath = data.get('Ar_CountryDeath', "")
    Ar_Movement = data.get('Ar_Movement', [])

    if not check_date(Ar_BirthDay):
        return send_error(status=400, message="Ar_BirthDay must be a valid date")
    
    if Ar_DeathDay and not check_date(Ar_DeathDay):
        return send_error(status=400, message="Ar_BirthDay must be a valid date")
    

    try:
        new_artist = artist_service.post_artist(Ar_FirstName, Ar_LastName, Ar_BirthDay, Ar_Nationality, Ar_Biography, Ar_ImageURL, Ar_DeathDay, Ar_CountryBirth, Ar_CountryDeath, Ar_Movement)

        if new_artist:
            return send_response(status=201, messages="Artist created", data=new_artist)
        else:
            return send_error(status=500, message="Failed to create artist. Please try again later.")
    except Exception as e:
        return send_error(status=500, message="An unexpected error occurred. Please try again later.")

@artist_controller.route('/page/<int:page_number>', methods=['GET'])
def get_artist(page_number: int) -> tuple[Response, int]:
    if page_number < 1:
        return send_error(status=400, message="page_number is already superior or egal to 1")

    info_artists = artist_service.get_artist_pagination_info(page_number)

    if info_artists:
        return send_response(data=info_artists)
    else:
        return send_error(status=404, message="Artists not found")

@artist_controller.route('/<int:artist_id>/artworks', methods=['GET'])
def get_artist_with_artworks(artist_id: int) -> tuple[Response, int]:
    artist_with_artworks = artist_service.get_artist_with_artworks(artist_id)
    if artist_with_artworks:
        return send_response(data=artist_with_artworks)
    else:
        return send_error(status=404, message="Artist not found")


@artist_controller.route('/<int:artist_id>/artworks', methods=['POST'])
def post_create_relation(artist_id: int) -> tuple[Response, int]:

    # Required field : Art_ArtworkID

    data = request.get_json()

    if not data or 'Art_ArtworkID' not in data:
        return send_error(status=400, message="Art_ArtworkID is required")

    Art_ArtworkID: int = data['Art_ArtworkID']

    try:
        relation = artist_service.post_create_relation(artist_id, Art_ArtworkID)

        if relation:
            return send_response(status=201, messages="Relation created", data=relation)
        else:
            return send_error(status=500, message="Failed to create created relation. Please try again later.")
    except Exception as e:
        return send_error(status=500, message="An unexpected error occurred. Please try again later.")

@artist_controller.route('/<int:artist_id>', methods=['PUT'])
def update_artist(artist_id: int) -> tuple[Response, int]:
    data = request.get_json()

    if not data:
        return send_error(status=400, message="No data provided")

    if 'Ar_BirthDay' in data and not check_date(data['Ar_BirthDay']):
        return send_error(status=400, message="Ar_BirthDay must be a valid date")

    if 'Ar_DeathDay' in data and data['Ar_DeathDay'] and not check_date(data['Ar_DeathDay']):
        return send_error(status=400, message="Ar_DeathDay must be a valid date")

    try:
        updated_artist = artist_service.update_artist_by_id(artist_id, data)
        if updated_artist:
            return send_response(messages="Artist updated", data=updated_artist)
        else:
            return send_error(status=404, message="Artist not found")
    except Exception as e:
        return send_error(status=500, message="An unexpected error occurred. Please try again later.")


@artist_controller.route('/<int:artist_id>', methods=['DELETE'])
def delete_artist(artist_id: int) -> tuple[Response, int]:
    try:
        deleted = artist_service.delete_artist_by_id(artist_id)
        if deleted:
            return send_response(status=200, messages="Artist deleted")
        else:
            return send_error(status=404, message="Artist not found")
    except Exception as e:
        return send_error(status=500, message="An unexpected error occurred. Please try again later.")
