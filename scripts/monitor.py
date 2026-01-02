import os
import psutil
from datetime import datetime
from supabase import create_client, Client

# Configuration
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_SERVICE_ROLE_KEY')

# Initialize Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def check_system_health():
    disk = psutil.disk_usage('/')
    ram = psutil.virtual_memory()
    
    status = "Healthy"
    if disk.percent > 90 or ram.percent > 95:
        status = "Warning"
    
    return status, disk.percent, ram.percent

def update_health_logs(status, disk, ram):
    data = {
        "timestamp": datetime.now().isoformat(),
        "status": status,
        "disk_usage": disk,
        "ram_usage": ram
    }
    supabase.table('health_logs').insert(data).execute()

def main():
    status, disk, ram = check_system_health()
    update_health_logs(status, disk, ram)
    print(f"Health check complete: {status} (D:{disk}%, R:{ram}%)")

if __name__ == "__main__":
    main()
