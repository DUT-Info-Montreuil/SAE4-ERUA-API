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
    # Optionnal field : Ar_DeathDay

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

    if not check_date(Ar_BirthDay):
        return send_error(status=400, message="Ar_BirthDay must be a valid date")
    
    if Ar_DeathDay and not check_date(Ar_DeathDay):
        return send_error(status=400, message="Ar_BirthDay must be a valid date")

    try:
        new_artist = artist_service.post_artist(Ar_FirstName, Ar_LastName, Ar_BirthDay, Ar_Nationality, Ar_Biography, Ar_ImageURL, Ar_DeathDay)

        if new_artist:
            return send_response(status=201, messages="Artist created", data=new_artist)
        else:
            return send_error(status=500, message="Failed to create artist. Please try again later.")
    except Exception as e:
        return send_error(status=500, message="An unexpected error occurred. Please try again later.")
