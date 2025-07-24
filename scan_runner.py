import os
import time

while True:
    print("Running VirusTotal check...")
    os.system("python manage.py check_virustotal_status")
    time.sleep(600)  # wait 10 minutes
