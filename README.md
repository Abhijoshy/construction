# 🏗️ Construction Management System

A Django-based construction project management application with AWS cloud services integration.

## 🌟 Features

### 📱 Application Pages (4 pages total)
1. **Login Page** - User authentication with CloudWatch logging
2. **Project List** - Overview of all construction projects
3. **Create Project** - Add new construction projects with file upload
4. **Project Details** - View, edit, and delete projects

### 🔐 Authentication
- Login/Logout functionality
- User session management
- Activity logging to CloudWatch

### ☁️ AWS Services Integration
- **Amazon S3** - Document storage and file management
- **Amazon SES** - Email notifications for project updates
- **Amazon SNS** - Push notifications for critical events
- **Amazon CloudWatch** - Activity logging and monitoring
- **Amazon RDS** - MySQL database for production (currently using SQLite3)

### 📚 Custom Library
- **AWS CloudWatch Logger** - Object-oriented logging library
- **S3 File Manager** - Secure file upload and management
- **Notification Manager** - Email and SNS notification handling

## 🚀 Quick Start

### Prerequisites
- Python virtual environment (`venv`) already created
- Required packages already installed
- AWS services configured with provided credentials

### Setup and Run

1. **Run the setup script:**
   ```bash
   setup_construction_app.bat
   ```

2. **Start the development server:**
   ```bash
   cd myproject
   ..\venv\Scripts\activate
   python manage.py runserver
   ```

3. **Access the application:**
   - Main app: http://127.0.0.1:8000/construction/
   - Admin panel: http://127.0.0.1:8000/admin/
   - Login credentials: `admin` / `admin`

## 📁 Project Structure

```
myproject/
├── construction/                 # Main app directory
│   ├── models.py                # Project model definition
│   ├── views.py                 # Application views (4 pages)
│   ├── urls.py                  # URL routing
│   ├── admin.py                 # Admin interface
│   ├── aws_utils.py             # Custom AWS integration library
│   ├── templates/construction/   # HTML templates
│   │   ├── base.html           # Base template
│   │   ├── login.html          # Page 1: Login
│   │   ├── project_list.html   # Page 2: Project list
│   │   ├── project_create.html # Page 3: Create project
│   │   └── project_detail.html # Page 4: Project details
│   └── management/commands/
│       └── init_construction.py # Setup command
├── myproject/                   # Django project settings
│   ├── settings.py             # Configuration with AWS settings
│   └── urls.py                 # Main URL configuration
└── requirements.txt            # Package dependencies
```

## 🗄️ Database Schema

### Project Model
- **name** - Project name
- **description** - Detailed description
- **location** - Project location
- **start_date** - Project start date
- **end_date** - Project end date
- **budget** - Project budget (decimal)
- **status** - Planning/In Progress/Completed/On Hold
- **priority** - Low/Medium/High/Critical
- **manager** - Foreign key to User model
- **document** - File upload field (stored in S3)
- **created_at** - Auto timestamp
- **updated_at** - Auto timestamp

## ☁️ AWS Configuration

The app uses the following AWS services configured in your environment:

```
S3_BUCKET_NAME=django-crud-files-18175-2025
AWS_REGION=eu-north-1
SNS_TOPIC_ARN=arn:aws:sns:eu-north-1:623849686048:django-crud-notifications
SES_SENDER_EMAIL=joshyabi82@gmail.com
CLOUDWATCH_LOG_GROUP=/aws/django-crud-app
```

## 🔧 Custom AWS Library Features

### CloudWatchLogger Class
- Project activity logging
- User authentication tracking
- File upload monitoring
- Error handling and retry logic

### S3FileManager Class
- Secure file uploads
- Presigned URL generation
- Document management

### NotificationManager Class
- SES email notifications
- SNS push notifications
- Event-driven messaging

## 📊 Activity Logging

All user activities are logged to AWS CloudWatch:
- User login/logout
- Project creation/updates/deletion
- File uploads
- Page views
- Error tracking

## 📧 Notifications

### Email Notifications (SES)
- Project creation confirmations
- Project update notifications
- Status change alerts

### Push Notifications (SNS)
- High/Critical priority project alerts
- System-wide notifications
- Real-time updates

## 🔄 CRUD Operations

### Create
- Add new construction projects
- Upload project documents to S3
- Send email notifications
- Log activities to CloudWatch

### Read
- List all projects with filtering
- View detailed project information
- Display document links from S3

### Update
- Edit project details
- Update project status/priority
- Replace documents in S3
- Track changes in CloudWatch

### Delete
- Remove projects with confirmation
- Clean up S3 documents
- Log deletion activities

## 🛡️ Security Features

- User authentication required
- CSRF protection
- File upload validation
- AWS IAM role-based access
- Secure S3 presigned URLs

## 🚀 Production Deployment

For production deployment with AWS RDS:

1. Update `settings.py` database configuration
2. Install MySQL client: `pip install mysqlclient`
3. Configure RDS connection settings
4. Run migrations: `python manage.py migrate`
5. Deploy with Gunicorn: `pip install gunicorn`

## 🎯 Usage Examples

### Creating a Project
1. Login with admin/admin
2. Click "New Project"
3. Fill in project details
4. Upload documents (optional)
5. Submit - triggers AWS notifications

### Managing Projects
1. View projects on main dashboard
2. Click project name for details
3. Edit information in-place
4. Monitor status changes
5. Delete when completed

## 📈 Monitoring and Logs

### CloudWatch Logs
- Access logs in AWS Console
- Filter by activity type
- Monitor user behavior
- Track system performance

### Application Metrics
- Project creation rates
- User activity patterns
- File upload statistics
- Error tracking

## 🆘 Troubleshooting

### Common Issues
1. **AWS Credentials** - Ensure IAM role has proper permissions
2. **S3 Uploads** - Check bucket permissions and CORS settings
3. **Email Delivery** - Verify SES sender verification
4. **Notifications** - Confirm SNS topic subscriptions

### Debug Mode
Set `DEBUG = True` in settings.py for detailed error messages.

## 📞 Support

This application demonstrates integration of Django with 5 AWS services in a construction management context, featuring a custom object-oriented AWS library for meaningful functionality.
