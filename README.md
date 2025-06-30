# 🧹 Augment Code Cleaner

<div align="center">

![Augment Cleaner](https://img.shields.io/badge/Augment-Cleaner-red?style=for-the-badge&logo=windows&logoColor=white)
![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![VSCode](https://img.shields.io/badge/VS_Code-007ACC?style=for-the-badge&logo=visual-studio-code&logoColor=white)

**🚀 Complete removal tool for Augment Code from Windows VSCode installations**

</div>

## 📋 What is this?

A powerful, safe, and comprehensive tool to completely remove **Augment Code** from your Windows system. This tool finds and cleans:

- ✅ **Extension files** from VSCode, VSCode Insiders, and Cursor
- ✅ **Database entries** in VSCode state files
- ✅ **Temporary files** and cache directories
- ✅ **Settings configurations** 
- ✅ **Registry entries** (Windows)
- ✅ **Environment variables**
- ✅ **Network traces** and API data

## 🎯 Features

### 🔍 **Comprehensive Detection**
- Scans multiple VSCode-based IDEs (VSCode, Insiders, Cursor)
- Finds hidden temporary files and cache
- Detects registry entries and environment variables
- Locates API traces and network configurations

### 🛡️ **Safety First**
- **Creates backups** before making any changes
- **Interactive confirmation** - asks before cleaning
- **Detailed reporting** of what will be removed
- **Rollback capability** using backup files

### 🎨 **User-Friendly**
- **Simple interface** - just run and follow prompts
- **Clear progress** indicators and status messages
- **Detailed logs** of all actions taken
- **No technical knowledge** required

## 🚀 Quick Start

### 📥 **Download & Run**

1. **Download** the latest `AugmentCleaner.exe` from [Releases](../../releases)
2. **Right-click** → "Run as Administrator" (recommended)
3. **Follow the prompts** to scan and clean
4. **Restart VSCode** when prompted

```bash
# Or run from command line
AugmentCleaner.exe
```

### 💻 **System Requirements**
- Windows 10/11
- VSCode, VSCode Insiders, or Cursor installed
- Administrator privileges (recommended)

## 📖 How It Works

### 🔍 **Step 1: Detection**
The tool scans your system for:
```
🔍 Scanning for Augment Code installations...
✅ Found 2 VSCode-based IDE(s): VSCode, Cursor
🔌 Checking for Augment Extensions...
📦 Found Augment: augment.vscode-augment-0.467.1
🗃️ Checking temporary files and cache...
📁 Found temp directory: Augment.vscode-augment
```

### ❓ **Step 2: Confirmation**
```
⚠️  AUGMENT CODE DETECTED!
📊 Summary of findings:
   • 2 Extension(s) installed
   • 1 Database entries
   • 18 Temporary files/directories

Do you want to proceed with cleanup? (y/yes or n/no):
```

### 🧹 **Step 3: Safe Removal**
```
🚀 Starting complete Augment removal...
🗂️  Removing Augment extensions...
   ✅ Created extension backup: augment.vscode-augment-0.467.1.backup
   ✅ VSCode: Removed extension augment.vscode-augment-0.467.1
🧹 Starting database cleanup...
   ✅ Created backup: state.vscdb.bak
   ✅ VSCode: Successfully removed 1 database entries
```

## 🛠️ Advanced Usage

### 📋 **Command Line Options**
```bash
AugmentCleaner.exe --help    # Show help information
```

### 🔧 **Manual Cleanup** (If needed)
If the tool encounters locked files, manually:
1. Close all VSCode instances
2. Run the tool again
3. Restart your computer if necessary

## 🔒 Security & Privacy

### 🛡️ **What We Do:**
- ✅ Only remove Augment-related files
- ✅ Create backups for safety
- ✅ Show exactly what will be removed
- ✅ No data collection or telemetry

### 🚫 **What We DON'T Do:**
- ❌ Modify other extensions or settings
- ❌ Send data to external servers
- ❌ Access personal files or documents
- ❌ Make changes without permission

## 🆘 Troubleshooting

### ❓ **Common Issues**

**Q: "Access denied" errors?**
A: Run as Administrator and close all VSCode instances

**Q: Some files couldn't be removed?**
A: Normal if VSCode is running. Restart VSCode and run again.

**Q: Want to restore Augment?**
A: Use the backup files created (`.backup` and `.bak` extensions)

**Q: Tool says "No Augment found" but I see it?**
A: Augment might be installed differently. Contact support.

### 🔄 **Recovery**
If you need to restore Augment:
1. Find backup files (`.backup`, `.bak`)
2. Restore them to original locations
3. Restart VSCode

## 🏗️ Technical Details

- Windows Registry entries
- Environment variables

### 🧹 **Removal Process:**
1. **Backup Creation** - All files backed up before removal
2. **Extension Removal** - Deletes extension folders
3. **Database Cleanup** - Removes entries from VSCode state
4. **Cache Clearing** - Removes temporary files
5. **Settings Cleanup** - Removes configuration entries

## 🤝 Contributing

Found a bug or want to improve the tool? 

### 🐛 **Report Issues**
- Open an [Issue](../../issues) with details
- Include error messages and system info
- Describe what you expected vs what happened

### 💡 **Feature Requests**
- Suggest improvements via [Issues](../../issues)
- Explain the use case and benefit
- Check existing requests first

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is provided "as is" without warranty. While we take care to only remove Augment-related files, always backup important data before running system cleaning tools.

## 🙏 Acknowledgments

- Built with Python and PyInstaller
- Uses Windows APIs for system integration
- Inspired by the need for clean development environments

---

<div align="center">

**Made with ❤️ by [Professor David](https://github.com/professor-david)**

**⭐ Star this repo if it helped you clean your system!**

![Downloads](https://img.shields.io/github/downloads/professor-david/augment-cleaner/total?style=flat-square)
![Stars](https://img.shields.io/github/stars/professor-david/augment-cleaner?style=flat-square)
![Issues](https://img.shields.io/github/issues/professor-david/augment-cleaner?style=flat-square)

</div>
