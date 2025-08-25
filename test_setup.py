#!/usr/bin/env python3
"""
Test script to verify Fundtik setup and sample data

This script checks if the platform is properly set up with sample data.
"""

import os
import sys
import django
from pathlib import Path

# Setup Django
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fundings.settings')
django.setup()

from django.contrib.auth import get_user_model
from fund.models import FbFunding
from projects.models import FbProjects, FbMileStones
from applications.models import FbApplication
from questions.models import FbQuestions

def test_setup():
    """Test if the platform is properly set up"""
    print("🧪 Testing Fundtik Setup...")
    print("=" * 40)
    
    User = get_user_model()
    
    # Test database connection and models
    tests = [
        ("Users", User.objects.count()),
        ("Funding Opportunities", FbFunding.objects.count()),
        ("Projects", FbProjects.objects.count()),
        ("Milestones", FbMileStones.objects.count()),
        ("Applications", FbApplication.objects.count()),
        ("FAQ Questions", FbQuestions.objects.count()),
    ]
    
    print("📊 Data Summary:")
    total_records = 0
    for name, count in tests:
        print(f"   {name}: {count}")
        total_records += count
    
    print(f"\nTotal Records: {total_records}")
    
    # Test admin user
    admin_exists = User.objects.filter(is_superuser=True).exists()
    print(f"Admin User: {'✅ Exists' if admin_exists else '❌ Missing'}")
    
    # Test relationships
    projects_with_funding = FbProjects.objects.filter(funding__isnull=False).count()
    print(f"Projects with Funding: {projects_with_funding}")
    
    applications_count = FbApplication.objects.count()
    print(f"Applications Created: {applications_count}")
    
    if total_records > 0:
        print("\n✅ Setup appears successful!")
        print("\n🚀 Ready to start development:")
        print("   python manage.py runserver")
    else:
        print("\n❌ No sample data found!")
        print("   Run: python setup_fundtik.py")
    
    return total_records > 0

if __name__ == '__main__':
    test_setup()
