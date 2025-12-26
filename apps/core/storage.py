"""
Backblaze B2 Storage Configuration
Django storage backend for Backblaze B2 cloud storage.
"""

from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class BackblazeB2Storage(S3Boto3Storage):
    """
    Custom storage backend for Backblaze B2.
    Uses S3-compatible API provided by Backblaze.
    """
    
    # Override bucket name from settings
    bucket_name = settings.B2_BUCKET_NAME
    
    # Use custom domain if set
    custom_domain = settings.B2_BUCKET_URL.replace('https://', '') if settings.B2_BUCKET_URL else None
    
    # B2 S3-compatible endpoint
    endpoint_url = f"https://s3.{getattr(settings, 'B2_REGION', 'us-west-004')}.backblazeb2.com"
    
    # Access keys
    access_key = settings.B2_APPLICATION_KEY_ID
    secret_key = settings.B2_APPLICATION_KEY
    
    # File settings
    file_overwrite = False
    default_acl = 'public-read'
    
    # Cache control for better performance
    object_parameters = {
        'CacheControl': 'max-age=86400',
    }


class BackblazeB2MediaStorage(BackblazeB2Storage):
    """Storage for user-uploaded media files"""
    location = 'media'


class BackblazeB2StaticStorage(BackblazeB2Storage):
    """Storage for static files (optional - usually served from CDN)"""
    location = 'static'


def get_b2_storage():
    """Helper function to get configured B2 storage or fall back to local storage"""
    if all([
        settings.B2_APPLICATION_KEY_ID,
        settings.B2_APPLICATION_KEY,
        settings.B2_BUCKET_NAME,
    ]):
        return BackblazeB2MediaStorage()
    else:
        # Fall back to local file storage if B2 not configured
        from django.core.files.storage import FileSystemStorage
        return FileSystemStorage()
