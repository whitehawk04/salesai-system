"""
Django management command to set up demo data and train the model
"""
from django.core.management.base import BaseCommand
from core.utils.sample_data import create_sample_data
from core.ai.trainer import AITrainer


class Command(BaseCommand):
    help = 'Set up demo data and train the AI model'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('Setting up Sales AI Demo System'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        
        # Create sample data
        self.stdout.write('\n📊 Step 1: Creating sample data...')
        create_sample_data()
        
        # Train model
        self.stdout.write('\n🤖 Step 2: Training AI model...')
        try:
            model, accuracy = AITrainer.train_model()
            self.stdout.write(self.style.SUCCESS(f'\n✅ Model trained successfully!'))
            self.stdout.write(self.style.SUCCESS(f'   Accuracy: {accuracy * 100:.2f}%'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error training model: {e}'))
        
        self.stdout.write(self.style.SUCCESS('\n' + '=' * 60))
        self.stdout.write(self.style.SUCCESS('✅ Setup complete!'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write('\n🚀 Run the server: python manage.py runserver')
        self.stdout.write('📊 View dashboard: http://localhost:8000\n')
