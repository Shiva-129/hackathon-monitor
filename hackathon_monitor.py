#!/usr/bin/env python3
"""
Hackathon Monitor - Windows Background Service
Monitors popular hackathon platforms and sends notifications about new events.
"""

import os
import sys
import time
import logging
import schedule
import configparser
from datetime import datetime, timedelta
from pathlib import Path

# Import custom modules
from scrapers.hackathon_scraper import HackathonScraper
from storage.excel_manager import ExcelManager
from notifications.notifier import WindowsNotifier
from service.windows_service import WindowsService

class HackathonMonitor:
    def __init__(self):
        self.setup_logging()
        self.load_config()
        self.scraper = HackathonScraper()
        self.excel_manager = ExcelManager(self.config['SETTINGS']['excel_file'])
        self.notifier = WindowsNotifier()
        
    def setup_logging(self):
        """Setup logging configuration"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / 'hackathon_monitor.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def load_config(self):
        """Load configuration from config.ini"""
        self.config = configparser.ConfigParser()

        # Handle both development and PyInstaller executable paths
        if getattr(sys, 'frozen', False):
            # Running as PyInstaller executable
            application_path = os.path.dirname(sys.executable)
            config_path = Path(application_path) / "config.ini"
        else:
            # Running as Python script
            config_path = Path("config.ini")

        if not config_path.exists():
            self.logger.error(f"config.ini not found at {config_path}!")
            # Create a default config if not found
            self.create_default_config(config_path)

        self.config.read(config_path)
        self.logger.info(f"Configuration loaded successfully from {config_path}")

    def create_default_config(self, config_path):
        """Create a default configuration file"""
        default_config = """[SETTINGS]
# How often to scrape (in hours)
scraping_interval = 6

# Excel file location
excel_file = hackathons_data.xlsx

# Enable/disable notifications
notifications_enabled = true

[PLATFORMS]
# Enable/disable specific platforms
devpost = true
mlh = true
unstop = true

[FILTERS]
# Notification filters
min_days_notice = 1
max_days_advance = 90
keywords = AI,ML,blockchain,web,mobile,hackathon
"""

        try:
            with open(config_path, 'w') as f:
                f.write(default_config)
            self.logger.info(f"Created default config file at {config_path}")
        except Exception as e:
            self.logger.error(f"Failed to create default config: {e}")
            raise
        
    def run_scraping_cycle(self):
        """Run a complete scraping cycle for all enabled platforms"""
        self.logger.info("Starting scraping cycle...")
        
        try:
            # Get existing hackathons to avoid duplicates
            existing_hackathons = self.excel_manager.get_existing_hackathons()
            
            # Scrape all enabled platforms
            new_hackathons = self.scraper.scrape_all_platforms(
                self.config, existing_hackathons
            )
            
            if new_hackathons:
                # Save new hackathons to Excel
                self.excel_manager.save_hackathons(new_hackathons)
                
                # Send notifications for new hackathons
                if self.config.getboolean('SETTINGS', 'notifications_enabled'):
                    self.send_summary_notification(new_hackathons)
                    
                self.logger.info(f"Found and saved {len(new_hackathons)} new hackathons")
            else:
                self.logger.info("No new hackathons found")
                
        except Exception as e:
            self.logger.error(f"Error during scraping cycle: {str(e)}")
            
    def send_summary_notification(self, new_hackathons):
        """Send a single summary notification for new hackathons"""
        if new_hackathons:
            excel_path = Path(self.config['SETTINGS']['excel_file']).absolute()

            # Get total count from Excel file
            try:
                total_hackathons = self.excel_manager.get_existing_hackathons()
                total_count = len(total_hackathons)
            except:
                total_count = None

            self.notifier.send_hackathon_summary_notification(
                len(new_hackathons),
                str(excel_path),
                total_count,
                new_hackathons
            )
            
    def start_monitoring(self, run_once=False):
        """Start the monitoring service"""
        self.logger.info("Hackathon Monitor started")

        # Run initial scraping
        self.run_scraping_cycle()

        if run_once:
            self.logger.info("Single run completed. Exiting...")
            return

        # Schedule scraping based on config
        interval_hours = float(self.config['SETTINGS']['scraping_interval'])

        if interval_hours < 1:
            # For testing: schedule in minutes
            interval_minutes = int(interval_hours * 60)
            schedule.every(interval_minutes).minutes.do(self.run_scraping_cycle)
            self.logger.info(f"🧪 TEST MODE: Monitoring started. Will check every {interval_minutes} minute(s). Press Ctrl+C to stop.")
        else:
            # Normal operation: schedule in hours
            schedule.every(int(interval_hours)).hours.do(self.run_scraping_cycle)
            self.logger.info(f"Monitoring started. Will check every {int(interval_hours)} hours. Press Ctrl+C to stop.")

        # Keep the service running
        try:
            while True:
                schedule.run_pending()
                time.sleep(10)  # Check every 10 seconds for better responsiveness during testing
        except KeyboardInterrupt:
            self.logger.info("Monitoring stopped by user")

    def run_once(self):
        """Run scraping once and exit"""
        self.logger.info("Running single scraping cycle...")
        self.run_scraping_cycle()
        self.logger.info("Single scraping cycle completed")
            
if __name__ == "__main__":
    import sys
    import argparse

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Hackathon Monitor')
    parser.add_argument('--once', action='store_true',
                       help='Run single scraping cycle and exit')
    parser.add_argument('--background', action='store_true',
                       help='Run in background mode (minimized)')
    parser.add_argument('--startup', action='store_true',
                       help='Run as startup application (background mode)')
    args = parser.parse_args()

    # Initialize monitor
    monitor = HackathonMonitor()

    # Handle background/startup mode
    if args.background or args.startup:
        # Try to minimize console window
        try:
            import win32gui
            import win32con
            hwnd = win32gui.GetForegroundWindow()
            win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
        except:
            pass

        print("🎯 Hackathon Monitor starting in background mode...")
        print("📊 Monitoring will run every 6 hours automatically")
        print("🔔 You'll receive notifications for new hackathons")
        print("⚙️ To stop monitoring, use Task Manager or the GUI application")
        print("💡 This window will minimize automatically")

    # Run the appropriate mode
    if args.once:
        monitor.run_once()
    else:
        monitor.start_monitoring()
