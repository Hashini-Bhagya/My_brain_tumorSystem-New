import cloudinary
import cloudinary.uploader
import cloudinary.api
from config import Config

# Configure Cloudinary
cloudinary.config(
    cloud_name=Config.CLOUDINARY_CLOUD_NAME,
    api_key=Config.CLOUDINARY_API_KEY,
    api_secret=Config.CLOUDINARY_API_SECRET
)

def upload_image(file):
    """Upload image to Cloudinary and return the URL"""
    try:
        result = cloudinary.uploader.upload(
            file,
            folder="brain_tumor_scans",
            resource_type="image"
        )
        return result['secure_url'], None
    except Exception as e:
        return None, str(e)