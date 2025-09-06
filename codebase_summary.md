# Codebase Summary

This is a Django-based funding management platform called **Fundtik**, designed to help users discover funding opportunities, create projects, and manage applications. It uses Django 5.2.5, Django REST Framework, and other libraries for authentication, real-time features, and API development. The project structure follows Django's app-based architecture, with a SQLite database for development.

Below is a summary of each top-level folder (ignoring generated folders like `__pycache__` and `migrations`, as well as files like `db.sqlite3`, `manage.py`, `requirements.txt`, `setup_fundtik.py`, `test`, and `test_setup.py`). Descriptions are based on the README, app configurations, and file contents, going down to at most 2 levels.

#### `accounts/`
- **Purpose**: Handles user authentication and profile management, including custom user models and backends.
- **Key Features**: Email/phone authentication, user profiles with avatars, UUID-based keys.
- **Files**:
  - `__init__.py`: Package initializer.
  - `adapter.py`: Custom adapter for Allauth, handles email confirmation and user setup.
  - `admin.py`: Registers the FbUser model with Django admin.
  - `api.py`: API view for resending activation emails.
  - `apps.py`: App configuration for the accounts app.
  - `backends.py`: Custom authentication backend allowing login by email or phone.
  - `forms.py`: Custom forms for login, signup, etc., extending Allauth forms.
  - `models.py`: Defines the FbUser model extending AbstractUser with phone, email, etc.
  - `serializers.py`: (Commented out) Serializers for user details, likely for API.
  - `signals.py`: (Commented out) Signal handlers for user signup.
  - `tests.py`: Empty test file.
  - `urls.py`: URL patterns for account views like signup, login, password reset.
  - `utils.py`: Utility functions for user filtering, name parsing, etc.
  - `views.py`: Views for signup, login, profile editing, etc., extending Allauth views.
- **Subfolders/Files (Level 1)**:
  - `management/commands/`: Contains custom Django management commands for account-related tasks.
  - `templates/accounts/`: HTML templates for account-related views (e.g., login, profile).

#### `applications/`
- **Purpose**: Manages funding applications, linking projects to funding opportunities.
- **Key Features**: Application status tracking, approval workflows, comment systems.
- **Files**:
  - `__init__.py`: Package initializer.
  - `admin.py`: Empty, no models registered.
  - `apps.py`: App configuration.
  - `forms.py`: ModelForm for FbApplication.
  - `models.py`: Defines FbApplication model linking projects and funding.
  - `tests.py`: Empty.
  - `urls.py`: URLs for listing and editing applications.
  - `views.py`: Views for listing and editing applications.
- **Subfolders/Files (Level 1)**:
  - `templates/applications/`: Templates for application-related pages.

#### `core/`
- **Purpose**: A utility package for shared components, not a full Django app.
- **Key Features**: Custom DRF fields, pagination classes, and storage backends.
- **Files**:
  - `__init__.py`: Package initializer.
  - `custom_fields.py`: Base64ImageField for DRF.
  - `pagination_class.py`: Custom pagination class.
  - `storage_backends.py`: Defines public and private media storage classes.
- **Subfolders/Files (Level 1)**: No subfolders.

#### `filemanager/`
- **Purpose**: Provides file management functionality for the platform.
- **Key Features**: Handles file uploads, storage, and organization.
- **Files**:
  - `__init__.py`: Package initializer.
  - `admin.py`: Empty.
  - `apps.py`: App configuration.
  - `models.py`: Empty.
  - `tests.py`: Empty.
  - `urls.py`: URL for files view.
  - `views.py`: View to render files page.
- **Subfolders/Files (Level 1)**:
  - `templates/filemanager/`: Templates for file management interfaces.

#### `fund/`
- **Purpose**: Manages funding opportunities and agencies.
- **Key Features**: Tracks funding details, categories, dates, amounts, and attachments.
- **Files**:
  - `__init__.py`: Package initializer.
  - `admin.py`: Empty.
  - `apps.py`: App configuration.
  - `forms.py`: ModelForm for FbFunding with custom save for PDF upload.
  - `models.py`: Defines FbFunding model for funding opportunities.
  - `tests.py`: Empty.
  - `urls.py`: URLs for listing, adding, viewing funds.
  - `views.py`: Views for listing, adding, viewing funding opportunities.
- **Subfolders/Files (Level 1)**:
  - `templates/fund/`: Templates for funding-related views.

#### `fundings/`
- **Purpose**: The main Django project configuration folder.
- **Key Features**: Contains project settings, URLs, routing, and WSGI/ASGI configurations.
- **Files**:
  - `__init__.py`: Package initializer.
  - `routing.py`: Channels routing for WebSockets (empty).
  - `settings.py`: Django project settings, including installed apps, database, etc.
  - `urls.py`: Main URL configuration including all app URLs.
  - `wsgi.py`: WSGI application entry point.
- **Subfolders/Files (Level 1)**: No subfolders.

#### `main/`
- **Purpose**: Handles landing pages and general content for the platform.
- **Key Features**: Static pages, home views, and non-app-specific functionality.
- **Files**:
  - `__init__.py`: Package initializer.
  - `admin.py`: Empty.
  - `apps.py`: App configuration.
  - `models.py`: Empty.
  - `tests.py`: Empty.
  - `urls.py`: URLs for home and dashboard.
  - `views.py`: Views for index (redirect to login) and dashboard.
- **Subfolders/Files (Level 1)**:
  - `static/`: Static assets like CSS, JS, and images.
  - `templates/main/`: Templates for main pages (e.g., homepage).

#### `projects/`
- **Purpose**: Manages project creation, lifecycle, and milestones.
- **Key Features**: Budget tracking, categories, milestones with assignees, file uploads.
- **Files**:
  - `__init__.py`: Package initializer.
  - `admin.py`: Empty.
  - `apps.py`: App configuration.
  - `forms.py`: ModelForms for FbProjects and FbMileStones.
  - `models.py`: Defines FbProjects and FbMileStones models.
  - `tests.py`: Empty.
  - `urls.py`: URLs for project CRUD, milestones, applications.
  - `views.py`: Views for listing, creating, editing projects, etc.
- **Subfolders/Files (Level 1)**:
  - `templates/projects/`: Templates for project-related views.

#### `questions/`
- **Purpose**: Manages FAQs and a knowledge base.
- **Key Features**: Question/answer system with tags and lifecycle management.
- **Files**:
  - `__init__.py`: Package initializer.
  - `admin.py`: Empty.
  - `apps.py`: App configuration.
  - `forms.py`: ModelForm for FbQuestions.
  - `models.py`: Defines FbQuestions model for FAQs.
  - `tests.py`: Empty.
  - `urls.py`: URL for listing questions.
  - `views.py`: View for listing and creating questions.
- **Subfolders/Files (Level 1)**:
  - `templates/questions/`: Templates for question-related pages.

#### `staff/`
- **Purpose**: Provides administrative functionality for staff users.
- **Key Features**: Admin interfaces, staff-specific views and management.
- **Files**:
  - `__init__.py`: Package initializer.
  - `admin.py`: Registers Staff model with admin, with list display, filters, etc.
  - `apps.py`: App configuration.
  - `models.py`: Defines Staff model for staff members.
  - `tests.py`: Empty.
  - `urls.py`: URLs for staff CRUD.
  - `views.py`: Views for listing, creating, editing, deleting staff.
- **Subfolders/Files (Level 1)**:
  - `templates/staff/`: Templates for staff-related pages.
