#!/usr/bin/env python3
"""
Fundtik Initial Setup Script

This script sets up the Fundtik platform with sample data for development and testing.
It creates sample users, funding opportunities, projects, milestones, applications, and FAQ questions.

Usage:
    python setup_fundtik.py [--clear] [--users N] [--funding N] [--projects N]

Options:
    --clear       Clear existing data before creating sample data
    --users N     Number of sample users to create (default: 10)
    --funding N   Number of funding opportunities to create (default: 15)
    --projects N  Number of projects to create (default: 20)
"""

import os
import sys
import django
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fundings.settings')
django.setup()

import argparse
from django.core.management import execute_from_command_line
from django.core.management.base import CommandError


def run_setup():
    """Main setup function"""
    parser = argparse.ArgumentParser(description='Setup Fundtik platform with sample data')
    parser.add_argument('--clear', action='store_true', help='Clear existing data')
    parser.add_argument('--users', type=int, default=10, help='Number of users to create')
    parser.add_argument('--funding', type=int, default=15, help='Number of funding opportunities')
    parser.add_argument('--projects', type=int, default=20, help='Number of projects')
    
    args = parser.parse_args()
    
    print("🚀 Starting Fundtik Setup...")
    print("=" * 50)
    
    # Step 1: Run migrations
    print("📦 Running database migrations...")
    try:
        execute_from_command_line(['manage.py', 'migrate', '--noinput'])
        print("✅ Migrations completed successfully")
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False
    
    # Step 2: Create sample data
    print("\n📊 Creating sample data...")
    try:
        cmd_args = ['manage.py', 'setup_sample_data']
        
        if args.clear:
            cmd_args.append('--clear')
        
        cmd_args.extend([
            '--users', str(args.users),
            '--funding', str(args.funding),
            '--projects', str(args.projects)
        ])
        
        execute_from_command_line(cmd_args)
        print("✅ Sample data created successfully")
    except Exception as e:
        print(f"❌ Sample data creation failed: {e}")
        return False
    
    # Step 3: Create superuser (optional)
    print("\n👤 Creating superuser...")
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@fundtik.com',
                phone='+1234567890',
                first_name='Admin',
                last_name='User',
                password='admin123'
            )
            print("✅ Superuser created (username: admin, password: admin123)")
        else:
            print("ℹ️  Superuser already exists")
    except Exception as e:
        print(f"⚠️  Superuser creation failed: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Fundtik setup completed successfully!")
    print("\n📋 Setup Summary:")
    print(f"   • {args.users} sample users created")
    print(f"   • {args.funding} funding opportunities created")
    print(f"   • {args.projects} projects created")
    print("   • Milestones, applications, and FAQ questions added")
    print("   • Admin user: admin / admin123")
    
    print("\n🚀 Next Steps:")
    print("1. Start the development server:")
    print("   python manage.py runserver")
    print("\n2. Access the platform:")
    print("   • Main site: http://127.0.0.1:8000/")
    print("   • Admin panel: http://127.0.0.1:8000/admin/")
    print("\n3. Sample user credentials:")
    print("   • Users: [firstname].[lastname][number]@example.com")
    print("   • Password: password123")
    print("   • Staff users: staff0@fundtik.com / staff123")
    
    return True


if __name__ == '__main__':
    try:
        success = run_setup()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n❌ Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        sys.exit(1)
