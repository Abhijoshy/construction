"""
AWS CloudWatch Logger Library - A custom object-oriented library for Django CloudWatch integration
This library provides meaningful functionality for logging construction project activities to AWS CloudWatch
"""

import boto3
import json
from datetime import datetime
from typing import Dict, Any, List, Optional


class CloudWatchLogger:
    """
    Object-oriented CloudWatch logging library for construction project activities
    """
    
    def __init__(self, log_group_name: str, region_name: str = 'eu-north-1'):
        """
        Initialize CloudWatch Logger
        
        Args:
            log_group_name: AWS CloudWatch log group name
            region_name: AWS region name
        """
        self.log_group_name = log_group_name
        self.region_name = region_name
        self.client = boto3.client('logs', region_name=region_name)
        self.log_stream_name = f"construction-app-{datetime.now().strftime('%Y-%m-%d')}"
        
    def ensure_log_group_exists(self) -> bool:
        """
        Ensure the log group exists, create if it doesn't
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.client.describe_log_groups(logGroupNamePrefix=self.log_group_name)
            return True
        except Exception:
            try:
                self.client.create_log_group(logGroupName=self.log_group_name)
                return True
            except Exception as e:
                print(f"Error creating log group: {e}")
                return False
    
    def ensure_log_stream_exists(self) -> bool:
        """
        Ensure the log stream exists, create if it doesn't
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.client.describe_log_streams(
                logGroupName=self.log_group_name,
                logStreamNamePrefix=self.log_stream_name
            )
            return True
        except Exception:
            try:
                self.client.create_log_stream(
                    logGroupName=self.log_group_name,
                    logStreamName=self.log_stream_name
                )
                return True
            except Exception as e:
                print(f"Error creating log stream: {e}")
                return False
    
    def log_project_activity(self, activity_type: str, project_name: str, 
                           user: str, details: Dict[str, Any]) -> bool:
        """
        Log construction project activity to CloudWatch
        
        Args:
            activity_type: Type of activity (CREATE, UPDATE, DELETE, VIEW)
            project_name: Name of the construction project
            user: Username performing the activity
            details: Additional details about the activity
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.ensure_log_group_exists() or not self.ensure_log_stream_exists():
            return False
        
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'activity_type': activity_type,
            'project_name': project_name,
            'user': user,
            'details': details
        }
        
        try:
            response = self.client.put_log_events(
                logGroupName=self.log_group_name,
                logStreamName=self.log_stream_name,
                logEvents=[
                    {
                        'timestamp': int(datetime.utcnow().timestamp() * 1000),
                        'message': json.dumps(log_entry)
                    }
                ]
            )
            return True
        except Exception as e:
            print(f"Error logging to CloudWatch: {e}")
            return False
    
    def log_user_login(self, username: str, ip_address: str = None) -> bool:
        """
        Log user login activity
        
        Args:
            username: Username of the logged in user
            ip_address: IP address of the user (optional)
            
        Returns:
            bool: True if successful, False otherwise
        """
        details = {'ip_address': ip_address} if ip_address else {}
        return self.log_project_activity('LOGIN', 'USER_AUTH', username, details)
    
    def log_file_upload(self, filename: str, user: str, project_name: str) -> bool:
        """
        Log file upload activity
        
        Args:
            filename: Name of the uploaded file
            user: Username who uploaded the file
            project_name: Name of the related project
            
        Returns:
            bool: True if successful, False otherwise
        """
        details = {'filename': filename, 'action': 'file_upload'}
        return self.log_project_activity('FILE_UPLOAD', project_name, user, details)


class S3FileManager:
    """
    Object-oriented S3 file management for construction documents
    """
    
    def __init__(self, bucket_name: str, region_name: str = 'eu-north-1'):
        """
        Initialize S3 File Manager
        
        Args:
            bucket_name: AWS S3 bucket name
            region_name: AWS region name
        """
        self.bucket_name = bucket_name
        self.region_name = region_name
        self.client = boto3.client('s3', region_name=region_name)
    
    def upload_file(self, file_obj, file_key: str) -> bool:
        """
        Upload file to S3 bucket
        
        Args:
            file_obj: File object to upload
            file_key: S3 key for the file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.client.upload_fileobj(file_obj, self.bucket_name, file_key)
            return True
        except Exception as e:
            print(f"Error uploading file to S3: {e}")
            return False
    
    def get_file_url(self, file_key: str, expiration: int = 3600) -> Optional[str]:
        """
        Generate presigned URL for file access
        
        Args:
            file_key: S3 key for the file
            expiration: URL expiration time in seconds
            
        Returns:
            str: Presigned URL or None if error
        """
        try:
            url = self.client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': file_key},
                ExpiresIn=expiration
            )
            return url
        except Exception as e:
            print(f"Error generating presigned URL: {e}")
            return None


class NotificationManager:
    """
    Object-oriented notification manager using AWS SES and SNS
    """
    
    def __init__(self, region_name: str = 'eu-north-1'):
        """
        Initialize Notification Manager
        
        Args:
            region_name: AWS region name
        """
        self.region_name = region_name
        self.ses_client = boto3.client('ses', region_name=region_name)
        self.sns_client = boto3.client('sns', region_name=region_name)
    
    def send_email(self, to_email: str, subject: str, body: str, 
                   sender_email: str) -> bool:
        """
        Send email using AWS SES
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            body: Email body
            sender_email: Verified sender email
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            response = self.ses_client.send_email(
                Source=sender_email,
                Destination={'ToAddresses': [to_email]},
                Message={
                    'Subject': {'Data': subject},
                    'Body': {'Text': {'Data': body}}
                }
            )
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    def send_sns_notification(self, topic_arn: str, message: str, 
                            subject: str = None) -> bool:
        """
        Send SNS notification
        
        Args:
            topic_arn: SNS topic ARN
            message: Notification message
            subject: Optional subject
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            params = {
                'TopicArn': topic_arn,
                'Message': message
            }
            if subject:
                params['Subject'] = subject
                
            response = self.sns_client.publish(**params)
            return True
        except Exception as e:
            print(f"Error sending SNS notification: {e}")
            return False
