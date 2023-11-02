from django.core.exceptions import ValidationError
import magic

def validate_image_file(file):
    """ 
        This function is used to validate if an uploaded file is an image. The function validates if the user has uploaded a valid file 
        of type image. Accepted image file extensions/type are: .jpg, .jpeg & .png
    """
    accept = ['image/jpg', 'image/jpeg', 'image/png']
    file_mime_type = magic.from_buffer(file.read(2048), mime=True)

    if file_mime_type not in accept:
        raise ValidationError('Unsupported file type for profile picture!')