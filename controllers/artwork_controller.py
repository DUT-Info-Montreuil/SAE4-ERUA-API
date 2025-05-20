from flask import Blueprint, Response, request
import services.artwork_service as artwork_service
from utils.function import send_response, send_error, check_date

artwork_controller = Blueprint('artwork', __name__, url_prefix='/artwork')


@artwork_controller.route('', methods=['GET'])
def get_artwork() -> tuple[Response, int]:
    artwork = artwork_service.get_artwork()
    return send_response(data=artwork)


@artwork_controller.route('', methods=['POST'])
def post_artwork() -> tuple[Response, int]:

    # Required field : Art_Title, Art_Year, Art_Description
    # Optionnal field : NULL

    data = request.get_json()

    if not data or 'Art_Title' not in data:
        return send_error(status=400, message="Art_Title is required")
    
    if not data or 'Art_Year' not in data:
        return send_error(status=400, message="Art_Year is required")
    
    if not data or 'Art_Description' not in data:
        return send_error(status=400, message="Art_Description is required")
    
    if not data or 'Ar_FirstName' not in data:
        return send_error(status=400, message="Ar_FirstName is required")
    
    if not data or 'Ar_LastName' not in data:
        return send_error(status=400, message="Ar_LastName is required")
    

    Art_Title: str = data['Art_Title']
    Art_Year: str = data['Art_Year']
    Art_Description: str = data['Art_Description']
    Ar_FirstName: str = data['Ar_FirstName']
    Ar_LastName: str = data['Ar_LastName']

    if not check_date(Art_Year):
        return send_error(status=400, message="Art_Year must be a valid date")

    try:
        new_artwork = artwork_service.post_artwork(Art_Title, Art_Year, Art_Description, Ar_FirstName, Ar_LastName)
        return send_response(status=201, messages="Artwork created", data=new_artwork)
    except Exception as e:
        return send_error(status=500, message="An unexpected error occurred. Please try again later.")