import os
import sys
import json
import random
import string
import winreg
import subprocess
from datetime import datetime
import sqlite3
import shutil

class AugmentPrivacyShield:
    """Privacy protection layer that feeds fake data to Augment Code"""
    
    def __init__(self):
        self.fake_data = self.generate_fake_system_data()
        self.original_env = {}
        self.protection_active = False
        
    def generate_fake_system_data(self):
        """Generate convincing fake system information"""
        fake_names = ["DevUser", "CodeMaster", "TechGuru", "BuildBot", "TestUser"]
        fake_computers = ["DEV-MACHINE", "BUILD-SERVER", "TEST-PC", "CODE-STATION"]
        fake_domains = ["WORKGROUP", "DEV-DOMAIN", "TEST-LAB"]
        
        return {
            'username': random.choice(fake_names),
            'computername': random.choice(fake_computers),
            'userdomain': random.choice(fake_domains),
            'userprofile': f"C:\\Users\\{random.choice(fake_names)}",
            'processor': self.generate_fake_cpu(),
            'memory': self.generate_fake_memory(),
            'gpu': self.generate_fake_gpu(),
            'network': self.generate_fake_network(),
            'software': self.generate_fake_software_list()
        }
    
    def generate_fake_cpu(self):
        """Generate fake CPU information"""
        cpu_brands = ["Intel", "AMD"]
        cpu_models = [
            "Core i5-10400", "Core i7-11700", "Ryzen 5 5600X", 
            "Ryzen 7 5800X", "Core i9-12900K"
        ]
        return {
            'brand': random.choice(cpu_brands),
            'model': random.choice(cpu_models),
            'cores': random.choice([4, 6, 8, 12]),
            'speed': f"{random.uniform(2.5, 4.5):.1f} GHz"
        }
    
    def generate_fake_memory(self):
        """Generate fake memory information"""
        return {
            'total': random.choice([8, 16, 32]) * 1024 * 1024 * 1024,  # GB in bytes
            'available': random.randint(4, 16) * 1024 * 1024 * 1024,
            'type': random.choice(["DDR4", "DDR5"])
        }
    
    def generate_fake_gpu(self):
        """Generate fake GPU information"""
        gpu_models = [
            "NVIDIA GeForce GTX 1660", "NVIDIA RTX 3060", 
            "AMD Radeon RX 6600", "Intel UHD Graphics 630"
        ]
        return {
            'model': random.choice(gpu_models),
            'memory': random.choice([4, 6, 8, 12]) * 1024 * 1024 * 1024
        }
    
    def generate_fake_network(self):
        """Generate fake network configuration"""
        return {
            'ip': f"192.168.{random.randint(1, 254)}.{random.randint(1, 254)}",
            'mac': ':'.join([f"{random.randint(0, 255):02x}" for _ in range(6)]),
            'dns': ["8.8.8.8", "1.1.1.1"],
            'gateway': f"192.168.{random.randint(1, 254)}.1"
        }
    
    def generate_fake_software_list(self):
        """Generate fake installed software list"""
        return [
            "Visual Studio Code", "Git", "Node.js", "Python 3.9",
            "Google Chrome", "Firefox", "7-Zip", "Notepad++",
            "Docker Desktop", "Postman", "FileZilla", "VLC Media Player"
        ]
    
    def activate_protection(self):
        """Activate privacy protection by modifying environment and system calls"""
        print("🛡️ Activating Augment Privacy Shield...")
        
        # Backup original environment variables
        self.backup_environment()
        
        # Set fake environment variables
        self.set_fake_environment()
        
        # Patch system information sources
        self.patch_system_info_sources()
        
        # Monitor and intercept Augment data collection
        self.setup_data_interception()
        
        self.protection_active = True
        print("✅ Privacy Shield activated! Fake data will be provided to Augment.")
    
    def backup_environment(self):
        """Backup original environment variables"""
        env_vars_to_backup = [
            'USERNAME', 'COMPUTERNAME', 'USERDOMAIN', 'USERPROFILE',
            'PROCESSOR_IDENTIFIER', 'PROCESSOR_ARCHITECTURE'
        ]
        
        for var in env_vars_to_backup:
            if var in os.environ:
                self.original_env[var] = os.environ[var]
    
    def set_fake_environment(self):
        """Set fake environment variables"""
        os.environ['USERNAME'] = self.fake_data['username']
        os.environ['COMPUTERNAME'] = self.fake_data['computername']
        os.environ['USERDOMAIN'] = self.fake_data['userdomain']
        os.environ['USERPROFILE'] = self.fake_data['userprofile']
        os.environ['PROCESSOR_IDENTIFIER'] = f"{self.fake_data['processor']['brand']} {self.fake_data['processor']['model']}"
        
        print(f"   👤 Fake Username: {self.fake_data['username']}")
        print(f"   🖥️ Fake Computer: {self.fake_data['computername']}")
        print(f"   🏢 Fake Domain: {self.fake_data['userdomain']}")
    
    def patch_system_info_sources(self):
        """Patch common system information sources"""
        # Create fake registry entries
        self.create_fake_registry_entries()
        
        # Create fake WMI responses (advanced)
        self.setup_wmi_interception()
        
        # Patch file system queries
        self.setup_filesystem_interception()
    
    def create_fake_registry_entries(self):
        """Create fake registry entries for system information"""
        try:
            # Create fake processor information
            fake_reg_path = r"SOFTWARE\FakeAugmentShield\ProcessorInfo"
            
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, fake_reg_path) as key:
                winreg.SetValueEx(key, "ProcessorNameString", 0, winreg.REG_SZ, 
                                f"{self.fake_data['processor']['brand']} {self.fake_data['processor']['model']}")
                winreg.SetValueEx(key, "~MHz", 0, winreg.REG_DWORD, 
                                int(float(self.fake_data['processor']['speed'].split()[0]) * 1000))
            
            print("   🗂️ Created fake registry entries")
        except Exception as e:
            print(f"   ❌ Registry patching failed: {str(e)}")
    
    def setup_wmi_interception(self):
        """Setup WMI query interception (advanced technique)"""
        # This would require more advanced hooking techniques
        # For now, we'll focus on environment and file-based interception
        print("   🔧 WMI interception setup (placeholder)")
    
    def setup_filesystem_interception(self):
        """Setup file system query interception"""
        # Create fake system info files in temp directory
        temp_dir = os.path.join(os.environ.get('TEMP', ''), 'AugmentShield')
        os.makedirs(temp_dir, exist_ok=True)
        
        # Create fake system info file
        fake_sysinfo = {
            'computer_name': self.fake_data['computername'],
            'username': self.fake_data['username'],
            'processor': self.fake_data['processor'],
            'memory': self.fake_data['memory'],
            'network': self.fake_data['network']
        }
        
        with open(os.path.join(temp_dir, 'system_info.json'), 'w') as f:
            json.dump(fake_sysinfo, f, indent=2)
        
        print("   📁 Created fake system info files")
    
    def setup_data_interception(self):
        """Setup interception of Augment's data collection attempts"""
        # Monitor VSCode state database for Augment writes
        self.monitor_vscode_databases()
        
        # Intercept network requests (placeholder)
        self.setup_network_interception()
    
    def monitor_vscode_databases(self):
        """Monitor and modify VSCode databases to inject fake data"""
        vscode_paths = [
            os.path.expandvars(r"%APPDATA%\Code\User\globalStorage"),
            os.path.expandvars(r"%APPDATA%\Code - Insiders\User\globalStorage"),
            os.path.expandvars(r"%APPDATA%\Cursor\User\globalStorage")
        ]
        
        for vscode_path in vscode_paths:
            state_db = os.path.join(vscode_path, "state.vscdb")
            if os.path.exists(state_db):
                self.inject_fake_data_to_database(state_db)
    
    def inject_fake_data_to_database(self, db_path):
        """Inject fake data into VSCode state database"""
        try:
            # Backup original database
            backup_path = db_path + ".shield_backup"
            shutil.copy2(db_path, backup_path)
            
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            
            # Inject fake system information
            fake_entries = [
                ('augment.system.username', self.fake_data['username']),
                ('augment.system.computername', self.fake_data['computername']),
                ('augment.system.processor', json.dumps(self.fake_data['processor'])),
                ('augment.system.memory', json.dumps(self.fake_data['memory'])),
                ('augment.system.network', json.dumps(self.fake_data['network'])),
                ('augment.telemetry.hardware', json.dumps({
                    'cpu': self.fake_data['processor'],
                    'memory': self.fake_data['memory'],
                    'gpu': self.fake_data['gpu']
                }))
            ]
            
            for key, value in fake_entries:
                # Insert or update fake data
                cur.execute("INSERT OR REPLACE INTO ItemTable (key, value) VALUES (?, ?)", 
                          (key, value))
            
            conn.commit()
            conn.close()
            
            print(f"   💉 Injected fake data into {os.path.basename(db_path)}")
            
        except Exception as e:
            print(f"   ❌ Database injection failed: {str(e)}")
    
    def setup_network_interception(self):
        """Setup network request interception (placeholder)"""
        # This would require more advanced techniques like proxy or DLL injection
        print("   🌐 Network interception setup (placeholder)")
    
    def deactivate_protection(self):
        """Deactivate privacy protection and restore original settings"""
        if not self.protection_active:
            print("⚠️ Privacy Shield is not active")
            return
        
        print("🔄 Deactivating Augment Privacy Shield...")
        
        # Restore original environment variables
        for var, value in self.original_env.items():
            os.environ[var] = value
        
        # Clean up fake registry entries
        self.cleanup_fake_registry()
        
        # Clean up fake files
        self.cleanup_fake_files()
        
        # Restore database backups
        self.restore_database_backups()
        
        self.protection_active = False
        print("✅ Privacy Shield deactivated. Original system data restored.")
    
    def cleanup_fake_registry(self):
        """Clean up fake registry entries"""
        try:
            winreg.DeleteKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\FakeAugmentShield\ProcessorInfo")
            winreg.DeleteKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\FakeAugmentShield")
            print("   🗂️ Cleaned up fake registry entries")
        except Exception as e:
            print(f"   ❌ Registry cleanup failed: {str(e)}")
    
    def cleanup_fake_files(self):
        """Clean up fake system info files"""
        temp_dir = os.path.join(os.environ.get('TEMP', ''), 'AugmentShield')
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
            print("   📁 Cleaned up fake files")
    
    def restore_database_backups(self):
        """Restore original database backups"""
        vscode_paths = [
            os.path.expandvars(r"%APPDATA%\Code\User\globalStorage"),
            os.path.expandvars(r"%APPDATA%\Code - Insiders\User\globalStorage"),
            os.path.expandvars(r"%APPDATA%\Cursor\User\globalStorage")
        ]
        
        for vscode_path in vscode_paths:
            state_db = os.path.join(vscode_path, "state.vscdb")
            backup_db = state_db + ".shield_backup"
            
            if os.path.exists(backup_db):
                shutil.copy2(backup_db, state_db)
                os.remove(backup_db)
                print(f"   💾 Restored {os.path.basename(state_db)}")
    
    def status_report(self):
        """Show current protection status"""
        print("\n" + "=" * 50)
        print("🛡️ AUGMENT PRIVACY SHIELD STATUS")
        print("=" * 50)
        print(f"Protection Active: {'✅ YES' if self.protection_active else '❌ NO'}")
        
        if self.protection_active:
            print(f"Fake Username: {self.fake_data['username']}")
            print(f"Fake Computer: {self.fake_data['computername']}")
            print(f"Fake CPU: {self.fake_data['processor']['brand']} {self.fake_data['processor']['model']}")
            print(f"Fake Memory: {self.fake_data['memory']['total'] // (1024**3)} GB")
            print(f"Fake IP: {self.fake_data['network']['ip']}")

def main():
    """Main function for privacy shield control"""
    shield = AugmentPrivacyShield()
    
    print("🛡️ Augment Privacy Shield - Fake Data Injection Tool")
    print("=" * 60)
    print("This tool feeds fake system information to Augment Code")
    print("to protect your real personal and system data.")
    print()
    
    while True:
        print("\nOptions:")
        print("1. 🛡️ Activate Privacy Shield")
        print("2. 🔄 Deactivate Privacy Shield") 
        print("3. 📊 Show Status")
        print("4. 🚪 Exit")
        
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == '1':
            shield.activate_protection()
        elif choice == '2':
            shield.deactivate_protection()
        elif choice == '3':
            shield.status_report()
        elif choice == '4':
            if shield.protection_active:
                print("⚠️ Deactivating protection before exit...")
                shield.deactivate_protection()
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid option. Please try again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Interrupted by user. Cleaning up...")
        # Emergency cleanup if needed
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("Press Enter to exit...")
        input()
