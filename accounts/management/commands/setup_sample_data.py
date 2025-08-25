"""
Django management command to create sample data for Fundtik platform.
This command creates sample users, funding opportunities, projects, milestones, applications, and questions.
"""

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import date, timedelta
import random
from decimal import Decimal

from fund.models import FbFunding
from projects.models import FbProjects, FbMileStones
from applications.models import FbApplication
from questions.models import FbQuestions

FbUser = get_user_model()


class Command(BaseCommand):
    help = 'Create sample data for Fundtik platform including users, funding, projects, and applications'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before creating sample data',
        )
        parser.add_argument(
            '--users',
            type=int,
            default=10,
            help='Number of sample users to create (default: 10)',
        )
        parser.add_argument(
            '--funding',
            type=int,
            default=15,
            help='Number of sample funding opportunities to create (default: 15)',
        )
        parser.add_argument(
            '--projects',
            type=int,
            default=20,
            help='Number of sample projects to create (default: 20)',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting Fundtik sample data creation...'))
        
        if options['clear']:
            self.clear_data()
        
        # Create sample data
        users = self.create_users(options['users'])
        funding_opportunities = self.create_funding(options['funding'], users)
        projects = self.create_projects(options['projects'], users, funding_opportunities)
        self.create_milestones(projects, users)
        self.create_applications(projects, funding_opportunities, users)
        self.create_questions(users)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created sample data:\n'
                f'- {len(users)} users\n'
                f'- {len(funding_opportunities)} funding opportunities\n'
                f'- {len(projects)} projects\n'
                f'- Milestones, applications, and questions'
            )
        )

    def clear_data(self):
        """Clear existing data"""
        self.stdout.write('Clearing existing data...')
        FbApplication.objects.all().delete()
        FbMileStones.objects.all().delete()
        FbProjects.objects.all().delete()
        FbFunding.objects.all().delete()
        FbQuestions.objects.all().delete()
        # Don't delete superusers
        FbUser.objects.filter(is_superuser=False).delete()
        self.stdout.write(self.style.WARNING('Existing data cleared.'))

    def create_users(self, count):
        """Create sample users"""
        self.stdout.write(f'Creating {count} sample users...')
        users = []
        
        # Sample user data
        first_names = ['John', 'Jane', 'Michael', 'Sarah', 'David', 'Emily', 'Robert', 'Lisa', 'James', 'Maria']
        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez']
        
        for i in range(count):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            email = f'{first_name.lower()}.{last_name.lower()}{i}@example.com'
            phone = f'+1{random.randint(1000000000, 9999999999)}'
            username = f'{first_name.lower()}{last_name.lower()}{i}'
            
            user = FbUser.objects.create_user(
                username=username,
                email=email,
                phone=phone,
                first_name=first_name,
                last_name=last_name,
                password='password123'
            )
            users.append(user)
        
        # Create some staff users
        for i in range(2):
            staff_user = FbUser.objects.create_user(
                username=f'staff{i}',
                email=f'staff{i}@fundtik.com',
                phone=f'+1{random.randint(1000000000, 9999999999)}',
                first_name=f'Staff{i}',
                last_name='Member',
                password='staff123',
                is_staff=True
            )
            users.append(staff_user)
        
        return users

    def create_funding(self, count, users):
        """Create sample funding opportunities"""
        self.stdout.write(f'Creating {count} sample funding opportunities...')
        funding_opportunities = []
        
        # Sample funding data
        agencies = [
            'National Science Foundation',
            'Department of Energy',
            'National Institutes of Health',
            'NASA',
            'Department of Defense',
            'Environmental Protection Agency',
            'Ford Foundation',
            'Gates Foundation',
            'Rockefeller Foundation',
            'Carnegie Corporation'
        ]
        
        fund_types = [
            'Research Grant',
            'Innovation Fund',
            'Startup Grant',
            'Development Fund',
            'Fellowship Program',
            'Seed Funding',
            'Technology Grant',
            'Social Impact Fund',
            'Environmental Grant',
            'Education Fund'
        ]
        
        categories = [
            'Technology,Innovation,Research',
            'Healthcare,Medical,Biotech',
            'Environment,Sustainability,Climate',
            'Education,Social,Community',
            'Energy,Renewable,Clean Tech',
            'AI,Machine Learning,Data Science',
            'Agriculture,Food,Nutrition',
            'Transportation,Infrastructure,Urban',
            'Arts,Culture,Media',
            'Finance,Fintech,Blockchain'
        ]
        
        for i in range(count):
            opening_date = date.today() + timedelta(days=random.randint(-30, 30))
            closing_date = opening_date + timedelta(days=random.randint(30, 180))
            
            funding = FbFunding.objects.create(
                agency=random.choice(agencies),
                fund_name=f'{random.choice(fund_types)} {i+1}',
                web_link=f'https://funding-portal.com/opportunity/{i+1}',
                opening_date=opening_date,
                closing_date=closing_date,
                occurrence='Annual',
                occurrence_no=random.randint(1, 10),
                amount=random.randint(10000, 1000000),
                qualifiers='Graduate degree required, 3+ years experience',
                key_contacts='Program Officer: officer@agency.gov',
                requirements='Detailed project proposal, budget breakdown, team credentials',
                categories=random.choice(categories),
                created_by=random.choice(users)
            )
            funding_opportunities.append(funding)
        
        return funding_opportunities

    def create_projects(self, count, users, funding_opportunities):
        """Create sample projects"""
        self.stdout.write(f'Creating {count} sample projects...')
        projects = []
        
        # Sample project data
        project_names = [
            'AI-Powered Healthcare Platform',
            'Sustainable Energy Management System',
            'Smart City Infrastructure',
            'Educational Technology Platform',
            'Climate Change Monitoring',
            'Fintech Innovation Lab',
            'Agricultural IoT Solutions',
            'Mental Health App Development',
            'Blockchain Supply Chain',
            'Renewable Energy Research',
            'Social Impact Measurement Tool',
            'Environmental Data Analytics',
            'Digital Health Records',
            'Clean Water Technology',
            'Urban Mobility Solutions'
        ]
        
        categories = [
            'Technology',
            'Healthcare',
            'Environment',
            'Education',
            'Energy',
            'Finance',
            'Agriculture',
            'Social Impact',
            'Infrastructure',
            'Research'
        ]
        
        descriptions = [
            'Innovative project aimed at solving real-world problems through technology.',
            'Research-focused initiative to advance scientific understanding.',
            'Community-driven project to improve quality of life.',
            'Sustainable solution for environmental challenges.',
            'Educational platform to enhance learning outcomes.',
            'Healthcare technology to improve patient care.',
            'Financial innovation to increase accessibility.',
            'Agricultural technology to boost productivity.',
            'Infrastructure development for smart cities.',
            'Social initiative to address inequality.'
        ]
        
        for i in range(count):
            start_date = date.today() + timedelta(days=random.randint(-60, 60))
            end_date = start_date + timedelta(days=random.randint(180, 730))
            
            project = FbProjects.objects.create(
                name=f'{random.choice(project_names)} - Phase {i+1}',
                category=random.choice(categories),
                start_date=start_date,
                end_date=end_date,
                created_by=random.choice(users),
                description=random.choice(descriptions),
                budget=random.randint(50000, 2000000)
            )
            
            # Add random funding opportunities to projects
            funding_count = random.randint(1, 3)
            selected_funding = random.sample(funding_opportunities, min(funding_count, len(funding_opportunities)))
            project.funding.set(selected_funding)
            
            projects.append(project)
        
        return projects

    def create_milestones(self, projects, users):
        """Create sample milestones for projects"""
        self.stdout.write('Creating sample milestones...')
        
        milestone_names = [
            'Project Kickoff',
            'Requirements Analysis',
            'Design Phase Completion',
            'Development Sprint 1',
            'Prototype Testing',
            'User Feedback Collection',
            'Beta Release',
            'Final Testing',
            'Documentation',
            'Project Delivery'
        ]
        
        milestone_descriptions = [
            'Initial project setup and team coordination',
            'Comprehensive analysis of project requirements',
            'Complete design documentation and approval',
            'First development milestone achieved',
            'Working prototype ready for testing',
            'Collect and analyze user feedback',
            'Beta version released to stakeholders',
            'Comprehensive testing and bug fixes',
            'Complete project documentation',
            'Final project delivery and handover'
        ]
        
        for project in projects:
            milestone_count = random.randint(3, 8)
            project_duration = (project.end_date - project.start_date).days
            
            for i in range(milestone_count):
                days_offset = (project_duration // milestone_count) * (i + 1)
                due_date = project.start_date + timedelta(days=days_offset)
                
                FbMileStones.objects.create(
                    name=random.choice(milestone_names),
                    due_date=due_date,
                    project=project,
                    created_by=project.created_by,
                    assignee=random.choice(users),
                    description=random.choice(milestone_descriptions),
                    reminder=random.randint(1, 14)
                )

    def create_applications(self, projects, funding_opportunities, users):
        """Create sample applications"""
        self.stdout.write('Creating sample applications...')
        
        comments = [
            'This project aligns perfectly with our funding priorities.',
            'Innovative approach to solving complex challenges.',
            'Strong team with relevant experience and expertise.',
            'Comprehensive project plan with clear milestones.',
            'Potential for significant impact in the target domain.',
            'Well-structured budget and resource allocation.',
            'Addresses critical needs in the community.',
            'Leverages cutting-edge technology effectively.',
            'Strong partnership network and collaboration.',
            'Clear path to sustainability and scalability.'
        ]
        
        # Create applications linking projects to funding opportunities
        application_count = min(len(projects) * 2, len(funding_opportunities) * 3)
        
        for _ in range(application_count):
            project = random.choice(projects)
            funding = random.choice(funding_opportunities)
            
            # Avoid duplicate applications
            if not FbApplication.objects.filter(project=project, funding=funding).exists():
                FbApplication.objects.create(
                    project=project,
                    funding=funding,
                    comment=random.choice(comments),
                    created_by=project.created_by,
                    status='not submitted'
                )

    def create_questions(self, users):
        """Create sample FAQ questions"""
        self.stdout.write('Creating sample questions...')
        
        qa_data = [
            {
                'title': 'How do I submit a funding application?',
                'answer': 'To submit a funding application, navigate to the Projects section, select your project, and click on "Apply for Funding". Choose the relevant funding opportunity and complete the application form.',
                'tags': 'application,funding,submit'
            },
            {
                'title': 'What documents are required for project applications?',
                'answer': 'Required documents typically include project proposal, budget breakdown, team credentials, timeline, and any supporting research or references.',
                'tags': 'documents,requirements,application'
            },
            {
                'title': 'How can I track my application status?',
                'answer': 'You can track your application status in the Applications section of your dashboard. Status updates include submitted, under review, approved, or rejected.',
                'tags': 'status,tracking,application'
            },
            {
                'title': 'What types of funding are available?',
                'answer': 'Our platform features various funding types including research grants, innovation funds, startup grants, fellowships, and social impact funds from multiple agencies.',
                'tags': 'funding,types,grants'
            },
            {
                'title': 'How do I create and manage project milestones?',
                'answer': 'In your project dashboard, you can add milestones with due dates, assign team members, set reminders, and track progress throughout your project lifecycle.',
                'tags': 'milestones,project,management'
            },
            {
                'title': 'Can I collaborate with team members on projects?',
                'answer': 'Yes, you can invite team members to your projects, assign milestones, share documents, and collaborate in real-time through our platform.',
                'tags': 'collaboration,team,sharing'
            },
            {
                'title': 'What happens after my application is approved?',
                'answer': 'Once approved, you will receive notification and instructions for next steps, including funding disbursement process and reporting requirements.',
                'tags': 'approval,next steps,funding'
            },
            {
                'title': 'How do I update my profile information?',
                'answer': 'Go to your profile settings to update personal information, contact details, professional background, and profile picture.',
                'tags': 'profile,settings,update'
            },
            {
                'title': 'Are there deadlines for funding applications?',
                'answer': 'Yes, each funding opportunity has specific opening and closing dates. Make sure to check the deadline before starting your application.',
                'tags': 'deadlines,timing,application'
            },
            {
                'title': 'How can I search for relevant funding opportunities?',
                'answer': 'Use the search and filter features in the Funding section to find opportunities by category, amount, agency, or keywords relevant to your project.',
                'tags': 'search,funding,opportunities'
            }
        ]
        
        for qa in qa_data:
            FbQuestions.objects.create(
                title=qa['title'],
                answer=qa['answer'],
                created_by=random.choice(users),
                life_cycle=random.randint(30, 365),
                tag=qa['tags']
            )
