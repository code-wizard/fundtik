from django.core.files.storage import FileSystemStorage

# Use local filesystem storage for all files
class PublicMediaStorage(FileSystemStorage):
    def __init__(self, *args, **kwargs):
        super().__init__(location=None, base_url=None, *args, **kwargs)

class PrivateMediaStorage(FileSystemStorage):
    def __init__(self, *args, **kwargs):
        super().__init__(location=None, base_url=None, *args, **kwargs)