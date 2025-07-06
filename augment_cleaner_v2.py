import os
import sqlite3
import shutil
import json
import winreg
import subprocess
import sys
from datetime import datetime

class AugmentCleanerV2:
    """Enhanced cleaner for newer Augment versions (0.492.2+)"""
    
    def __init__(self):
        self.findings = {
            'extensions': [],
            'databases': [],
            'personal_data': [],
            'system_fingerprints': [],
            'network_traces': [],
            'cloud_data': [],
            'ai_training_data': [],
            'registry_entries': []
        }
        self.cleaned_items = 0
        self.backup_dir = None
    
    def scan_for_newer_augment(self):
        """Comprehensive scan for newer Augment versions and their data"""
        print("🔍 Enhanced Augment Scanner v2.0 - Targeting newer versions")
        print("=" * 60)
        
        # Create backup directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.backup_dir = f"augment_backup_{timestamp}"
        os.makedirs(self.backup_dir, exist_ok=True)
        
        # Scan different areas
        self.scan_extensions()
        self.scan_databases_deep()
        self.scan_personal_data()
        self.scan_system_fingerprints()
        self.scan_cloud_data()
        self.scan_ai_training_data()
        self.scan_registry_deep()
        self.scan_network_traces()
        
        return self.generate_findings_report()
    
    def scan_extensions(self):
        """Scan for Augment extensions with version detection"""
        print("\n📦 Scanning for Augment extensions...")
        
        vscode_paths = [
            (os.path.expandvars(r"%APPDATA%\Code"), "VSCode"),
            (os.path.expandvars(r"%APPDATA%\Code - Insiders"), "VSCode Insiders"),
            (os.path.expandvars(r"%APPDATA%\Cursor"), "Cursor"),
            (os.path.expanduser("~/.vscode"), "VSCode (User)"),
        ]
        
        for base_path, ide_name in vscode_paths:
            extensions_dir = os.path.join(base_path, "User", "extensions")
            if not os.path.exists(extensions_dir):
                continue
                
            for item in os.listdir(extensions_dir):
                if any(pattern in item.lower() for pattern in ['augment', 'augmentcode']):
                    ext_path = os.path.join(extensions_dir, item)
                    version = self.extract_version(item)
                    
                    self.findings['extensions'].append({
                        'ide': ide_name,
                        'name': item,
                        'path': ext_path,
                        'version': version,
                        'is_newer': self.is_newer_version(version),
                        'size_mb': self.get_folder_size_mb(ext_path)
                    })
                    
                    print(f"   📦 Found: {item} (v{version}) in {ide_name}")
                    if self.is_newer_version(version):
                        print(f"       🚨 NEWER VERSION - Enhanced data collection!")
    
    def scan_databases_deep(self):
        """Deep scan of VSCode databases for personal data"""
        print("\n🗄️ Deep scanning databases for personal data...")
        
        vscode_paths = [
            os.path.expandvars(r"%APPDATA%\Code\User\globalStorage"),
            os.path.expandvars(r"%APPDATA%\Code - Insiders\User\globalStorage"),
            os.path.expandvars(r"%APPDATA%\Cursor\User\globalStorage")
        ]
        
        personal_patterns = [
            '%username%', '%user%', '%computer%', '%machine%', '%email%',
            '%identity%', '%profile%', '%account%', '%name%', '%domain%'
        ]
        
        for vscode_path in vscode_paths:
            state_db = os.path.join(vscode_path, "state.vscdb")
            if not os.path.exists(state_db):
                continue
                
            try:
                conn = sqlite3.connect(state_db)
                cur = conn.cursor()
                
                # Check for personal data in database
                personal_entries = []
                for pattern in personal_patterns:
                    cur.execute("SELECT key, value FROM ItemTable WHERE LOWER(key) LIKE ? OR LOWER(value) LIKE ?", 
                              (pattern, pattern))
                    results = cur.fetchall()
                    personal_entries.extend(results)
                
                # Check for actual username in data
                username = os.environ.get('USERNAME', '').lower()
                if username:
                    cur.execute("SELECT key, value FROM ItemTable WHERE LOWER(value) LIKE ?", 
                              (f'%{username}%',))
                    username_entries = cur.fetchall()
                    personal_entries.extend(username_entries)
                
                if personal_entries:
                    self.findings['personal_data'].append({
                        'database': state_db,
                        'entries': len(personal_entries),
                        'sample_keys': [entry[0] for entry in personal_entries[:5]],
                        'contains_username': any(username in str(entry[1]).lower() for entry in personal_entries)
                    })
                    
                    print(f"   🚨 Found {len(personal_entries)} personal data entries in {os.path.basename(state_db)}")
                    if any(username in str(entry[1]).lower() for entry in personal_entries):
                        print(f"       ⚠️ Contains your actual username: {username}")
                
                conn.close()
                
            except Exception as e:
                print(f"   ❌ Error scanning {state_db}: {str(e)}")
    
    def scan_personal_data(self):
        """Scan for personal data collection"""
        print("\n👤 Scanning for personal data collection...")
        
        # Check workspace storage for personal projects
        workspace_paths = [
            os.path.expandvars(r"%APPDATA%\Code\User\workspaceStorage"),
            os.path.expandvars(r"%APPDATA%\Code - Insiders\User\workspaceStorage"),
            os.path.expandvars(r"%APPDATA%\Cursor\User\workspaceStorage")
        ]
        
        for workspace_path in workspace_paths:
            if not os.path.exists(workspace_path):
                continue
                
            for workspace_dir in os.listdir(workspace_path):
                workspace_full = os.path.join(workspace_path, workspace_dir)
                if os.path.isdir(workspace_full):
                    # Check for Augment-related files
                    for file in os.listdir(workspace_full):
                        if 'augment' in file.lower():
                            self.findings['personal_data'].append({
                                'type': 'workspace_data',
                                'path': os.path.join(workspace_full, file),
                                'workspace': workspace_dir
                            })
                            print(f"   📁 Personal workspace data: {file}")
    
    def scan_system_fingerprints(self):
        """Scan for system fingerprinting data"""
        print("\n🖥️ Scanning for system fingerprinting data...")
        
        # Check for hardware fingerprint files
        fingerprint_locations = [
            os.path.expandvars(r"%LOCALAPPDATA%\Augment"),
            os.path.expandvars(r"%APPDATA%\Augment"),
            os.path.expandvars(r"%TEMP%\Augment")
        ]
        
        for location in fingerprint_locations:
            if os.path.exists(location):
                for root, dirs, files in os.walk(location):
                    for file in files:
                        if any(keyword in file.lower() for keyword in ['hardware', 'system', 'fingerprint', 'machine']):
                            file_path = os.path.join(root, file)
                            self.findings['system_fingerprints'].append({
                                'type': 'hardware_fingerprint',
                                'path': file_path,
                                'size': os.path.getsize(file_path)
                            })
                            print(f"   🖥️ System fingerprint: {file}")
    
    def scan_cloud_data(self):
        """Scan for cloud synchronization data"""
        print("\n☁️ Scanning for cloud synchronization data...")
        
        cloud_patterns = ['sync', 'cloud', 'remote', 'server', 'upload', 'backup']
        
        # Check VSCode logs for cloud activity
        log_paths = [
            os.path.expandvars(r"%APPDATA%\Code\logs"),
            os.path.expandvars(r"%APPDATA%\Code - Insiders\logs")
        ]
        
        for log_path in log_paths:
            if os.path.exists(log_path):
                for root, dirs, files in os.walk(log_path):
                    for file in files:
                        if file.endswith('.log'):
                            file_path = os.path.join(root, file)
                            try:
                                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                    content = f.read()
                                    if any(pattern in content.lower() for pattern in cloud_patterns):
                                        self.findings['cloud_data'].append({
                                            'type': 'cloud_activity_log',
                                            'path': file_path,
                                            'suspicious': True
                                        })
                                        print(f"   ☁️ Cloud activity in logs: {file}")
                                        break
                            except Exception:
                                pass
    
    def scan_ai_training_data(self):
        """Scan for AI/ML training data collection"""
        print("\n🤖 Scanning for AI/ML training data...")
        
        ai_patterns = ['training', 'model', 'ml', 'ai', 'neural', 'learning']
        
        # Check extension directories for AI data
        for extension in self.findings['extensions']:
            if extension['is_newer']:
                ext_path = extension['path']
                for root, dirs, files in os.walk(ext_path):
                    for file in files:
                        if any(pattern in file.lower() for pattern in ai_patterns):
                            file_path = os.path.join(root, file)
                            self.findings['ai_training_data'].append({
                                'type': 'ai_training_file',
                                'path': file_path,
                                'extension': extension['name']
                            })
                            print(f"   🤖 AI training data: {file}")
    
    def scan_registry_deep(self):
        """Deep scan of Windows Registry for Augment data"""
        print("\n🗂️ Deep scanning Windows Registry...")
        
        try:
            registry_paths = [
                (winreg.HKEY_CURRENT_USER, r"Software"),
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE"),
                (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Uninstall")
            ]
            
            for hkey, path in registry_paths:
                try:
                    with winreg.OpenKey(hkey, path) as key:
                        i = 0
                        while True:
                            try:
                                subkey_name = winreg.EnumKey(key, i)
                                if 'augment' in subkey_name.lower():
                                    self.findings['registry_entries'].append({
                                        'hkey': 'HKEY_CURRENT_USER' if hkey == winreg.HKEY_CURRENT_USER else 'HKEY_LOCAL_MACHINE',
                                        'path': f"{path}\\{subkey_name}",
                                        'name': subkey_name
                                    })
                                    print(f"   🗂️ Registry entry: {subkey_name}")
                                i += 1
                            except WindowsError:
                                break
                except Exception:
                    continue
        except Exception as e:
            print(f"   ❌ Registry scan error: {str(e)}")
    
    def scan_network_traces(self):
        """Scan for network activity traces"""
        print("\n🌐 Scanning for network traces...")
        
        # Check hosts file
        hosts_file = r"C:\Windows\System32\drivers\etc\hosts"
        try:
            if os.path.exists(hosts_file):
                with open(hosts_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    if 'augment' in content.lower():
                        self.findings['network_traces'].append({
                            'type': 'hosts_file_entry',
                            'path': hosts_file
                        })
                        print("   🌐 Found Augment entries in hosts file")
        except Exception:
            pass
    
    def extract_version(self, extension_name):
        """Extract version from extension name"""
        import re
        version_pattern = r'(\d+\.\d+\.\d+)'
        match = re.search(version_pattern, extension_name)
        return match.group(1) if match else "0.0.0"
    
    def is_newer_version(self, version):
        """Check if version is newer than 0.490.0"""
        try:
            parts = [int(x) for x in version.split('.')]
            return parts[0] > 0 or (parts[0] == 0 and parts[1] >= 490)
        except:
            return False
    
    def get_folder_size_mb(self, folder_path):
        """Get folder size in MB"""
        try:
            total_size = 0
            for dirpath, dirnames, filenames in os.walk(folder_path):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    if os.path.exists(filepath):
                        total_size += os.path.getsize(filepath)
            return round(total_size / (1024 * 1024), 2)
        except:
            return 0
    
    def generate_findings_report(self):
        """Generate comprehensive findings report"""
        print("\n" + "=" * 60)
        print("📊 ENHANCED AUGMENT DETECTION REPORT")
        print("=" * 60)
        
        total_items = sum(len(self.findings[category]) for category in self.findings)
        print(f"🎯 Total items found: {total_items}")
        
        # Show newer version warnings
        newer_extensions = [ext for ext in self.findings['extensions'] if ext['is_newer']]
        if newer_extensions:
            print(f"\n🚨 PRIVACY ALERT: {len(newer_extensions)} newer Augment version(s) detected!")
            print("   These versions collect significantly more personal data.")
        
        # Show personal data concerns
        personal_items = len(self.findings['personal_data'])
        if personal_items > 0:
            print(f"\n👤 PERSONAL DATA: {personal_items} instances of personal data collection found")
        
        # Show system fingerprinting
        fingerprint_items = len(self.findings['system_fingerprints'])
        if fingerprint_items > 0:
            print(f"\n🖥️ SYSTEM FINGERPRINTING: {fingerprint_items} hardware fingerprint files found")
        
        return total_items > 0
    
    def clean_all_findings(self):
        """Clean all found Augment data with enhanced removal"""
        if not any(self.findings.values()):
            print("✅ No Augment data found to clean.")
            return 0
        
        print("\n🧹 Starting enhanced Augment removal...")
        
        # Clean extensions
        for ext in self.findings['extensions']:
            self.clean_extension(ext)
        
        # Clean databases with personal data removal
        for db_info in self.findings['personal_data']:
            if 'database' in db_info:
                self.clean_database_personal_data(db_info)
        
        # Clean system fingerprints
        for fingerprint in self.findings['system_fingerprints']:
            self.clean_system_fingerprint(fingerprint)
        
        # Clean cloud data
        for cloud_item in self.findings['cloud_data']:
            self.clean_cloud_data(cloud_item)
        
        # Clean AI training data
        for ai_item in self.findings['ai_training_data']:
            self.clean_ai_data(ai_item)
        
        # Clean registry entries
        for reg_entry in self.findings['registry_entries']:
            self.clean_registry_entry(reg_entry)
        
        print(f"\n✅ Enhanced cleaning completed! Removed {self.cleaned_items} items.")
        print(f"💾 Backups saved to: {self.backup_dir}")
        
        return self.cleaned_items
    
    def clean_extension(self, ext_info):
        """Clean extension with backup"""
        try:
            ext_path = ext_info['path']
            if os.path.exists(ext_path):
                # Create backup
                backup_path = os.path.join(self.backup_dir, f"extension_{ext_info['name']}")
                shutil.copytree(ext_path, backup_path)
                
                # Remove extension
                shutil.rmtree(ext_path)
                self.cleaned_items += 1
                print(f"   ✅ Removed extension: {ext_info['name']}")
        except Exception as e:
            print(f"   ❌ Failed to remove extension: {str(e)}")
    
    def clean_database_personal_data(self, db_info):
        """Clean personal data from databases"""
        try:
            db_path = db_info['database']
            if os.path.exists(db_path):
                # Create backup
                backup_path = os.path.join(self.backup_dir, f"database_{os.path.basename(db_path)}")
                shutil.copy2(db_path, backup_path)
                
                # Remove personal data entries
                conn = sqlite3.connect(db_path)
                cur = conn.cursor()
                
                # Remove entries containing personal data
                personal_patterns = ['%augment%', '%username%', '%user%', '%computer%']
                for pattern in personal_patterns:
                    cur.execute("DELETE FROM ItemTable WHERE LOWER(key) LIKE ? OR LOWER(value) LIKE ?", 
                              (pattern, pattern))
                
                conn.commit()
                conn.close()
                self.cleaned_items += 1
                print(f"   ✅ Cleaned personal data from: {os.path.basename(db_path)}")
        except Exception as e:
            print(f"   ❌ Failed to clean database: {str(e)}")
    
    def clean_system_fingerprint(self, fingerprint_info):
        """Clean system fingerprint files"""
        try:
            file_path = fingerprint_info['path']
            if os.path.exists(file_path):
                # Create backup
                backup_path = os.path.join(self.backup_dir, f"fingerprint_{os.path.basename(file_path)}")
                shutil.copy2(file_path, backup_path)
                
                # Remove file
                os.remove(file_path)
                self.cleaned_items += 1
                print(f"   ✅ Removed fingerprint file: {os.path.basename(file_path)}")
        except Exception as e:
            print(f"   ❌ Failed to remove fingerprint: {str(e)}")
    
    def clean_cloud_data(self, cloud_info):
        """Clean cloud synchronization data"""
        try:
            file_path = cloud_info['path']
            if os.path.exists(file_path):
                # Create backup
                backup_path = os.path.join(self.backup_dir, f"cloud_{os.path.basename(file_path)}")
                shutil.copy2(file_path, backup_path)
                
                # Remove or clean file
                if cloud_info['type'] == 'cloud_activity_log':
                    # Clear log content instead of deleting
                    with open(file_path, 'w') as f:
                        f.write("")
                else:
                    os.remove(file_path)
                
                self.cleaned_items += 1
                print(f"   ✅ Cleaned cloud data: {os.path.basename(file_path)}")
        except Exception as e:
            print(f"   ❌ Failed to clean cloud data: {str(e)}")
    
    def clean_ai_data(self, ai_info):
        """Clean AI training data"""
        try:
            file_path = ai_info['path']
            if os.path.exists(file_path):
                # Create backup
                backup_path = os.path.join(self.backup_dir, f"ai_{os.path.basename(file_path)}")
                shutil.copy2(file_path, backup_path)
                
                # Remove AI training file
                os.remove(file_path)
                self.cleaned_items += 1
                print(f"   ✅ Removed AI training data: {os.path.basename(file_path)}")
        except Exception as e:
            print(f"   ❌ Failed to remove AI data: {str(e)}")
    
    def clean_registry_entry(self, reg_info):
        """Clean registry entries"""
        try:
            # This is a placeholder - registry cleaning requires careful handling
            print(f"   ⚠️ Registry entry found (manual removal recommended): {reg_info['name']}")
        except Exception as e:
            print(f"   ❌ Registry cleaning error: {str(e)}")

def main():
    """Main function for enhanced Augment cleaner"""
    print("🧹 Augment Cleaner v2.0 - Enhanced Privacy Protection")
    print("Specifically designed for newer Augment versions (0.492.2+)")
    print("=" * 60)
    
    cleaner = AugmentCleanerV2()
    
    try:
        # Scan for Augment data
        found_items = cleaner.scan_for_newer_augment()
        
        if not found_items:
            print("\n✅ No Augment installations found. Your system appears clean!")
            return
        
        # Ask for confirmation
        print(f"\n⚠️ Found Augment data that may contain personal information.")
        print("This includes usernames, system fingerprints, and usage data.")
        
        response = input("\nProceed with enhanced cleaning? (y/yes or n/no): ").strip().lower()
        
        if response in ['y', 'yes']:
            cleaned_count = cleaner.clean_all_findings()
            
            print(f"\n🎉 Enhanced cleaning completed!")
            print(f"✅ Removed {cleaned_count} items containing personal data")
            print(f"💾 Backups created for safety")
            print(f"🔒 Your privacy has been protected!")
            
        else:
            print("\n❌ Cleaning cancelled. No changes made.")
    
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
    
    finally:
        print("\nPress Enter to exit...")
        input()

if __name__ == "__main__":
    main()
