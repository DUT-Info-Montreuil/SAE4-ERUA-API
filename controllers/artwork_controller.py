from flask import Blueprint, Response, request
import services.artwork_service as artwork_service
from utils.function import send_response, send_error, check_date

artwork_controller = Blueprint('artworks', __name__, url_prefix='/artworks')


@artwork_controller.route('', methods=['GET'])
def get_artwork() -> tuple[Response, int]:
    artwork = artwork_service.get_artwork()
    return send_response(data=artwork)


@artwork_controller.route('/<int:artwork_id>', methods=['GET'])
def get_artwork_by_id(artwork_id: int) -> tuple[Response, int]:
    artwork = artwork_service.get_artwork_by_id(artwork_id)
    if artwork:
        return send_response(data=artwork)
    else:
        return send_error(status=404, message="Artwork not found")


@artwork_controller.route('', methods=['POST'])
def post_artwork() -> tuple[Response, int]:
    # Required fields : Art_Title, Art_Year, Art_Description, Art_ImageURL, Art_Medium, Art_Dimensions
    # Optional field : Ar_ArtistID

    data = request.get_json()

    if not data or 'Art_Title' not in data:
        return send_error(status=400, message="Art_Title is required")
    
    if not data or 'Art_Year' not in data:
        return send_error(status=400, message="Art_Year is required")
    
    if not data or 'Art_Description' not in data:
        return send_error(status=400, message="Art_Description is required")
    
    if not data or 'Art_ImageURL' not in data:
        return send_error(status=400, message="Art_ImageURL is required")
    
    if not data or 'Art_Medium' not in data:
        return send_error(status=400, message="Art_Medium is required")
    
    if not data or 'Art_Dimensions' not in data:
        return send_error(status=400, message="Art_Dimensions is required")

    Art_Title: str = data['Art_Title']
    Art_Year: str = data['Art_Year']
    Art_Description: str = data['Art_Description']
    Art_ImageURL: str = data['Art_ImageURL']
    Art_Medium: str = data['Art_Medium']
    Art_Dimensions: str = data['Art_Dimensions']

    Ar_ArtistID: int = data.get('Ar_ArtistID', "")

    if not check_date(Art_Year):
        return send_error(status=400, message="Art_Year must be a valid date")

    try:
        new_artwork = artwork_service.post_artwork(
            Art_Title, Art_Year, Art_Description, Art_ImageURL, Art_Medium,
            Art_Dimensions, Ar_ArtistID
        )
        return send_response(status=201, messages="Artwork created", data=new_artwork)
    except Exception as e:
        return send_error(status=500, message="An unexpected error occurred. Please try again later.")



@artwork_controller.route('/<int:artwork_id>/inspires', methods=['GET'])
def get_artworks_inspired_by(artwork_id: int) -> tuple[Response, int]:
    artworks = artwork_service.get_artworks_inspired_by(artwork_id)
    if artworks:
        return send_response(data=artworks)
    else:
        return send_error(status=404, message="Artwork not found")


@artwork_controller.route('/<int:artwork_id>/inspired', methods=['GET'])
def get_artworks_that_inspired(artwork_id: int) -> tuple[Response, int]:
    artworks = artwork_service.get_artworks_that_inspired(artwork_id)
    if artworks:
        return send_response(data=artworks)
    else:
        return send_error(status=404, message="Artwork not found")


@artwork_controller.route('/<int:artwork_id>/inspirations', methods=['GET'])
def get_artwork_with_inspirations(artwork_id: int) -> tuple[Response, int]:
    artwork_with_inspirations = artwork_service.get_artwork_with_inspirations(artwork_id)
    if artwork_with_inspirations:
        return send_response(data=artwork_with_inspirations)
    else:
        return send_error(status=404, message="Artwork not found")


@artwork_controller.route('/<int:artwork_id>/artist', methods=['GET'])
def get_artist_of_artwork(artwork_id: int) -> tuple[Response, int]:
    artist = artwork_service.get_artist_of_artwork(artwork_id)
    if artist:
        return send_response(data=artist)
    else:
        return send_error(status=404, message="No artist found for this artwork")


@artwork_controller.route('/<int:artwork_id>/inspire', methods=['POST'])
def post_inspire_relation(artwork_id: int) -> tuple[Response, int]:

    # Required field : Art_InspiredArtworkID

    data = request.get_json()

    if not data or 'Art_InspiredArtworkID' not in data:
        return send_error(status=400, message="Art_InspiredArtworkID is required")

    Art_InspiredArtworkID: int = data['Art_InspiredArtworkID']

    try:
        relation = artwork_service.post_inspire_relation(artwork_id, Art_InspiredArtworkID)

        if relation:
            return send_response(status=201, messages="Inspiration relation created", data=relation)
        else:
            return send_error(status=500, message="Failed to create inspiration relation. Please try again later.")
    except Exception as e:
        return send_error(status=500, message="An unexpected error occurred. Please try again later.")
    

@artwork_controller.route('/<int:artwork_id>', methods=['DELETE'])
def delete_artwork(artwork_id: int) -> tuple[Response, int]:
    try:
        deleted = artwork_service.delete_artwork(artwork_id)
        if deleted:
            return send_response(messages="Artwork deleted")
        else:
            return send_error(status=404, message="Artwork not found")
    except Exception as e:
        return send_error(status=500, message="An unexpected error occurred. Please try again later.")


@artwork_controller.route('/<int:artwork_id>', methods=['PUT'])
def update_artwork(artwork_id: int) -> tuple[Response, int]:
    data = request.get_json()
    if not data:
        return send_error(status=400, message="Invalid data")

    try:
        updated_artwork = artwork_service.update_artwork(artwork_id, data)
        if updated_artwork:
            return send_response(messages="Artwork updated", data=updated_artwork)
        else:
            return send_error(status=404, message="Artwork not found")
    except Exception as e:
        return send_error(status=500, message="An unexpected error occurred. Please try again later.")
