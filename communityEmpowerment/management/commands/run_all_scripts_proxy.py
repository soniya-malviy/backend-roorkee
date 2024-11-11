# communityEmpowerment/management/commands/run_all_scripts_proxy.py
import subprocess
import os
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Proxy command to run runAllScripts from Scrapers directory'

    def handle(self, *args, **kwargs):
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Scrapers/runAllScripts.py'))
        try:
            result = subprocess.run(['python', script_path], check=True, capture_output=True, text=True)
            self.stdout.write(f"Output of runAllScripts.py:\n{result.stdout}")
        except subprocess.CalledProcessError as e:
            self.stderr.write(f"Error running runAllScripts.py:\n{e.stderr}")
            raise
