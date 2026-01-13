"""
Django management command to set up demo data and train the model
"""
from django.core.management.base import BaseCommand
from core.utils.sample_data import create_sample_data, clear_all_data
from core.utils.banking_products_data import create_banking_products, create_sample_leads_and_sales
from core.ai.trainer import AITrainer
from core.database import db


class Command(BaseCommand):
    help = 'Set up complete demo data including products, leads, and train the AI model'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before creating new data',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('Setting up Sales AI Demo System'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        
        # Clear existing data if requested
        if options['clear']:
            self.stdout.write('\n🗑️  Clearing existing data...')
            clear_all_data()
            db.products.delete_many({})
            db.leads.delete_many({})
            self.stdout.write(self.style.SUCCESS('   ✅ Data cleared!'))
        
        # Step 1: Create organizational hierarchy and agents
        self.stdout.write('\n📊 Step 1: Creating organizational hierarchy and agents...')
        try:
            create_sample_data()
            self.stdout.write(self.style.SUCCESS('   ✅ Hierarchy and agents created!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ❌ Error: {e}'))
            if 'duplicate key error' in str(e).lower():
                self.stdout.write(self.style.WARNING('   ⚠️  Data already exists. Use --clear to reset.'))
        
        # Step 2: Create banking products
        self.stdout.write('\n🏦 Step 2: Creating banking products...')
        try:
            create_banking_products()
            products_count = db.products.count_documents({})
            self.stdout.write(self.style.SUCCESS(f'   ✅ {products_count} products created!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ❌ Error: {e}'))
            if 'duplicate key error' in str(e).lower():
                self.stdout.write(self.style.WARNING('   ⚠️  Products already exist. Use --clear to reset.'))
        
        # Step 3: Create leads and sales
        self.stdout.write('\n📈 Step 3: Creating leads and sales data...')
        try:
            create_sample_leads_and_sales()
            leads_count = db.leads.count_documents({})
            sales_count = db.sales.count_documents({})
            self.stdout.write(self.style.SUCCESS(f'   ✅ {leads_count} leads and {sales_count} sales created!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ❌ Error: {e}'))
        
        # Step 4: Display summary
        self.stdout.write('\n📊 Data Summary:')
        division_heads_count = db.division_heads.count_documents({})
        area_managers_count = db.area_managers.count_documents({})
        agents_count = db.agents.count_documents({})
        activities_count = db.activities.count_documents({})
        sales_count = db.sales.count_documents({})
        products_count = db.products.count_documents({})
        leads_count = db.leads.count_documents({})
        
        self.stdout.write(f'   Division Heads: {division_heads_count}')
        self.stdout.write(f'   Area Managers: {area_managers_count}')
        self.stdout.write(f'   Agents: {agents_count}')
        self.stdout.write(f'   Activities: {activities_count}')
        self.stdout.write(f'   Sales: {sales_count}')
        self.stdout.write(f'   Products: {products_count}')
        self.stdout.write(f'   Leads: {leads_count}')
        
        # Step 5: Train model
        self.stdout.write('\n🤖 Step 4: Training AI model...')
        try:
            model, accuracy = AITrainer.train_model()
            self.stdout.write(self.style.SUCCESS(f'   ✅ Model trained successfully!'))
            self.stdout.write(self.style.SUCCESS(f'   Accuracy: {accuracy * 100:.2f}%'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ❌ Error training model: {e}'))
            self.stdout.write(self.style.WARNING('   ⚠️  You can train the model later at /train/'))
        
        self.stdout.write(self.style.SUCCESS('\n' + '=' * 60))
        self.stdout.write(self.style.SUCCESS('✅ Setup complete!'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write('\n💡 Usage:')
        self.stdout.write('   • View dashboard: http://your-domain.com/')
        self.stdout.write('   • Train AI model: http://your-domain.com/train/')
        self.stdout.write('   • To reset data: python manage.py setup_demo --clear\n')
