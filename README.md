# Fundtik - Funding Management Platform

**Fundtik** is a Django-based funding management platform that helps users discover funding opportunities, create projects, and manage applications. The platform connects project creators with funding sources and facilitates the application process.

## 🚀 Quick Start

Get Fundtik running with sample data in under 2 minutes:

```bash
git clone https://github.com/code-wizard/fundtik.git && cd fundtik
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python setup_fundtik.py
python manage.py runserver
```

**🎯 Instant Demo Ready:** Complete with sample users, funding opportunities, projects, and applications!

## 🏗️ Architecture Overview

- **Backend Framework:** Django 5.2.5 with Django REST Framework
- **Database:** SQLite (development)
- **Authentication:** Django Allauth with JWT tokens and custom email/phone authentication
- **Real-time Features:** Django Channels for WebSocket support
- **API:** RESTful API with django-rest-auth

## 📁 Project Structure

The application follows Django's app-based architecture with the following core apps:

### Core Applications

#### 🔐 Accounts App (`/accounts/`)
- **Purpose:** User authentication and profile management
- **Key Model:** `FbUser` (Custom User model extending AbstractUser)
- **Features:**
  - Email and phone-based authentication
  - User profiles with avatars
  - Custom authentication backend supporting email or phone login
  - UUID-based primary keys for enhanced security

#### 💰 Fund App (`/fund/`)
- **Purpose:** Funding opportunity management
- **Key Model:** `FbFunding`
- **Features:**
  - Funding agencies and opportunities tracking
  - Opening/closing dates management
  - Amount and qualification details
  - File attachments for funding documentation
  - Category-based classification

#### 📋 Projects App (`/projects/`)
- **Purpose:** Project creation and management
- **Key Models:** `FbProjects`, `FbMileStones`
- **Features:**
  - Project lifecycle management (start/end dates)
  - Budget tracking
  - Category-based project classification
  - Many-to-many relationship with funding opportunities
  - Milestone tracking with assignees and due dates
  - File upload capabilities

#### 📝 Applications App (`/applications/`)
- **Purpose:** Funding application management
- **Key Model:** `FbApplication`
- **Features:**
  - Links projects to funding opportunities
  - Application status tracking
  - Request approval workflow
  - Comment system for application notes

#### ❓ Questions App (`/questions/`)
- **Purpose:** FAQ and knowledge base
- **Key Model:** `FbQuestions`
- **Features:**
  - Question and answer management
  - Tag-based categorization
  - Lifecycle management for content freshness

#### Supporting Apps
- **Staff App:** Administrative functionality
- **File Manager App:** File management system
- **Main App:** Landing pages and general content
- **Core App:** Custom fields, pagination, and storage backends

## ✨ Key Features

### 👥 User Management
- Custom user model with email/phone authentication
- Profile management with avatars
- Role-based access (staff/regular users)

### 🔍 Funding Discovery
- Comprehensive funding opportunity database
- Search and filtering capabilities
- Category-based organization

### 📊 Project Management
- Full project lifecycle tracking
- Milestone management with assignments
- Budget tracking and reporting
- File attachment support

### 🔄 Application Workflow
- Streamlined application process
- Status tracking and approval workflow
- Integration between projects and funding opportunities

### 📚 Knowledge Base
- FAQ system with tagging
- Content lifecycle management

### 🎯 Sample Data & Quick Setup
- One-click setup script with comprehensive sample data
- Realistic funding opportunities, projects, and user accounts
- Pre-configured relationships and workflows
- Instant development environment ready for testing

## 🛠️ Technical Specifications

### Dependencies
```
Django==5.2.5
djangorestframework==3.16.1
django-channels==4.3.1
django-allauth==65.11.0
django-rest-auth==0.9.5
django-cors-headers==4.7.0
djangorestframework-jwt==1.11.0
pillow==11.3.0
gunicorn==23.0.0
```

### Database Design
- Uses SQLite for development
- Custom file upload paths with timestamp-based naming
- Optimized for SQLite with comma-separated fields for arrays

### Authentication
- JWT token-based API authentication
- Custom backend supporting email OR phone login
- Django Allauth integration for comprehensive auth features

## 🚀 Getting Started

### Prerequisites
- Python 3.8+ (3.9 recommended)
- pip (Python package manager)
- Git

### Quick Setup (Recommended)

For a quick start with sample data:

```bash
# Clone and setup
git clone https://github.com/code-wizard/fundtik.git
cd fundtik

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# .venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt

# Run the setup script with sample data
python setup_fundtik.py

# Start the server
python manage.py runserver
```

**Default Credentials:**
- **Admin:** admin / admin123
- **Sample Users:** firstname.lastname[number]@example.com / password123
- **Staff Users:** staff0@fundtik.com / staff123

### Manual Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/code-wizard/fundtik.git
   cd fundtik
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On macOS/Linux
   # .venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   # Create .env file (optional)
   cp .env.example .env  # If example exists
   ```

5. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Main application: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

### 🎯 Setup Script Options

The `setup_fundtik.py` script supports several options:

```bash
# Basic setup with default sample data
python setup_fundtik.py

# Clear existing data and create fresh sample data
python setup_fundtik.py --clear

# Customize the amount of sample data
python setup_fundtik.py --users 20 --funding 25 --projects 30

# Clear and create custom sample data
python setup_fundtik.py --clear --users 15 --funding 20 --projects 25
```

**Sample Data Created:**
- **Users:** Regular users, staff members, and admin
- **Funding Opportunities:** Various agencies and grant types
- **Projects:** Different categories with realistic timelines
- **Milestones:** Project milestones with assignments
- **Applications:** Links between projects and funding
- **FAQ Questions:** Common platform questions and answers

### 🔧 Django Management Commands

You can also use Django management commands directly:

```bash
# Create sample data using Django command
python manage.py setup_sample_data --users 10 --funding 15 --projects 20

# Clear existing data
python manage.py setup_sample_data --clear
```

### 📊 Sample Data Details

The setup script creates comprehensive, realistic sample data to help you explore the platform:

#### 👥 **Users (Default: 10)**
- **Regular Users:** Realistic names and email addresses (e.g., john.smith1@example.com)
- **Staff Users:** Administrative access (staff0@fundtik.com, staff1@fundtik.com)
- **Admin User:** Full superuser access (admin@fundtik.com)
- **Password:** All sample users use `password123` (staff: `staff123`, admin: `admin123`)

#### 💰 **Funding Opportunities (Default: 15)**
- **Agencies:** NSF, NIH, NASA, DoE, Ford Foundation, Gates Foundation, etc.
- **Types:** Research grants, innovation funds, fellowships, startup grants
- **Amounts:** $10,000 - $1,000,000 with realistic distribution
- **Categories:** Technology, Healthcare, Environment, Education, Energy, AI/ML
- **Timelines:** Mix of open, closing soon, and future opportunities

#### 📋 **Projects (Default: 20)**
- **Categories:** AI/Healthcare, Sustainable Energy, Smart Cities, EdTech, etc.
- **Realistic Names:** "AI-Powered Healthcare Platform", "Climate Change Monitoring"
- **Budgets:** $50,000 - $2,000,000 range
- **Timelines:** 6 months to 2 years project duration
- **Funding Links:** Each project linked to 1-3 relevant funding opportunities

#### 🎯 **Milestones (3-8 per project)**
- **Phases:** Kickoff, Analysis, Design, Development, Testing, Documentation
- **Assignments:** Distributed among sample users
- **Timelines:** Evenly distributed across project duration
- **Reminders:** 1-14 days before due dates

#### 📝 **Applications (Varies)**
- **Smart Linking:** Projects automatically linked to relevant funding
- **Realistic Comments:** Professional application comments and justifications
- **Status Tracking:** All start as "not submitted" status
- **No Duplicates:** Each project-funding pair has only one application

#### ❓ **FAQ Questions (10)**
- **Common Topics:** Application process, document requirements, status tracking
- **Categories:** Tagged for easy searching (application, funding, milestones)
- **Realistic Content:** Practical questions users would actually ask

### 🧪 **Testing Your Setup**

After running the setup, verify everything works:

```bash
# Test the setup and view data summary
python test_setup.py

# Start the development server
python manage.py runserver

# Access the platform
open http://127.0.0.1:8000
```

**Quick Test Checklist:**
- ✅ Login with admin credentials (admin / admin123)
- ✅ Browse funding opportunities in the Fund section
- ✅ View sample projects and their milestones
- ✅ Check applications linking projects to funding
- ✅ Test user authentication with sample user credentials

## 📱 API Endpoints

The application provides RESTful API endpoints for:

- **Authentication:** `/accounts/`
- **Projects:** `/projects/`
- **Applications:** `/applications/`
- **Funding:** `/fund/`
- **Questions:** `/questions/`
- **Staff:** `/staff/`
- **File Management:** `/file-manager/`

## 🗂️ File Structure

```
fundtik/
├── accounts/           # User management
│   └── management/     # Django management commands
│       └── commands/   
│           └── setup_sample_data.py  # 📊 Sample data creation command
├── applications/       # Application workflows
├── core/              # Core utilities
├── filemanager/       # File management
├── fund/              # Funding opportunities
├── fundings/          # Project settings
├── main/              # Main app
├── projects/          # Project management
├── questions/         # FAQ system
├── staff/             # Staff functionality
├── static/            # Static files
├── templates/         # HTML templates
├── manage.py          # Django management
├── requirements.txt   # Dependencies
├── setup_fundtik.py   # 🚀 One-click setup script
├── test_setup.py      # 🧪 Setup verification script
└── db.sqlite3        # Database (development)
```

### 🔧 Setup & Testing Files

| File | Purpose | Usage |
|------|---------|-------|
| `setup_fundtik.py` | **Main Setup Script** | `python setup_fundtik.py` |
| `test_setup.py` | **Verify Setup** | `python test_setup.py` |
| `accounts/management/commands/setup_sample_data.py` | **Django Command** | `python manage.py setup_sample_data` |

## 🔧 Configuration

### Settings
Main configuration is in `fundings/settings.py`:
- Database configuration
- Installed apps
- Middleware setup
- Authentication backends

### URL Configuration
URL routing is defined in `fundings/urls.py` with app-specific URLs included from each app's `urls.py`.

## 📊 Database Models

### User Model (`FbUser`)
- Extended AbstractUser with UUID primary key
- Email and phone authentication
- Profile information with avatar support

### Core Models
- **FbFunding:** Funding opportunities
- **FbProjects:** Project information
- **FbMileStones:** Project milestones
- **FbApplication:** Funding applications
- **FbQuestions:** FAQ entries

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Code Wizard** - *Initial work* - [code-wizard](https://github.com/code-wizard)

## 🆘 Support

For support and questions:
- Create an issue in the GitHub repository
- Contact the development team

## 🔮 Future Enhancements

- [ ] Integration with external funding APIs
- [ ] Advanced search and filtering
- [ ] Email notifications for application status
- [ ] Dashboard analytics
- [ ] Mobile application support
- [ ] Multi-language support

---

*Last updated: August 25, 2025*
