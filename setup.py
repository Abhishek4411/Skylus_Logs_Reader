#!/usr/bin/env python3
"""
Skylus Analytics Platform - Enterprise Setup Script
Automated installation and configuration for professional deployment
"""

import os
import sys
import subprocess
import platform
import json
from pathlib import Path

class SkylAnalyticsSetup:
    def __init__(self):
        self.platform = platform.system()
        self.python_version = sys.version_info
        self.base_dir = Path.cwd()
        self.config = {
            "server": {
                "port": 9501,
                "host": "localhost",
                "max_upload_size": 200,
                "theme": "dark_pro"
            },
            "analytics": {
                "max_records_display": 5000,
                "enable_3d_graphics": True,
                "animation_speed": 1.0,
                "auto_refresh": False,
                "cache_enabled": True
            },
            "security": {
                "enable_auth": False,
                "allowed_ips": ["127.0.0.1", "localhost"],
                "max_file_size_mb": 500
            },
            "performance": {
                "memory_limit_gb": 4,
                "parallel_processing": True,
                "compression_enabled": True
            }
        }
    
    def print_banner(self):
        """Display professional setup banner"""
        banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                     🚀 SKYLUS ANALYTICS PLATFORM                            ║
║                        Enterprise Setup & Configuration                     ║
║                                                                              ║
║  Professional-Grade Log Intelligence • Advanced 3D Visualizations           ║
║  Real-time Analytics • AI-Powered Insights • Security Monitoring            ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """
        print(banner)
        print(f"🔧 System: {self.platform}")
        print(f"🐍 Python: {self.python_version.major}.{self.python_version.minor}.{self.python_version.micro}")
        print(f"📁 Directory: {self.base_dir}")
        print("="*80)
    
    def check_requirements(self):
        """Check system requirements"""
        print("📋 Checking System Requirements...")
        
        # Python version check
        if self.python_version < (3, 8):
            print("❌ Python 3.8+ required. Current version:", sys.version)
            return False
        print("✅ Python version compatible")
        
        # Memory check
        try:
            import psutil
            memory_gb = psutil.virtual_memory().total / (1024**3)
            if memory_gb < 2:
                print(f"⚠️  Low memory detected: {memory_gb:.1f}GB (Recommended: 4GB+)")
            else:
                print(f"✅ Memory: {memory_gb:.1f}GB")
        except ImportError:
            print("ℹ️  Memory check skipped (psutil not available)")
        
        # Disk space check
        disk_space = os.statvfs('.').f_bavail * os.statvfs('.').f_frsize / (1024**3)
        if disk_space < 1:
            print(f"⚠️  Low disk space: {disk_space:.1f}GB")
        else:
            print(f"✅ Disk space: {disk_space:.1f}GB")
        
        return True
    
    def install_dependencies(self):
        """Install required Python packages"""
        print("\n📦 Installing Dependencies...")
        
        requirements = [
            "streamlit>=1.28.0",
            "pandas>=1.5.0", 
            "plotly>=5.15.0",
            "numpy>=1.24.0",
            "python-dateutil>=2.8.0",
            "kaleido>=0.2.1",
            "psutil>=5.9.0"
        ]
        
        for package in requirements:
            try:
                print(f"📥 Installing {package}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--quiet"])
                print(f"✅ {package} installed successfully")
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to install {package}: {e}")
                return False
        
        print("✅ All dependencies installed successfully!")
        return True
    
    def create_directory_structure(self):
        """Create professional directory structure"""
        print("\n📁 Creating Directory Structure...")
        
        directories = [
            "logs",
            "exports", 
            "cache",
            "config",
            "backups",
            "reports",
            "templates"
        ]
        
        for directory in directories:
            dir_path = self.base_dir / directory
            dir_path.mkdir(exist_ok=True)
            print(f"📂 Created: {directory}/")
        
        # Create sample log structure
        log_subdirs = ["auth", "storage", "network", "compute"]
        for subdir in log_subdirs:
            (self.base_dir / "logs" / subdir).mkdir(exist_ok=True)
            print(f"📂 Created: logs/{subdir}/")
        
        print("✅ Directory structure created!")
    
    def create_configuration_files(self):
        """Create configuration files"""
        print("\n⚙️ Creating Configuration Files...")
        
        # Main configuration
        config_file = self.base_dir / "config" / "settings.json"
        with open(config_file, 'w') as f:
            json.dump(self.config, f, indent=4)
        print(f"✅ Created: {config_file}")
        
        # Environment configuration
        env_file = self.base_dir / ".env"
        env_content = f"""# Skylus Analytics Platform Environment Configuration
SKYLUS_PORT={self.config['server']['port']}
SKYLUS_HOST={self.config['server']['host']}
SKYLUS_MAX_UPLOAD_SIZE={self.config['server']['max_upload_size']}
SKYLUS_THEME={self.config['server']['theme']}
SKYLUS_CACHE_ENABLED={str(self.config['analytics']['cache_enabled']).lower()}
SKYLUS_3D_GRAPHICS={str(self.config['analytics']['enable_3d_graphics']).lower()}
"""
        with open(env_file, 'w') as f:
            f.write(env_content)
        print(f"✅ Created: {env_file}")
        
        # Streamlit configuration
        streamlit_dir = self.base_dir / ".streamlit"
        streamlit_dir.mkdir(exist_ok=True)
        
        streamlit_config = streamlit_dir / "config.toml"
        streamlit_content = f"""[server]
port = {self.config['server']['port']}
headless = true
enableCORS = false
enableXsrfProtection = false
maxUploadSize = {self.config['server']['max_upload_size']}

[browser]
gatherUsageStats = false
showErrorDetails = false

[theme]
base = "dark"
primaryColor = "#4ecdc4"
backgroundColor = "#0c0c0c"
secondaryBackgroundColor = "#1a1a2e"
textColor = "#ffffff"

[logger]
level = "warning"
"""
        with open(streamlit_config, 'w') as f:
            f.write(streamlit_content)
        print(f"✅ Created: {streamlit_config}")
    
    def create_launch_scripts(self):
        """Create platform-specific launch scripts"""
        print("\n🚀 Creating Launch Scripts...")
        
        if self.platform == "Windows":
            # Windows batch script
            batch_content = f"""@echo off
title Skylus Analytics Platform
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║           🚀 SKYLUS ANALYTICS PLATFORM                      ║
echo ║              Starting Enterprise Dashboard...               ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo 🌐 Starting server on http://localhost:{self.config['server']['port']}
echo 📊 Loading professional interface...
echo ⚡ Initializing analytics engine...
echo.
python -m streamlit run main.py --server.port {self.config['server']['port']} --server.headless true
pause
"""
            with open("start_skylus.bat", 'w') as f:
                f.write(batch_content)
            print("✅ Created: start_skylus.bat")
        
        # Universal shell script
        shell_content = f"""#!/bin/bash
echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║           🚀 SKYLUS ANALYTICS PLATFORM                      ║"
echo "║              Starting Enterprise Dashboard...               ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "🌐 Starting server on http://localhost:{self.config['server']['port']}"
echo "📊 Loading professional interface..."
echo "⚡ Initializing analytics engine..."
echo ""

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "🔧 Activating virtual environment..."
    source venv/bin/activate
fi

# Start Skylus Analytics Platform
python -m streamlit run main.py --server.port {self.config['server']['port']} --server.headless true

echo ""
echo "👋 Skylus Analytics Platform stopped."
"""
        with open("start_skylus.sh", 'w') as f:
            f.write(shell_content)
        
        # Make shell script executable
        if self.platform != "Windows":
            os.chmod("start_skylus.sh", 0o755)
        print("✅ Created: start_skylus.sh")
    
    def create_sample_data(self):
        """Create sample log data for testing"""
        print("\n📄 Creating Sample Data...")
        
        sample_logs = [
            "2025-07-18 10:00:00,123|INFO|abc123|AUTH|testuser|tenant123|192.168.1.1|Mozilla/5.0 (Windows NT 10.0; Win64; x64)|LOGIN|LOGIN succeeded",
            "2025-07-18 10:01:00,456|INFO|def456|STORAGE|testuser|tenant123|192.168.1.1|Mozilla/5.0 (Windows NT 10.0; Win64; x64)|UPLOAD_FILE|UPLOAD_FILE succeeded",
            "2025-07-18 10:02:00,789|ERROR|ghi789|COMPUTE|testuser|tenant123|192.168.1.1|Mozilla/5.0 (Windows NT 10.0; Win64; x64)|CREATE_VM|Quota exceeded for cores",
            "2025-07-18 10:03:00,012|INFO|jkl012|NETWORK|admin|tenant456|192.168.1.2|Mozilla/5.0 (X11; Linux x86_64)|LIST_NETWORK|LIST_NETWORK succeeded"
        ]
        
        sample_file = self.base_dir / "logs" / "sample_demo.log"
        with open(sample_file, 'w') as f:
            for log in sample_logs:
                f.write(log + '\n')
        
        print(f"✅ Created: {sample_file}")
        print("ℹ️  Sample data ready for testing the platform")
    
    def create_documentation(self):
        """Create additional documentation"""
        print("\n📚 Creating Documentation...")
        
        # Quick start guide
        quickstart = self.base_dir / "QUICKSTART.md"
        quickstart_content = """# 🚀 Skylus Analytics - Quick Start

## Instant Launch
```bash
# Windows
start_skylus.bat

# Linux/Mac
./start_skylus.sh
```

## Access Dashboard
- Open: http://localhost:9501
- Upload logs or connect to ./logs folder
- Start analyzing immediately!

## Sample Data
- Use `logs/sample_demo.log` for testing
- Professional interface loads automatically
- Explore all 7 dashboard tabs

## Support
- Check README.md for comprehensive guide
- Configuration in config/settings.json
- Logs stored in logs/ directory
"""
        with open(quickstart, 'w') as f:
            f.write(quickstart_content)
        print(f"✅ Created: {quickstart}")
        
        # Troubleshooting guide
        troubleshooting = self.base_dir / "TROUBLESHOOTING.md"
        troubleshooting_content = """# 🔧 Troubleshooting Guide

## Common Issues

### Port Already in Use
```bash
# Change port in config/settings.json
# Or use different port:
streamlit run main.py --server.port 8502
```

### Memory Issues
- Reduce max_records_display in config
- Disable 3D graphics for large datasets
- Use data filtering before analysis

### File Access Issues
- Check file permissions
- Ensure logs directory exists
- Verify log file format

### Browser Issues
- Clear browser cache
- Try different browser
- Check JavaScript is enabled

## Performance Optimization
- Enable caching in settings
- Use SSD for log storage
- Increase memory limit if available
"""
        with open(troubleshooting, 'w') as f:
            f.write(troubleshooting_content)
        print(f"✅ Created: {troubleshooting}")
    
    def run_setup(self):
        """Run complete setup process"""
        self.print_banner()
        
        try:
            # Setup steps
            if not self.check_requirements():
                print("❌ Setup failed: Requirements not met")
                return False
            
            if not self.install_dependencies():
                print("❌ Setup failed: Dependency installation failed")
                return False
            
            self.create_directory_structure()
            self.create_configuration_files()
            self.create_launch_scripts()
            self.create_sample_data()
            self.create_documentation()
            
            # Success message
            print("\n" + "="*80)
            print("🎉 SKYLUS ANALYTICS PLATFORM SETUP COMPLETE!")
            print("="*80)
            print("🚀 Ready to launch:")
            print(f"   • Windows: start_skylus.bat")
            print(f"   • Linux/Mac: ./start_skylus.sh")
            print(f"   • Manual: streamlit run main.py")
            print(f"🌐 Access: http://localhost:{self.config['server']['port']}")
            print("📁 Sample data: logs/sample_demo.log")
            print("⚙️ Configuration: config/settings.json")
            print("📚 Quick start: QUICKSTART.md")
            print("🔧 Troubleshooting: TROUBLESHOOTING.md")
            print("\n🎯 Professional log analytics is ready!")
            
            return True
            
        except Exception as e:
            print(f"❌ Setup failed: {e}")
            return False

if __name__ == "__main__":
    setup = SkylAnalyticsSetup()
    success = setup.run_setup()
    
    if success:
        print("\n🚀 Launch the platform now? (y/n): ", end="")
        if input().lower().startswith('y'):
            os.system("python -m streamlit run main.py" if os.path.exists("main.py") else "echo main.py not found")
    else:
        sys.exit(1)