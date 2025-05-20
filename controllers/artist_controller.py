from flask import Blueprint, request, Response
import services.artist_service as artist_service
from utils.function import send_response, send_error, check_date

artist_controller = Blueprint('artists', __name__, url_prefix='/artists')


@artist_controller.route('', methods=['GET'])
def get_artists() -> tuple[Response, int]:
    artists = artist_service.get_artists()
    return send_response(data=artists)


@artist_controller.route('', methods=['POST'])
def post_artist() -> tuple[Response, int]:

    # Required field : Ar_FirstName, Ar_LastName, Ar_BirthDay
    # Optionnal field : NULL

    data = request.get_json()

    if not data or 'Ar_FirstName' not in data:
        return send_error(status=400, message="Ar_FirstName is required")
    
    if not data or 'Ar_LastName' not in data:
        return send_error(status=400, message="Ar_LastName is required")
    
    if not data or 'Ar_BirthDay' not in data:
        return send_error(status=400, message="Ar_BirthDay is required")

    
    Ar_FirstName: str = data['Ar_FirstName']
    Ar_LastName: str = data['Ar_LastName']
    Ar_BirthDay: str = data['Ar_BirthDay']

    if not check_date(Ar_BirthDay):
        return send_error(status=400, message="Ar_BirthDay must be a valid date")

    try:
        new_artist = artist_service.post_artist(Ar_FirstName, Ar_LastName, Ar_BirthDay)
        return send_response(status=201, messages="Artist created", data=new_artist)
    except Exception as e:
        return send_error(status=500, message="An unexpected error occurred. Please try again later.")
