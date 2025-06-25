"""
Windows Service Module
Handles running the hackathon monitor as a Windows service.
"""

import sys
import os
import logging
import time
import win32serviceutil
import win32service
import win32event
import servicemanager
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

class HackathonMonitorService(win32serviceutil.ServiceFramework):
    _svc_name_ = "HackathonMonitor"
    _svc_display_name_ = "Hackathon Monitor Service"
    _svc_description_ = "Monitors hackathon platforms and sends notifications about new events"
    
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.is_running = True
        
        # Setup logging for service
        self.setup_service_logging()
        
    def setup_service_logging(self):
        """Setup logging for the Windows service"""
        log_dir = project_root / "logs"
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / 'service.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def SvcStop(self):
        """Stop the service"""
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.is_running = False
        self.logger.info("Hackathon Monitor Service stopped")
        
    def SvcDoRun(self):
        """Main service execution"""
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, '')
        )
        
        self.logger.info("Hackathon Monitor Service started")
        self.main()
        
    def main(self):
        """Main service loop"""
        try:
            # Change to project directory
            os.chdir(project_root)
            
            # Import and start the monitor
            from hackathon_monitor import HackathonMonitor
            
            monitor = HackathonMonitor()
            
            # Run the monitoring in a separate thread-like manner
            import threading
            monitor_thread = threading.Thread(target=monitor.start_monitoring)
            monitor_thread.daemon = True
            monitor_thread.start()
            
            # Wait for stop signal
            while self.is_running:
                # Wait for stop event with timeout
                rc = win32event.WaitForSingleObject(self.hWaitStop, 5000)
                if rc == win32event.WAIT_OBJECT_0:
                    break
                    
        except Exception as e:
            self.logger.error(f"Error in service main loop: {e}")
            servicemanager.LogErrorMsg(f"Hackathon Monitor Service error: {e}")

class WindowsService:
    """Helper class for managing the Windows service"""
    
    @staticmethod
    def install_service():
        """Install the Windows service"""
        try:
            win32serviceutil.InstallService(
                HackathonMonitorService._svc_reg_class_,
                HackathonMonitorService._svc_name_,
                HackathonMonitorService._svc_display_name_,
                startType=win32service.SERVICE_AUTO_START,
                description=HackathonMonitorService._svc_description_
            )
            print("Service installed successfully!")
            return True
        except Exception as e:
            print(f"Error installing service: {e}")
            return False
            
    @staticmethod
    def remove_service():
        """Remove the Windows service"""
        try:
            win32serviceutil.RemoveService(HackathonMonitorService._svc_name_)
            print("Service removed successfully!")
            return True
        except Exception as e:
            print(f"Error removing service: {e}")
            return False
            
    @staticmethod
    def start_service():
        """Start the Windows service"""
        try:
            win32serviceutil.StartService(HackathonMonitorService._svc_name_)
            print("Service started successfully!")
            return True
        except Exception as e:
            print(f"Error starting service: {e}")
            return False
            
    @staticmethod
    def stop_service():
        """Stop the Windows service"""
        try:
            win32serviceutil.StopService(HackathonMonitorService._svc_name_)
            print("Service stopped successfully!")
            return True
        except Exception as e:
            print(f"Error stopping service: {e}")
            return False
            
    @staticmethod
    def restart_service():
        """Restart the Windows service"""
        try:
            win32serviceutil.RestartService(HackathonMonitorService._svc_name_)
            print("Service restarted successfully!")
            return True
        except Exception as e:
            print(f"Error restarting service: {e}")
            return False

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(HackathonMonitorService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(HackathonMonitorService)
