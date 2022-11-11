from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings

class MediaStorage(S3Boto3Storage):
    location = 'media'

    location = settings.PUBLIC_MEDIA_LOCATION

    default_acl = settings.PUBLIC_MEDIA_DEFAULT_ACL

    file_overwrite = False
