from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from construction.models import Project
from datetime import date, timedelta


class Command(BaseCommand):
    help = 'Initialize the construction app with sample data'
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Initializing Construction Management App...'))
        
        # Create superuser if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@construction.com',
                password='admin'
            )
            self.stdout.write(self.style.SUCCESS('✅ Created superuser: admin/admin'))
        else:
            self.stdout.write(self.style.WARNING('⚠️ Superuser "admin" already exists'))
        
        # Create sample projects if none exist
        if not Project.objects.exists():
            admin_user = User.objects.get(username='admin')
            
            # Sample project 1
            Project.objects.create(
                name='Downtown Office Complex',
                description='A 25-story office building with modern amenities including underground parking, rooftop garden, and energy-efficient systems.',
                location='123 Main Street, New York, NY 10001',
                start_date=date.today(),
                end_date=date.today() + timedelta(days=365),
                budget=5000000.00,
                status='Planning',
                priority='High',
                manager=admin_user
            )
            
            # Sample project 2
            Project.objects.create(
                name='Residential Housing Development',
                description='A 50-unit residential complex with family-friendly amenities including playground, community center, and green spaces.',
                location='456 Oak Avenue, Brooklyn, NY 11201',
                start_date=date.today() + timedelta(days=30),
                end_date=date.today() + timedelta(days=545),
                budget=8500000.00,
                status='Planning',
                priority='Medium',
                manager=admin_user
            )
            
            # Sample project 3
            Project.objects.create(
                name='Highway Bridge Renovation',
                description='Complete renovation of a critical highway bridge including structural reinforcement and traffic safety improvements.',
                location='Route 95, Queens, NY 11368',
                start_date=date.today() + timedelta(days=60),
                end_date=date.today() + timedelta(days=240),
                budget=2750000.00,
                status='Planning',
                priority='Critical',
                manager=admin_user
            )
            
            self.stdout.write(self.style.SUCCESS('✅ Created 3 sample construction projects'))
        else:
            self.stdout.write(self.style.WARNING('⚠️ Projects already exist, skipping sample data creation'))
        
        self.stdout.write(
            self.style.SUCCESS(
                '\n🎉 Construction Management App initialized successfully!\n'
                '📝 Login with: admin/admin\n'
                '🌐 Access the app at: http://127.0.0.1:8000/construction/\n'
                '🔧 Admin panel at: http://127.0.0.1:8000/admin/\n'
            )
        )
