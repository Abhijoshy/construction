"""
Test script to verify the Construction Management App functionality
"""

import os
import sys
import django

# Add the project directory to Python path
project_dir = r'e:\abhishek_cpp\myproject'
sys.path.append(project_dir)

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

def test_app():
    print("🧪 Testing Construction Management App...")
    print("=" * 50)
    
    try:
        # Test 1: Import models
        from construction.models import Project
        from django.contrib.auth.models import User
        print("✅ Models imported successfully")
        
        # Test 2: Check database connection
        user_count = User.objects.count()
        project_count = Project.objects.count()
        print(f"✅ Database connection: {user_count} users, {project_count} projects")
        
        # Test 3: Test AWS utilities import
        from construction.aws_utils import CloudWatchLogger, S3FileManager, NotificationManager
        print("✅ AWS utilities imported successfully")
        
        # Test 4: Check views import
        from construction import views
        print("✅ Views imported successfully")
        
        # Test 5: Check URL configuration
        from construction.urls import urlpatterns
        print(f"✅ URL patterns loaded: {len(urlpatterns)} routes")
        
        # Test 6: Check templates exist
        import os
        template_dir = os.path.join(project_dir, 'construction', 'templates', 'construction')
        templates = os.listdir(template_dir)
        print(f"✅ Templates found: {', '.join(templates)}")
        
        # Test 7: Sample project data
        if project_count > 0:
            sample_project = Project.objects.first()
            print(f"✅ Sample project: '{sample_project.name}' by {sample_project.manager.username}")
        
        print("\n🎉 All tests passed! The app is ready to use.")
        print("🌐 Run 'python manage.py runserver' to start the development server")
        print("📱 Then visit: http://127.0.0.1:8000/construction/")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_app()
