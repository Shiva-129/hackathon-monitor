# 🎯 Hackathon Monitor v1.0.0 - Installation Guide

## 📦 **Quick Installation**

### **Download & Install**
1. **Download**: [`HackathonMonitor_v1.0.0_Installer.exe`](dist/HackathonMonitor_v1.0.0_Installer.exe) (10.7 MB)
2. **Run**: Double-click the downloaded file
3. **Choose Options**:
   - Select installation path
   - ✅ **Enable "Start automatically when Windows boots"** (Recommended)
4. **Install**: Click "INSTALL" and wait for completion
5. **Auto-Start**: Application will start automatically on boot (if enabled)

### **System Requirements**
- **OS**: Windows 10/11
- **Python**: 3.8+ (installer will check and guide you)
- **Browser**: Chrome (for web scraping)
- **Internet**: Required for dependency installation

## 🚀 **What Gets Installed**

The installer automatically sets up:

### **Application Files**
```
HackathonMonitor/
├── hackathon_monitor_gui.py     # Main GUI application
├── hackathon_monitor.py         # Background monitoring
├── config.ini                  # Configuration settings
├── requirements.txt            # Python dependencies
├── run_hackathon_monitor.bat   # Easy launcher
├── notifications/              # Notification system
├── scrapers/                   # Web scraping modules
├── storage/                    # Excel data management
└── service/                    # Windows service support
```

### **Dependencies**
All Python packages are automatically installed:
- `requests` - Web scraping
- `beautifulsoup4` - HTML parsing
- `selenium` - Browser automation
- `openpyxl` - Excel file handling
- `schedule` - Task scheduling
- `win10toast` - Windows notifications
- `webdriver-manager` - Chrome driver
- And more...

### **Shortcuts**
- **Desktop**: "Hackathon Monitor" shortcut
- **Start Menu**: Application entry
- **Quick Launch**: Batch file launchers

## 🎯 **Using Hackathon Monitor**

After installation, you can:

### **Launch the Application**
- **Desktop Shortcut**: Double-click "Hackathon Monitor"
- **Start Menu**: Search for "Hackathon Monitor"
- **Manual**: Navigate to installation folder → `run_hackathon_monitor.bat`

### **Main Features**
1. **🔍 Scrape Once**: Single scan of all platforms
2. **⏰ Start Monitoring**: Continuous 6-hour monitoring
3. **📊 Open Excel**: View collected hackathon data
4. **🔔 Test Notification**: Verify notification system
5. **⚙️ Settings**: Configure monitoring preferences

### **Supported Platforms**
- **DevPost**: Main hackathons page
- **MLH**: Major League Hacking events
- **Unstop**: Competitions and hackathons

## 📊 **How It Works**

### **Auto-Startup Mode (Recommended)**
1. **Boot-Time Start**: Automatically starts when Windows boots
2. **Background Monitoring**: Runs silently in background every 6 hours
3. **Smart Detection**: Identifies new hackathons automatically
4. **Instant Notifications**: Sends Windows notifications for new finds
5. **Click-to-Open**: Click notifications to open Excel data
6. **No User Intervention**: Works completely automatically

### **Manual Mode**
1. **On-Demand Scanning**: Run when you want to check for hackathons
2. **GUI Interface**: Use the application window for control
3. **Scheduled Monitoring**: Start 6-hour cycles manually

## 🔧 **Troubleshooting**

### **If Installation Fails**
- **Run as Administrator**: Right-click installer → "Run as administrator"
- **Check Python**: Ensure Python 3.8+ is installed from python.org
- **Internet Connection**: Verify stable internet for dependency downloads

### **If Application Won't Start**
- **Check Python PATH**: Ensure Python is added to system PATH
- **Reinstall Dependencies**: Navigate to install folder, run `pip install -r requirements.txt`
- **Use CLI Version**: Try command-line version if GUI fails

### **If Notifications Don't Work**
- **Windows Settings**: Check Windows notification settings
- **Test Feature**: Use "🔔 Test Notification" button in app
- **Permissions**: Ensure app has notification permissions

## 📁 **Installation Locations**

### **Default Installation**
- **Path**: `C:\Users\[YourName]\HackathonMonitor`
- **Data Files**: Excel files saved in same directory
- **Logs**: Application logs in installation folder

### **Custom Installation**
- Choose different path during installation
- All files and shortcuts will be created accordingly

## 🔄 **Updating**

To update to a newer version:
1. **Download** new installer
2. **Run installer** (will detect existing installation)
3. **Choose** to upgrade or install fresh
4. **Existing data** will be preserved

## 🗑️ **Uninstalling**

To remove Hackathon Monitor:
1. **Delete** installation folder
2. **Remove** desktop shortcuts
3. **Optional**: Uninstall Python dependencies if not needed elsewhere

## 💡 **Tips for Best Results**

- **First Run**: Use "🔍 Scrape Once" to test and populate initial data
- **Stable Internet**: Ensure reliable connection for web scraping
- **Chrome Updated**: Keep Chrome browser updated for best compatibility
- **Excel Closed**: Don't keep Excel files open during scraping

## 📞 **Support**

If you encounter issues:
1. **Check Logs**: Look at console output in the application
2. **Verify Setup**: Ensure all requirements are met
3. **Test Components**: Use individual test features
4. **Reinstall**: Try fresh installation if problems persist

---

## 🎉 **Ready to Discover Hackathons!**

Once installed, Hackathon Monitor will automatically:
- **🔍 Scan** popular platforms every 6 hours
- **📊 Save** all hackathon data to Excel files
- **🔔 Notify** you instantly about new opportunities
- **📱 Open** Excel when you click notifications

**Happy Hackathon Hunting! 🎯**
