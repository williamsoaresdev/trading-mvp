#!/usr/bin/env python3
"""
Trading MVP - Real-Time Orchestrator
Starts all services simultaneously for real-time trading
"""

import os
import sys
import subprocess
import platform
import time
import signal
import threading
from pathlib import Path
import requests
import json

class ServiceOrchestrator:
    """Manages all trading services in real-time mode"""
    
    def __init__(self):
        self.processes = {}
        self.running = False
        self.base_dir = Path(__file__).parent
        
    def log(self, service: str, message: str):
        """Log message with timestamp and service name"""
        timestamp = time.strftime("%H:%M:%S")
        print(f"[{timestamp}] [{service:10}] {message}")
    
    def check_prerequisites(self):
        """Check if all tools are available"""
        self.log("SYSTEM", "Checking prerequisites...")
        
        # Check Python
        try:
            result = subprocess.run(["python", "--version"], capture_output=True, text=True)
            self.log("SYSTEM", f"✅ Python: {result.stdout.strip()}")
        except FileNotFoundError:
            self.log("SYSTEM", "❌ Python not found!")
            return False
        
        # Check .NET
        try:
            result = subprocess.run(["dotnet", "--version"], capture_output=True, text=True)
            self.log("SYSTEM", f"✅ .NET: {result.stdout.strip()}")
        except FileNotFoundError:
            self.log("SYSTEM", "❌ .NET not found!")
            return False
        
        # Check Node.js
        try:
            result = subprocess.run(["node", "--version"], capture_output=True, text=True)
            self.log("SYSTEM", f"✅ Node.js: {result.stdout.strip()}")
        except FileNotFoundError:
            self.log("SYSTEM", "❌ Node.js not found!")
            return False
        
        return True
    
    def start_python_api(self):
        """Start Python FastAPI with WebSocket support"""
        self.log("API", "Starting real-time Python API...")\n        
        python_dir = self.base_dir / "python"
        
        # Determine activation command
        if platform.system() == "Windows":
            activate_cmd = str(python_dir / ".venv" / "Scripts" / "activate.bat")
            cmd = f'"{activate_cmd}" && python -m uvicorn app.realtime_service:app --host 0.0.0.0 --port 8000 --reload'
        else:
            activate_cmd = str(python_dir / ".venv" / "bin" / "activate")
            cmd = f'source "{activate_cmd}" && python -m uvicorn app.realtime_service:app --host 0.0.0.0 --port 8000 --reload'
        
        process = subprocess.Popen(
            cmd,
            shell=True,
            cwd=python_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        self.processes["api"] = process
        
        # Monitor output in separate thread
        def monitor_api():
            for line in iter(process.stdout.readline, ''):
                if line.strip():
                    self.log("API", line.strip())
            process.stdout.close()
        
        threading.Thread(target=monitor_api, daemon=True).start()
        self.log("API", "Started on http://localhost:8000")
    
    def start_angular_dashboard(self):
        """Start Angular dashboard"""
        self.log("DASHBOARD", "Starting Angular dashboard...")
        
        dashboard_dir = self.base_dir / "trading-dashboard"
        
        process = subprocess.Popen(
            ["npm", "start"],
            cwd=dashboard_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        self.processes["dashboard"] = process
        
        # Monitor output
        def monitor_dashboard():
            for line in iter(process.stdout.readline, ''):
                if line.strip():
                    self.log("DASHBOARD", line.strip())
            process.stdout.close()
        
        threading.Thread(target=monitor_dashboard, daemon=True).start()
        self.log("DASHBOARD", "Starting on http://localhost:4200")
    
    def start_dotnet_executor(self):
        """Start .NET trading executor"""
        self.log("EXECUTOR", "Starting .NET trading executor...")
        
        executor_dir = self.base_dir / "dotnet" / "TradingExecutor"
        
        process = subprocess.Popen(
            ["dotnet", "run"],
            cwd=executor_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        self.processes["executor"] = process
        
        # Monitor output
        def monitor_executor():
            for line in iter(process.stdout.readline, ''):
                if line.strip():
                    self.log("EXECUTOR", line.strip())
            process.stdout.close()
        
        threading.Thread(target=monitor_executor, daemon=True).start()
        self.log("EXECUTOR", "Started trading executor")
    
    def wait_for_api(self, timeout=30):
        """Wait for API to be ready"""
        self.log("SYSTEM", "Waiting for API to be ready...")
        
        for i in range(timeout):
            try:
                response = requests.get("http://localhost:8000/health", timeout=2)
                if response.status_code == 200:
                    self.log("SYSTEM", "✅ API is ready!")
                    return True
            except requests.exceptions.RequestException:
                pass
            
            time.sleep(1)
            if i % 5 == 0:
                self.log("SYSTEM", f"Still waiting for API... ({i}/{timeout}s)")
        
        self.log("SYSTEM", "❌ API failed to start within timeout")
        return False
    
    def start_real_time_trading(self):
        """Start real-time trading via API"""
        try:
            response = requests.post("http://localhost:8000/trading/start", 
                                   json={"symbol": "BTC/USDT", "interval_seconds": 30})
            if response.status_code == 200:
                self.log("TRADING", "✅ Real-time trading started!")
                return True
            else:
                self.log("TRADING", f"❌ Failed to start trading: {response.text}")
                return False
        except Exception as e:
            self.log("TRADING", f"❌ Error starting trading: {e}")
            return False
    
    def stop_all_services(self):
        """Stop all running services"""
        self.log("SYSTEM", "Stopping all services...")
        self.running = False
        
        # Stop real-time trading
        try:
            requests.post("http://localhost:8000/trading/stop", timeout=2)
            self.log("TRADING", "Real-time trading stopped")
        except:
            pass
        
        # Terminate all processes
        for name, process in self.processes.items():
            try:
                if process.poll() is None:  # Still running
                    self.log(name.upper(), "Stopping...")
                    process.terminate()
                    
                    # Wait a bit for graceful shutdown
                    try:
                        process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        self.log(name.upper(), "Force killing...")
                        process.kill()
                        
                    self.log(name.upper(), "Stopped")
            except Exception as e:
                self.log(name.upper(), f"Error stopping: {e}")
        
        self.processes.clear()
    
    def run_real_time_system(self):
        """Run the complete real-time trading system"""
        if not self.check_prerequisites():
            return False
        
        self.running = True
        
        try:
            # Start services in order
            self.log("SYSTEM", "🚀 Starting Real-Time Trading System")
            print("=" * 60)
            
            # 1. Start Python API
            self.start_python_api()
            
            # 2. Wait for API to be ready
            if not self.wait_for_api():
                self.stop_all_services()
                return False
            
            # 3. Start real-time trading
            time.sleep(2)  # Give API a moment to fully initialize
            if not self.start_real_time_trading():
                self.log("SYSTEM", "⚠️  Continuing without real-time trading...")
            
            # 4. Start Angular dashboard
            self.start_angular_dashboard()
            
            # 5. Start .NET executor
            time.sleep(3)  # Give dashboard a moment to start
            self.start_dotnet_executor()
            
            # System is running
            print("=" * 60)
            self.log("SYSTEM", "🎉 All services started successfully!")
            self.log("SYSTEM", "")
            self.log("SYSTEM", "🌐 Access URLs:")
            self.log("SYSTEM", "• Dashboard: http://localhost:4200")
            self.log("SYSTEM", "• API: http://localhost:8000")
            self.log("SYSTEM", "• API Docs: http://localhost:8000/docs")
            self.log("SYSTEM", "• WebSocket: ws://localhost:8000/ws")
            self.log("SYSTEM", "")
            self.log("SYSTEM", "📊 Real-time features:")
            self.log("SYSTEM", "• Live trading decisions every 30 seconds")
            self.log("SYSTEM", "• WebSocket streaming to dashboard")
            self.log("SYSTEM", "• Automatic order execution via .NET")
            self.log("SYSTEM", "")
            self.log("SYSTEM", "⚠️  Press Ctrl+C to stop all services")
            print("=" * 60)
            
            # Keep running until interrupted
            while self.running:
                time.sleep(1)
                
                # Check if any process died
                for name, process in list(self.processes.items()):
                    if process.poll() is not None:
                        self.log(name.upper(), "❌ Process died unexpectedly!")
                        self.running = False
                        break
                        
        except KeyboardInterrupt:
            self.log("SYSTEM", "👋 Shutdown requested by user")
        except Exception as e:
            self.log("SYSTEM", f"❌ Unexpected error: {e}")
        finally:
            self.stop_all_services()
            self.log("SYSTEM", "🏁 All services stopped")
        
        return True

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print("\n")
    orchestrator.stop_all_services()
    sys.exit(0)

def main():
    global orchestrator
    orchestrator = ServiceOrchestrator()
    
    # Setup signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    print("🚀 Trading MVP - Real-Time Orchestrator")
    print("=" * 50)
    
    success = orchestrator.run_real_time_system()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()