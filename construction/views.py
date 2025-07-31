from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.files.storage import default_storage
from django.http import JsonResponse
from .models import Project
from .aws_utils import CloudWatchLogger, S3FileManager, NotificationManager
import os


# Initialize AWS utilities
cloudwatch_logger = CloudWatchLogger(settings.AWS_CLOUDWATCH_LOG_GROUP, settings.AWS_REGION)
s3_manager = S3FileManager(settings.AWS_S3_BUCKET_NAME, settings.AWS_REGION)
notification_manager = NotificationManager(settings.AWS_REGION)


def user_login(request):
    """Login page - Page 1"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Log login activity to CloudWatch
            ip_address = request.META.get('REMOTE_ADDR', '')
            cloudwatch_logger.log_user_login(username, ip_address)
            
            messages.success(request, 'Login successful!')
            return redirect('project_list')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'construction/login.html')


def user_logout(request):
    """Logout functionality"""
    username = request.user.username if request.user.is_authenticated else 'Anonymous'
    logout(request)
    
    # Log logout activity
    cloudwatch_logger.log_project_activity('LOGOUT', 'USER_AUTH', username, {})
    
    messages.success(request, 'You have been logged out successfully.')
    return redirect('user_login')


@login_required
def project_list(request):
    """Project list page - Page 2"""
    projects = Project.objects.all()
    
    # Log view activity
    cloudwatch_logger.log_project_activity(
        'VIEW', 'PROJECT_LIST', request.user.username, 
        {'total_projects': projects.count()}
    )
    
    return render(request, 'construction/project_list.html', {'projects': projects})


@login_required
def project_create(request):
    """Create project page - Page 3"""
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        description = request.POST.get('description')
        location = request.POST.get('location')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        budget = request.POST.get('budget')
        status = request.POST.get('status')
        priority = request.POST.get('priority')
        document = request.FILES.get('document')
        
        # Create project
        project = Project.objects.create(
            name=name,
            description=description,
            location=location,
            start_date=start_date,
            end_date=end_date,
            budget=budget,
            status=status,
            priority=priority,
            manager=request.user
        )
        
        # Handle file upload to S3
        if document:
            file_key = f"project_documents/{project.id}_{document.name}"
            if s3_manager.upload_file(document, file_key):
                project.document = file_key
                project.save()
                
                # Log file upload
                cloudwatch_logger.log_file_upload(document.name, request.user.username, name)
        
        # Log project creation
        cloudwatch_logger.log_project_activity(
            'CREATE', name, request.user.username,
            {'budget': str(budget), 'status': status, 'priority': priority}
        )
        
        # Send email notification using SES
        notification_manager.send_email(
            to_email=request.user.email or settings.AWS_SES_SENDER_EMAIL,
            subject=f'New Construction Project Created: {name}',
            body=f'A new construction project "{name}" has been created with budget ${budget}.',
            sender_email=settings.AWS_SES_SENDER_EMAIL
        )
        
        # Send SNS notification for high priority projects
        if priority in ['High', 'Critical']:
            notification_manager.send_sns_notification(
                topic_arn=settings.AWS_SNS_TOPIC_ARN,
                message=f'High priority construction project created: {name} (Priority: {priority})',
                subject='High Priority Project Alert'
            )
        
        messages.success(request, f'Project "{name}" created successfully!')
        return redirect('project_list')
    
    return render(request, 'construction/project_create.html')


@login_required
def project_detail(request, project_id):
    """Project detail and edit page - Page 4"""
    project = get_object_or_404(Project, id=project_id)
    
    if request.method == 'POST':
        # Handle project update
        action = request.POST.get('action')
        
        if action == 'update':
            # Update project fields
            project.name = request.POST.get('name')
            project.description = request.POST.get('description')
            project.location = request.POST.get('location')
            project.start_date = request.POST.get('start_date')
            project.end_date = request.POST.get('end_date')
            project.budget = request.POST.get('budget')
            project.status = request.POST.get('status')
            project.priority = request.POST.get('priority')
            
            # Handle new document upload
            document = request.FILES.get('document')
            if document:
                file_key = f"project_documents/{project.id}_{document.name}"
                if s3_manager.upload_file(document, file_key):
                    project.document = file_key
                    cloudwatch_logger.log_file_upload(document.name, request.user.username, project.name)
            
            project.save()
            
            # Log project update
            cloudwatch_logger.log_project_activity(
                'UPDATE', project.name, request.user.username,
                {'budget': str(project.budget), 'status': project.status}
            )
            
            messages.success(request, f'Project "{project.name}" updated successfully!')
            
        elif action == 'delete':
            project_name = project.name
            project.delete()
            
            # Log project deletion
            cloudwatch_logger.log_project_activity(
                'DELETE', project_name, request.user.username, {}
            )
            
            messages.success(request, f'Project "{project_name}" deleted successfully!')
            return redirect('project_list')
    
    # Log project detail view
    cloudwatch_logger.log_project_activity(
        'VIEW', project.name, request.user.username,
        {'project_id': project.id, 'status': project.status}
    )
    
    # Get S3 document URL if exists
    document_url = None
    if project.document:
        document_url = s3_manager.get_file_url(project.document)
    
    context = {
        'project': project,
        'document_url': document_url
    }
    
    return render(request, 'construction/project_detail.html', context)
