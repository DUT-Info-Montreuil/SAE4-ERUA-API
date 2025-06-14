from flask import Blueprint, request, Response
import services.document_service as document_service
from utils.function import send_response, send_error

document_controller = Blueprint('documents', __name__, url_prefix='/documents')

@document_controller.route('', methods=['POST'])
def post_document() -> tuple[Response, int]:
    if 'file' not in request.files:
        return send_error(status=400, message="No file part in the request")

    file = request.files['file']

    if file.filename == '':
        return send_error(status=400, message="No selected file")

    try:
        url = document_service.upload_document(file)
        return send_response(status=201, messages="Document uploaded", data={"url": url})
    except Exception:
        return send_error(status=500, message="An error occurred during upload")