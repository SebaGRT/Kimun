"""
Custom Supabase Storage Backend that fixes path handling.

The django-supabase-storage package has a bug where _save prepends folder_path
but _open doesn't, causing uploaded files to be stored at media/<path> but 
downloaded from <path> (without the media/ prefix).
"""

from django_supabase_storage.storage_backends import SupabaseMediaStorage


class FixedSupabaseMediaStorage(SupabaseMediaStorage):
    """
    Fixed storage backend that uses consistent path handling.
    """

    def _open(self, name, mode='rb'):
        """Open/download a file from Supabase with correct path."""
        from io import BytesIO
        import logging

        logger = logging.getLogger(__name__)
        name = str(name).lstrip('/')

        # Use the same path construction as _save
        path = f"{self.folder_path}/{name}" if self.folder_path else name
        logger.info(f"Opening file from Supabase: {self.bucket_name}/{path}")

        try:
            data = self.client.storage.from_(self.bucket_name).download(path)
            logger.info(f"✓ File opened: {path}")
            return BytesIO(data)
        except Exception as e:
            error_msg = f"Failed to download {path}: {str(e)}"
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)

    def delete(self, name):
        """Delete a file from Supabase with correct path."""
        import logging

        logger = logging.getLogger(__name__)
        if not name:
            return

        name = str(name).lstrip('/')
        path = f"{self.folder_path}/{name}" if self.folder_path else name
        logger.info(f"Deleting from Supabase: {self.bucket_name}/{path}")

        try:
            self.client.storage.from_(self.bucket_name).remove([path])
            logger.info(f"✓ Deleted: {path}")
        except Exception as e:
            logger.warning(f"Could not delete {path}: {str(e)}")

    def exists(self, name):
        """Check if file exists in Supabase with correct path."""
        if not name:
            return False

        name = str(name).lstrip('/')
        path = f"{self.folder_path}/{name}" if self.folder_path else name

        try:
            self.client.storage.from_(self.bucket_name).get_metadata(path)
            return True
        except Exception:
            return False

    def size(self, name):
        """Get file size in bytes with correct path."""
        if not name:
            return 0

        name = str(name).lstrip('/')
        path = f"{self.folder_path}/{name}" if self.folder_path else name

        try:
            metadata = self.client.storage.from_(self.bucket_name).get_metadata(path)
            size = metadata.get('metadata', {}).get('size', 0)
            return size
        except Exception:
            return 0

    def url(self, name):
        """Get public URL for a file with correct path."""
        if not name:
            return ''

        name = str(name).lstrip('/')
        path = f"{self.folder_path}/{name}" if self.folder_path else name

        url = f"{self.supabase_url}/storage/v1/object/public/{self.bucket_name}/{path}"
        return url

    def get_created_time(self, name):
        """Get file creation time with correct path."""
        if not name:
            return None

        name = str(name).lstrip('/')
        path = f"{self.folder_path}/{name}" if self.folder_path else name

        try:
            metadata = self.client.storage.from_(self.bucket_name).get_metadata(path)
            return metadata.get('created_at')
        except Exception:
            return None

    def get_modified_time(self, name):
        """Get file modification time with correct path."""
        if not name:
            return None

        name = str(name).lstrip('/')
        path = f"{self.folder_path}/{name}" if self.folder_path else name

        try:
            metadata = self.client.storage.from_(self.bucket_name).get_metadata(path)
            return metadata.get('updated_at')
        except Exception:
            return None
