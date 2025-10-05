import boto3
from botocore.exceptions import ClientError
import os
from typing import Optional
import logging
from datetime import datetime, timedelta

from app.core.config import settings

logger = logging.getLogger(__name__)

class StorageService:
    def __init__(self):
        self.bucket_name = settings.S3_BUCKET
        self.client = boto3.client(
            's3',
            endpoint_url=settings.S3_ENDPOINT,
            aws_access_key_id=settings.S3_ACCESS_KEY,
            aws_secret_access_key=settings.S3_SECRET_KEY
        )
    
    def upload_project_file(self, user_id: str, project_id: str, content: str, file_type: str = "html") -> Optional[str]:
        """Upload project file to storage"""
        try:
            key = f"projects/{user_id}/{project_id}/{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.{file_type}"
            
            self.client.put_object(
                Bucket=self.bucket_name,
                Key=key,
                Body=content,
                ContentType='text/html' if file_type == 'html' else 'application/json'
            )
            
            return key
        except ClientError as e:
            logger.error(f"Error uploading project file: {str(e)}")
            return None
    
    def generate_presigned_url(self, key: str, expires_in: int = 3600) -> Optional[str]:
        """Generate presigned URL for accessing stored files"""
        try:
            url = self.client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': key},
                ExpiresIn=expires_in
            )
            return url
        except ClientError as e:
            logger.error(f"Error generating presigned URL: {str(e)}")
            return None
    
    def delete_project_files(self, user_id: str, project_id: str) -> bool:
        """Delete all files for a project"""
        try:
            # List all objects with the project prefix
            objects_to_delete = []
            paginator = self.client.get_paginator('list_objects_v2')
            
            for page in paginator.paginate(
                Bucket=self.bucket_name,
                Prefix=f"projects/{user_id}/{project_id}/"
            ):
                if 'Contents' in page:
                    objects_to_delete.extend([{'Key': obj['Key']} for obj in page['Contents']])
            
            if objects_to_delete:
                self.client.delete_objects(
                    Bucket=self.bucket_name,
                    Delete={'Objects': objects_to_delete}
                )
            
            return True
        except ClientError as e:
            logger.error(f"Error deleting project files: {str(e)}")
            return False

# Global instance
storage_service = StorageService()
