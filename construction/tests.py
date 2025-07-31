from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Project
from datetime import date, timedelta

class ConstructionAppTests(TestCase):
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        
    def test_login_page_loads(self):
        """Test that login page loads correctly"""
        response = self.client.get(reverse('user_login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Login to Construction Management')
        
    def test_user_can_login(self):
        """Test user authentication"""
        response = self.client.post(reverse('user_login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after login
        
    def test_project_creation(self):
        """Test project model creation"""
        project = Project.objects.create(
            name='Test Project',
            description='Test Description',
            location='Test Location',
            start_date=date.today(),
            end_date=date.today() + timedelta(days=365),
            budget=100000.00,
            status='Planning',
            priority='Medium',
            manager=self.user
        )
        self.assertEqual(project.name, 'Test Project')
        self.assertEqual(str(project), 'Test Project')
        self.assertEqual(project.manager, self.user)
        
    def test_project_list_requires_login(self):
        """Test that project list requires authentication"""
        response = self.client.get(reverse('project_list'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        
    def test_authenticated_user_can_view_projects(self):
        """Test authenticated user can view project list"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('project_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Construction Projects')
        
    def test_project_create_requires_login(self):
        """Test that project creation requires authentication"""
        response = self.client.get(reverse('project_create'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        
    def test_authenticated_user_can_create_project(self):
        """Test authenticated user can access project creation page"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('project_create'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create New Construction Project')
        
    def test_project_detail_view(self):
        """Test project detail view"""
        # Create a test project
        project = Project.objects.create(
            name='Detail Test Project',
            description='Test Description for Detail View',
            location='Test Location',
            start_date=date.today(),
            end_date=date.today() + timedelta(days=180),
            budget=250000.00,
            status='In Progress',
            priority='High',
            manager=self.user
        )
        
        # Login and access project detail
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('project_detail', args=[project.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Detail Test Project')
        self.assertContains(response, 'Test Description for Detail View')
        
    def test_project_model_str_method(self):
        """Test project model string representation"""
        project = Project(name='String Test Project')
        self.assertEqual(str(project), 'String Test Project')
        
    def test_project_model_ordering(self):
        """Test project model ordering"""
        # Create two projects
        project1 = Project.objects.create(
            name='First Project',
            description='First Description',
            location='Location 1',
            start_date=date.today(),
            end_date=date.today() + timedelta(days=100),
            budget=50000.00,
            status='Planning',
            priority='Low',
            manager=self.user
        )
        
        project2 = Project.objects.create(
            name='Second Project',
            description='Second Description',
            location='Location 2',
            start_date=date.today(),
            end_date=date.today() + timedelta(days=200),
            budget=75000.00,
            status='In Progress',
            priority='Medium',
            manager=self.user
        )
        
        # Check ordering (should be by -created_at, so latest first)
        projects = Project.objects.all()
        self.assertEqual(projects.first(), project2)  # Latest created should be first
        
    def test_aws_utils_import(self):
        """Test that AWS utilities can be imported"""
        try:
            from .aws_utils import CloudWatchLogger, S3FileManager, NotificationManager
            self.assertTrue(True)  # If import succeeds, test passes
        except ImportError:
            self.fail("AWS utilities import failed")
            
    def test_logout_functionality(self):
        """Test user logout"""
        # Login first
        self.client.login(username='testuser', password='testpass123')
        
        # Then logout
        response = self.client.get(reverse('user_logout'))
        self.assertEqual(response.status_code, 302)  # Redirect after logout
