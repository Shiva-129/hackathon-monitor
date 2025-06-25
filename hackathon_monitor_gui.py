#!/usr/bin/env python3
#!/usr/bin/env python3
"""
Hackathon Monitor - GUI Version
Windows application with graphical interface
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import subprocess
import threading
import os
import sys
from pathlib import Path
from datetime import datetime

class HackathonMonitorGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Hackathon Monitor v1.0")
        self.root.geometry("600x500")
        self.root.resizable(True, True)

        # Set window icon
        self.set_window_icon()

        # Variables
        self.monitoring_process = None
        self.is_monitoring = False

        self.create_widgets()
        self.load_settings()

    def set_window_icon(self):
        """Set the window icon for taskbar display"""
        try:
            # Try to load the logo as window icon
            logo_path = Path("logo.png")
            if logo_path.exists():
                # For PNG files, we need to convert to PhotoImage
                from PIL import Image, ImageTk
                img = Image.open(logo_path)
                img = img.resize((32, 32), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.root.iconphoto(True, photo)
            else:
                # Fallback: try ICO file
                ico_path = Path("hackathon_monitor.ico")
                if ico_path.exists():
                    self.root.iconbitmap(ico_path)
        except Exception as e:
            print(f"Could not set window icon: {e}")
            # Continue without icon
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = tk.Label(main_frame, text="🎯 Hackathon Monitor", 
                              font=("Arial", 18, "bold"), fg="#2E86AB")
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Description
        desc_label = tk.Label(main_frame, 
                             text="Monitor DevPost, MLH, and Unstop for new hackathon opportunities!",
                             font=("Arial", 10), wraplength=500)
        desc_label.grid(row=1, column=0, columnspan=3, pady=(0, 20))
        
        # Control buttons frame
        control_frame = ttk.LabelFrame(main_frame, text="Controls", padding="10")
        control_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Main action buttons
        self.scrape_once_btn = ttk.Button(control_frame, text="🔍 Scrape Once",
                                         command=self.scrape_once, width=18)
        self.scrape_once_btn.grid(row=0, column=0, padx=5, pady=5)

        self.monitor_btn = ttk.Button(control_frame, text="⏰ Start Monitoring",
                                     command=self.toggle_monitoring, width=22)
        self.monitor_btn.grid(row=0, column=1, padx=5, pady=5)

        self.stop_btn = ttk.Button(control_frame, text="⏹️ Stop All",
                                  command=self.stop_all, width=15)
        self.stop_btn.grid(row=0, column=2, padx=5, pady=5)

        # Secondary buttons
        self.excel_btn = ttk.Button(control_frame, text="📊 Open Excel",
                                   command=self.open_excel, width=18)
        self.excel_btn.grid(row=1, column=0, padx=5, pady=5)

        self.test_btn = ttk.Button(control_frame, text="🔔 Test Notification",
                                  command=self.test_notification, width=22)
        self.test_btn.grid(row=1, column=1, padx=5, pady=5)

        self.config_btn = ttk.Button(control_frame, text="⚙️ Settings",
                                    command=self.open_settings, width=15)
        self.config_btn.grid(row=1, column=2, padx=5, pady=5)
        
        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="Scraping Status", padding="10")
        status_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))

        # Status text
        self.status_label = tk.Label(status_frame, text="Ready to scrape",
                                    font=("Arial", 10, "bold"), fg="green")
        self.status_label.grid(row=0, column=0, sticky=tk.W)

        # Current platform being scraped
        self.platform_label = tk.Label(status_frame, text="",
                                      font=("Arial", 9), fg="blue")
        self.platform_label.grid(row=1, column=0, sticky=tk.W, pady=(2, 0))

        # Progress bar with percentage
        progress_container = tk.Frame(status_frame)
        progress_container.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(5, 0))

        self.progress = ttk.Progressbar(progress_container, mode='determinate', length=400)
        self.progress.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.progress_label = tk.Label(progress_container, text="0%",
                                      font=("Arial", 8), width=5)
        self.progress_label.pack(side=tk.RIGHT, padx=(5, 0))

        # Results summary
        self.results_label = tk.Label(status_frame, text="",
                                     font=("Arial", 9), fg="darkgreen")
        self.results_label.grid(row=3, column=0, sticky=tk.W, pady=(5, 0))
        
        # Log frame
        log_frame = ttk.LabelFrame(main_frame, text="Activity Log", padding="10")
        log_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=10, width=70)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)
        status_frame.columnconfigure(0, weight=1)
        progress_container.columnconfigure(0, weight=1)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # Bind close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.log("Hackathon Monitor started")
        
    def log(self, message):
        """Add message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        self.log_text.insert(tk.END, log_message)
        self.log_text.see(tk.END)
        self.root.update()
        
    def update_status(self, message, color="black"):
        """Update status label"""
        self.status_label.config(text=message, fg=color)
        self.root.update()

    def update_platform(self, platform=""):
        """Update current platform being scraped"""
        self.platform_label.config(text=platform)
        self.root.update()

    def update_progress(self, value, text=""):
        """Update progress bar and percentage"""
        self.progress['value'] = value
        self.progress_label.config(text=f"{int(value)}%")
        if text:
            self.results_label.config(text=text)
        self.root.update()

    def reset_progress(self):
        """Reset progress indicators"""
        self.progress['value'] = 0
        self.progress_label.config(text="0%")
        self.platform_label.config(text="")
        self.results_label.config(text="")
        self.root.update()

    def scrape_once(self):
        """Run single scraping cycle with progress tracking"""
        self.update_status("Starting scrape...", "blue")
        self.reset_progress()
        self.scrape_once_btn.config(state="disabled")
        self.monitor_btn.config(state="disabled")

        def scrape_with_progress():
            try:
                self.log("🔍 Starting single scraping cycle...")

                # Import scraping modules
                from scrapers.hackathon_scraper import HackathonScraper
                from storage.excel_manager import ExcelManager
                from notifications.notifier import WindowsNotifier
                import configparser

                # Load config
                config = configparser.ConfigParser()
                if not os.path.exists('config.ini'):
                    self.log("⚠️ config.ini not found, using default settings")
                    # Create minimal config for this run
                    config.add_section('SETTINGS')
                    config.set('SETTINGS', 'excel_file', 'hackathons_data.xlsx')
                    config.set('SETTINGS', 'notifications_enabled', 'true')
                    config.add_section('PLATFORMS')
                    config.set('PLATFORMS', 'devpost', 'true')
                    config.set('PLATFORMS', 'mlh', 'true')
                    config.set('PLATFORMS', 'unstop', 'true')
                else:
                    config.read('config.ini')

                # Initialize components
                scraper = HackathonScraper()
                excel_manager = ExcelManager(config['SETTINGS']['excel_file'])
                notifier = WindowsNotifier()

                # Get existing hackathons
                self.update_progress(10, "Loading existing data...")
                existing_hackathons = excel_manager.get_existing_hackathons()
                self.log(f"📊 Found {len(existing_hackathons)} existing hackathons")

                # Scrape platforms with progress tracking
                all_new_hackathons = []
                platforms = []

                if config.getboolean('PLATFORMS', 'devpost', fallback=True):
                    platforms.append(('DevPost', 'scrape_devpost'))
                if config.getboolean('PLATFORMS', 'mlh', fallback=True):
                    platforms.append(('MLH', 'scrape_mlh'))
                if config.getboolean('PLATFORMS', 'unstop', fallback=True):
                    platforms.append(('Unstop', 'scrape_unstop'))

                total_platforms = len(platforms)

                for i, (platform_name, method_name) in enumerate(platforms):
                    try:
                        self.update_platform(f"🔍 Scraping {platform_name}...")
                        progress = 20 + (i * 60 // total_platforms)
                        self.update_progress(progress)

                        self.log(f"🌐 Scraping {platform_name}...")

                        # Get the scraping method
                        if hasattr(scraper, method_name):
                            method = getattr(scraper, method_name)
                            platform_hackathons = method()

                            # Filter new hackathons
                            new_hackathons = []
                            for hackathon in platform_hackathons:
                                is_new = True
                                for existing in existing_hackathons:
                                    if (hackathon.get('name', '').lower() == existing.get('name', '').lower() and
                                        hackathon.get('platform', '') == existing.get('platform', '')):
                                        is_new = False
                                        break
                                if is_new:
                                    new_hackathons.append(hackathon)

                            all_new_hackathons.extend(new_hackathons)
                            self.log(f"✅ {platform_name}: Found {len(new_hackathons)} new hackathons")
                        else:
                            self.log(f"⚠️ {platform_name}: Scraping method not available")

                    except Exception as e:
                        self.log(f"❌ {platform_name}: Error - {str(e)}")

                # Save results
                self.update_progress(85, "Saving results...")
                self.update_platform("💾 Saving to Excel...")

                if all_new_hackathons:
                    excel_manager.save_hackathons(all_new_hackathons)
                    self.log(f"💾 Saved {len(all_new_hackathons)} new hackathons to Excel")

                    # Send notification
                    if config.getboolean('SETTINGS', 'notifications_enabled', fallback=True):
                        self.update_platform("🔔 Sending notification...")
                        total_count = len(existing_hackathons) + len(all_new_hackathons)
                        excel_path = Path(config['SETTINGS']['excel_file']).absolute()
                        notifier.send_hackathon_summary_notification(
                            len(all_new_hackathons), str(excel_path), total_count, all_new_hackathons
                        )
                        self.log("🔔 Notification sent!")
                else:
                    self.log("ℹ️ No new hackathons found")

                # Complete
                self.update_progress(100, f"Complete! Found {len(all_new_hackathons)} new hackathons")
                self.update_platform("✅ Scraping completed!")
                self.update_status("Scraping completed successfully!", "green")

                # Show summary
                summary = f"Scraping Summary:\n"
                summary += f"• Platforms checked: {total_platforms}\n"
                summary += f"• New hackathons found: {len(all_new_hackathons)}\n"
                summary += f"• Total hackathons: {len(existing_hackathons) + len(all_new_hackathons)}"

                messagebox.showinfo("Scraping Complete", summary)

            except Exception as e:
                error_msg = f"Scraping failed: {str(e)}"
                self.log(f"❌ {error_msg}")
                self.update_status("Scraping failed!", "red")
                self.update_platform("❌ Error occurred")
                messagebox.showerror("Scraping Error", error_msg)
            finally:
                self.scrape_once_btn.config(state="normal")
                self.monitor_btn.config(state="normal")

        threading.Thread(target=scrape_with_progress, daemon=True).start()
        
    def toggle_monitoring(self):
        """Start or stop 6-hour monitoring"""
        if not self.is_monitoring:
            self.start_monitoring()
        else:
            self.stop_monitoring()

    def start_monitoring(self):
        """Start continuous 6-hour monitoring"""
        try:
            self.log("⏰ Starting monitoring cycle...")
            self.update_status("Starting monitoring...", "blue")

            # Start background monitoring process
            self.monitoring_process = subprocess.Popen([
                sys.executable, "hackathon_monitor.py"
            ], cwd=os.getcwd())

            # Read config to get actual interval
            try:
                import configparser
                config = configparser.ConfigParser()
                config.read('config.ini')
                interval_hours = float(config['SETTINGS']['scraping_interval'])

                if interval_hours < 1:
                    interval_minutes = int(interval_hours * 60)
                    interval_text = f"{interval_minutes} minute(s)"
                    mode_text = "🧪 TEST MODE"
                else:
                    interval_text = f"{int(interval_hours)} hour(s)"
                    mode_text = "MONITORING"
            except:
                interval_text = "6 hours"
                mode_text = "MONITORING"

            self.is_monitoring = True
            self.monitor_btn.config(text="⏹️ Stop Monitoring")
            self.scrape_once_btn.config(state="disabled")
            self.update_status(f"{mode_text} active", "green")
            self.update_platform(f"🕐 Next scrape in {interval_text}")

            self.log(f"✅ {mode_text} started successfully! Interval: {interval_text}")

            messagebox.showinfo("Monitoring Started",
                               f"Continuous monitoring started!\n\n" +
                               f"• Scrapes every {interval_text} automatically\n" +
                               "• Runs in background\n" +
                               "• Sends notifications for new hackathons\n" +
                               "• Click 'Stop Monitoring' to stop")

        except Exception as e:
            error_msg = f"Failed to start monitoring: {str(e)}"
            self.log(f"❌ {error_msg}")
            self.update_status("Failed to start monitoring", "red")
            messagebox.showerror("Error", error_msg)

    def stop_monitoring(self):
        """Stop continuous monitoring"""
        if self.monitoring_process:
            try:
                self.monitoring_process.terminate()
                self.monitoring_process = None
                self.is_monitoring = False
                self.monitor_btn.config(text="⏰ Start Monitoring")
                self.scrape_once_btn.config(state="normal")
                self.update_status("Monitoring stopped", "orange")
                self.update_platform("")
                self.reset_progress()
                self.log("⏹️ Monitoring stopped")
            except Exception as e:
                self.log(f"❌ Error stopping monitoring: {str(e)}")

    def stop_all(self):
        """Stop all monitoring and scraping"""
        try:
            # Stop monitoring if running
            if self.is_monitoring:
                self.stop_monitoring()

            # Kill any running Python processes related to hackathon monitor
            try:
                result1 = subprocess.run(["taskkill", "/f", "/im", "python.exe", "/fi", "WINDOWTITLE eq hackathon*"],
                                       capture_output=True, text=True)
                result2 = subprocess.run(["taskkill", "/f", "/im", "pythonw.exe", "/fi", "WINDOWTITLE eq hackathon*"],
                                       capture_output=True, text=True)
                self.log("🔍 Attempted to kill related Python processes")
            except Exception as e:
                self.log(f"⚠️ Could not kill Python processes: {str(e)}")

            self.reset_progress()
            self.update_status("All processes stopped", "orange")
            self.log("🛑 All monitoring and scraping stopped")

            messagebox.showinfo("Stopped", "All monitoring and scraping processes have been stopped.")

        except Exception as e:
            error_msg = f"Error stopping processes: {str(e)}"
            self.log(f"❌ {error_msg}")
            messagebox.showerror("Error", error_msg)
                
    def test_notification(self):
        """Send test notification"""
        self.update_status("Sending test notification...", "blue")
        
        def test():
            try:
                subprocess.run([sys.executable, "manage_service.py", "test"], check=True)
                self.log("Test notification sent!")
                self.update_status("Test notification sent!", "green")
            except Exception as e:
                error_msg = f"Test failed: {str(e)}"
                self.log(error_msg)
                self.update_status("Test failed!", "red")
        
        threading.Thread(target=test, daemon=True).start()
        
    def open_excel(self):
        """Open Excel file"""
        try:
            excel_file = Path("hackathons_data.xlsx")
            if excel_file.exists():
                os.startfile(excel_file)
                self.log("Excel file opened")
                self.update_status("Excel file opened!", "green")
            else:
                messagebox.showwarning("File Not Found", 
                                     "Excel file not found.\nRun a scan first to create the file!")
                self.log("Excel file not found")
        except Exception as e:
            error_msg = f"Failed to open Excel file: {str(e)}"
            self.log(error_msg)
            messagebox.showerror("Error", error_msg)
            
    def open_settings(self):
        """Open settings window"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("400x300")
        settings_window.resizable(False, False)
        
        # Settings content
        ttk.Label(settings_window, text="Settings", font=("Arial", 14, "bold")).pack(pady=10)
        ttk.Label(settings_window, text="Edit config.ini file to change settings").pack(pady=5)
        
        ttk.Button(settings_window, text="Open Config File", 
                  command=lambda: os.startfile("config.ini")).pack(pady=10)
        ttk.Button(settings_window, text="Close", 
                  command=settings_window.destroy).pack(pady=5)
        
    def load_settings(self):
        """Load settings from config file"""
        try:
            # Could load settings here if needed
            pass
        except Exception as e:
            self.log(f"Error loading settings: {str(e)}")
            
    def on_closing(self):
        """Handle window closing"""
        if self.is_monitoring:
            if messagebox.askokcancel("Quit", "Monitoring is active. Stop monitoring and quit?"):
                self.stop_monitoring()
                self.root.destroy()
        else:
            self.root.destroy()
    
    def run(self):
        """Start the GUI"""
        self.root.mainloop()

if __name__ == "__main__":
    app = HackathonMonitorGUI()
    app.run()
