# import subprocess
# import os
# from django.core.management.base import BaseCommand

# def run_script(script_command):
#     try:
#         result = subprocess.run(script_command, shell=True, check=True, capture_output=True, text=True)
#         print(f"Output of {script_command}:\n{result.stdout}")
#     except subprocess.CalledProcessError as e:
#         print(f"Error running {script_command}:\n{e.stderr}")
#         raise

# def main():
#     # List of commands to run
#     base_dir = os.path.abspath(os.path.dirname(__file__))
#     scripts = [
#         # "node index.js", 
#         # "python maharastra_gemini.py", 
#         "python ../converted_combined.py",
#         # f"python {os.path.join(base_dir, '../../../../manage.py load_data')}"

#         # "node scraper2.js",
#         # "python3 load_to_db.py"
#     ]

#     for script in scripts:
#         run_script(script)

# if __name__ == "__main__":
#     main()


# myapp/management/commands/Scrapers/runAllScripts.py
import subprocess
import os
import sys
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Run all scraper scripts'

    def handle(self, *args, **kwargs):
        def run_script(script_command):
            try:
                result = subprocess.run(script_command, shell=True, check=True, capture_output=True, text=True)
                self.stdout.write(f"Output of {script_command}:\n{result.stdout}")
            except subprocess.CalledProcessError as e:
                self.stderr.write(f"Error running {script_command}:\n{e.stderr}")
                raise

        base_dir = os.path.abspath(os.path.dirname(__file__))
        scripts = [
            "node index.js",
            "python maharastra_gemini.py",

            
            f"python {os.path.join(base_dir, '../converted_combined.py')}",
            f"python {os.path.join(base_dir, '../../../../manage.py load_data')}"
            # Add other scripts as needed
        ]

        for script in scripts:
            self.stdout.write(f"Running script: {script}")
            run_script(script)

        self.stdout.write(self.style.SUCCESS('All scripts ran successfully.'))

if __name__ == "__main__":
    try:
        Command().handle()
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)
