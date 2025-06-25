#!/usr/bin/env python3
"""
Service Management Script for Hackathon Monitor
Provides easy commands to manage the Windows service.
"""

import sys
import argparse
import logging
from pathlib import Path

def setup_logging():
    """Setup logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

def check_admin_privileges():
    """Check if running with administrator privileges"""
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def install_service():
    """Install the Windows service"""
    logger = logging.getLogger(__name__)
    
    if not check_admin_privileges():
        logger.error("Administrator privileges required to install service")
        return False
    
    try:
        from service.windows_service import WindowsService
        return WindowsService.install_service()
    except Exception as e:
        logger.error(f"Error installing service: {e}")
        return False

def remove_service():
    """Remove the Windows service"""
    logger = logging.getLogger(__name__)
    
    if not check_admin_privileges():
        logger.error("Administrator privileges required to remove service")
        return False
    
    try:
        from service.windows_service import WindowsService
        return WindowsService.remove_service()
    except Exception as e:
        logger.error(f"Error removing service: {e}")
        return False

def start_service():
    """Start the Windows service"""
    logger = logging.getLogger(__name__)
    
    try:
        from service.windows_service import WindowsService
        return WindowsService.start_service()
    except Exception as e:
        logger.error(f"Error starting service: {e}")
        return False

def stop_service():
    """Stop the Windows service"""
    logger = logging.getLogger(__name__)
    
    try:
        from service.windows_service import WindowsService
        return WindowsService.stop_service()
    except Exception as e:
        logger.error(f"Error stopping service: {e}")
        return False

def restart_service():
    """Restart the Windows service"""
    logger = logging.getLogger(__name__)
    
    try:
        from service.windows_service import WindowsService
        return WindowsService.restart_service()
    except Exception as e:
        logger.error(f"Error restarting service: {e}")
        return False

def status_service():
    """Check service status"""
    logger = logging.getLogger(__name__)
    
    try:
        import win32serviceutil
        from service.windows_service import HackathonMonitorService
        
        status = win32serviceutil.QueryServiceStatus(HackathonMonitorService._svc_name_)
        
        status_map = {
            1: "STOPPED",
            2: "START_PENDING", 
            3: "STOP_PENDING",
            4: "RUNNING",
            5: "CONTINUE_PENDING",
            6: "PAUSE_PENDING",
            7: "PAUSED"
        }
        
        current_status = status_map.get(status[1], "UNKNOWN")
        logger.info(f"Service status: {current_status}")
        return True
        
    except Exception as e:
        logger.error(f"Error checking service status: {e}")
        return False

def run_directly():
    """Run the monitor directly (not as service)"""
    logger = logging.getLogger(__name__)

    try:
        logger.info("Starting Hackathon Monitor directly...")
        from hackathon_monitor import HackathonMonitor

        monitor = HackathonMonitor()
        monitor.start_monitoring()

    except KeyboardInterrupt:
        logger.info("Stopped by user")
    except Exception as e:
        logger.error(f"Error running monitor: {e}")
        return False

    return True

def run_once():
    """Run the monitor once and exit"""
    logger = logging.getLogger(__name__)

    try:
        logger.info("Running Hackathon Monitor once...")
        from hackathon_monitor import HackathonMonitor

        monitor = HackathonMonitor()
        monitor.run_once()

        logger.info("Single run completed successfully!")
        return True

    except Exception as e:
        logger.error(f"Error running monitor once: {e}")
        return False

def test_notification():
    """Send a test notification"""
    logger = logging.getLogger(__name__)
    
    try:
        from notifications.notifier import WindowsNotifier
        notifier = WindowsNotifier()
        
        logger.info("Sending test notification...")
        if notifier.test_notification():
            logger.info("Test notification sent successfully!")
            return True
        else:
            logger.error("Failed to send test notification")
            return False
            
    except Exception as e:
        logger.error(f"Error sending test notification: {e}")
        return False

def main():
    """Main function"""
    logger = setup_logging()
    
    parser = argparse.ArgumentParser(description="Manage Hackathon Monitor Service")
    parser.add_argument("command", choices=[
        "install", "remove", "start", "stop", "restart",
        "status", "run", "once", "test"
    ], help="Command to execute")
    
    args = parser.parse_args()
    
    commands = {
        "install": install_service,
        "remove": remove_service,
        "start": start_service,
        "stop": stop_service,
        "restart": restart_service,
        "status": status_service,
        "run": run_directly,
        "once": run_once,
        "test": test_notification
    }
    
    command_func = commands.get(args.command)
    if command_func:
        success = command_func()
        if not success:
            sys.exit(1)
    else:
        logger.error(f"Unknown command: {args.command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
