# 🚀 Enterprise Deployment Guide

## 🏢 **Production Deployment Options**

### 📊 **Standalone Server Deployment**

#### **Option 1: Docker Deployment** (Recommended)
```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 9501

HEALTHCHECK CMD curl --fail http://localhost:9501/_stcore/health
CMD ["streamlit", "run", "main.py", "--server.port=9501", "--server.address=0.0.0.0"]
```

```bash
# Build and run
docker build -t skylus-analytics .
docker run -p 9501:9501 -v /path/to/logs:/app/logs skylus-analytics
```

#### **Option 2: Systemd Service** (Linux)
```ini
# /etc/systemd/system/skylus-analytics.service
[Unit]
Description=Skylus Analytics Platform
After=network.target

[Service]
Type=simple
User=skylus
WorkingDirectory=/opt/skylus-analytics
Environment=PATH=/opt/skylus-analytics/venv/bin
ExecStart=/opt/skylus-analytics/venv/bin/streamlit run main.py --server.port=9501 --server.address=0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl enable skylus-analytics
sudo systemctl start skylus-analytics
```

#### **Option 3: Windows Service**
```batch
# install_service.bat
sc create "Skylus Analytics" binPath= "C:\Python39\python.exe -m streamlit run C:\skylus-analytics\main.py --server.port=9501"
sc start "Skylus Analytics"
```

### 🌐 **Load Balanced Deployment**

#### **Nginx Reverse Proxy Configuration**
```nginx
upstream skylus_backend {
    server 127.0.0.1:9501;
    server 127.0.0.1:8502;
    server 127.0.0.1:8503;
}

server {
    listen 80;
    server_name analytics.company.com;
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name analytics.company.com;
    
    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;
    
    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains";
    
    location / {
        proxy_pass http://skylus_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support
        proxy_read_timeout 86400;
        proxy_send_timeout 86400;
    }
    
    # Static files caching
    location /static {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

#### **Apache Configuration**
```apache
<VirtualHost *:443>
    ServerName analytics.company.com
    
    SSLEngine on
    SSLCertificateFile /path/to/certificate.crt
    SSLCertificateKeyFile /path/to/private.key
    
    ProxyPreserveHost On
    ProxyRequests Off
    
    ProxyPass / http://localhost:9501/
    ProxyPassReverse / http://localhost:9501/
    
    # WebSocket support
    RewriteEngine on
    RewriteCond %{HTTP:Upgrade} websocket [NC]
    RewriteCond %{HTTP:Connection} upgrade [NC]
    RewriteRule ^/?(.*) "ws://localhost:9501/$1" [P,L]
</VirtualHost>
```

### ☁️ **Cloud Deployment**

#### **AWS EC2 with Auto Scaling**
```yaml
# cloudformation-template.yaml
AWSTemplateFormatVersion: '2010-09-09'
Resources:
  SkylAnalyticsLaunchTemplate:
    Type: AWS::EC2::LaunchTemplate
    Properties:
      LaunchTemplateName: skylus-analytics-template
      LaunchTemplateData:
        ImageId: ami-0abcdef1234567890  # Amazon Linux 2
        InstanceType: t3.large
        SecurityGroupIds:
          - !Ref SkylAnalyticsSecurityGroup
        UserData:
          Fn::Base64: !Sub |
            #!/bin/bash
            yum update -y
            yum install -y python3 python3-pip git
            git clone https://github.com/company/skylus-analytics.git /opt/skylus
            cd /opt/skylus
            pip3 install -r requirements.txt
            python3 setup.py
            systemctl enable skylus-analytics
            systemctl start skylus-analytics
```

#### **Google Cloud Platform**
```yaml
# app.yaml for App Engine
runtime: python39

env_variables:
  SKYLUS_PORT: 8080
  SKYLUS_HOST: 0.0.0.0

automatic_scaling:
  min_instances: 1
  max_instances: 10
  target_cpu_utilization: 0.6

handlers:
- url: /static
  static_dir: static
  
- url: /.*
  script: auto
```

#### **Microsoft Azure**
```json
{
  "name": "skylus-analytics",
  "type": "Microsoft.Web/sites",
  "properties": {
    "siteConfig": {
      "pythonVersion": "3.9",
      "appSettings": [
        {
          "name": "SKYLUS_PORT",
          "value": "8000"
        }
      ]
    }
  }
}
```

## 🔒 **Security Configuration**

### **Authentication Setup**
```python
# auth_config.py
import streamlit_authenticator as stauth

# User credentials (use secure storage in production)
credentials = {
    'usernames': {
        'admin': {
            'email': 'admin@company.com',
            'name': 'Administrator',
            'password': '$2b$12$...'  # bcrypt hash
        },
        'analyst': {
            'email': 'analyst@company.com', 
            'name': 'Security Analyst',
            'password': '$2b$12$...'
        }
    }
}

# Add to main.py
authenticator = stauth.Authenticate(
    credentials,
    'skylus_analytics',
    'secure_key_123',
    cookie_expiry_days=30
)

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status == True:
    # Load dashboard
    create_dashboard()
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
```

### **SSL/TLS Configuration**
```bash
# Generate self-signed certificate (development)
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes

# Production: Use Let's Encrypt
certbot --nginx -d analytics.company.com
```

### **Firewall Rules**
```bash
# Ubuntu/Debian
ufw allow ssh
ufw allow 443/tcp
ufw allow 80/tcp
ufw enable

# CentOS/RHEL
firewall-cmd --permanent --add-service=ssh
firewall-cmd --permanent --add-service=http
firewall-cmd --permanent --add-service=https
firewall-cmd --reload
```

## 📊 **Performance Optimization**

### **Hardware Recommendations**

#### **Small Deployment** (< 1GB logs/day)
- **CPU**: 2 cores, 2.5GHz+
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 100GB SSD
- **Network**: 100Mbps

#### **Medium Deployment** (1-10GB logs/day)
- **CPU**: 4 cores, 3.0GHz+
- **RAM**: 16GB minimum, 32GB recommended
- **Storage**: 500GB SSD with backup
- **Network**: 1Gbps

#### **Large Deployment** (10GB+ logs/day)
- **CPU**: 8+ cores, 3.5GHz+
- **RAM**: 64GB minimum, 128GB recommended
- **Storage**: 2TB+ NVMe SSD with RAID
- **Network**: 10Gbps with redundancy

### **Database Integration**
```python
# For large-scale deployments, integrate with databases
import postgresql
import elasticsearch

# PostgreSQL configuration
DB_CONFIG = {
    'host': 'localhost',
    'database': 'skylus_analytics',
    'user': 'skylus_user',
    'password': 'secure_password'
}

# Elasticsearch for log indexing
ES_CONFIG = {
    'hosts': ['elasticsearch-1:9200', 'elasticsearch-2:9200'],
    'index': 'skylus-logs',
    'doc_type': 'log_entry'
}
```

### **Caching Strategy**
```python
# Redis caching for improved performance
import redis
import pickle

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def cache_analytics_data(key, data, expiry=3600):
    """Cache analytics data with expiry"""
    redis_client.setex(key, expiry, pickle.dumps(data))

def get_cached_data(key):
    """Retrieve cached analytics data"""
    cached = redis_client.get(key)
    return pickle.loads(cached) if cached else None
```

## 📈 **Monitoring & Maintenance**

### **Health Monitoring**
```python
# health_check.py
import requests
import smtplib
from datetime import datetime

def check_service_health():
    """Monitor service health and send alerts"""
    try:
        response = requests.get('http://localhost:9501/_stcore/health', timeout=10)
        if response.status_code == 200:
            return True
    except Exception as e:
        send_alert(f"Skylus Analytics service down: {e}")
        return False

def send_alert(message):
    """Send email alerts"""
    # Configure SMTP and send notification
    pass

# Run as cron job every 5 minutes
# */5 * * * * /usr/bin/python3 /opt/skylus/health_check.py
```

### **Log Rotation**
```bash
# /etc/logrotate.d/skylus-analytics
/opt/skylus-analytics/logs/*.log {
    daily
    missingok
    rotate 52
    compress
    notifempty
    create 644 skylus skylus
    postrotate
        systemctl reload skylus-analytics
    endscript
}
```

### **Backup Strategy**
```bash
#!/bin/bash
# backup_skylus.sh

BACKUP_DIR="/backup/skylus-analytics"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p "$BACKUP_DIR/$DATE"

# Backup configuration
cp -r /opt/skylus-analytics/config "$BACKUP_DIR/$DATE/"

# Backup recent logs (last 7 days)
find /opt/skylus-analytics/logs -name "*.log" -mtime -7 -exec cp {} "$BACKUP_DIR/$DATE/" \;

# Backup reports and exports
cp -r /opt/skylus-analytics/exports "$BACKUP_DIR/$DATE/"
cp -r /opt/skylus-analytics/reports "$BACKUP_DIR/$DATE/"

# Compress backup
tar -czf "$BACKUP_DIR/skylus_backup_$DATE.tar.gz" -C "$BACKUP_DIR" "$DATE"
rm -rf "$BACKUP_DIR/$DATE"

# Keep only last 30 days of backups
find "$BACKUP_DIR" -name "skylus_backup_*.tar.gz" -mtime +30 -delete

echo "Backup completed: skylus_backup_$DATE.tar.gz"
```

## 🔧 **Troubleshooting Production Issues**

### **Performance Issues**
```bash
# Monitor resource usage
htop
iotop
iftop

# Check memory usage
free -h
cat /proc/meminfo

# Monitor disk I/O
iostat -x 1

# Check network connections
netstat -tulpn | grep :9501
```

### **Log Analysis for Issues**
```bash
# Check Streamlit logs
journalctl -u skylus-analytics -f

# Monitor error rates
tail -f /var/log/skylus/error.log | grep ERROR

# Performance metrics
tail -f /var/log/skylus/performance.log
```

### **Database Maintenance**
```sql
-- PostgreSQL maintenance
VACUUM ANALYZE log_entries;
REINDEX INDEX log_entries_timestamp_idx;

-- Check database size
SELECT pg_size_pretty(pg_database_size('skylus_analytics'));
```

## 📋 **Deployment Checklist**

### **Pre-Deployment**
- [ ] Hardware requirements verified
- [ ] Network security configured
- [ ] SSL certificates installed
- [ ] Database setup completed
- [ ] Backup strategy implemented
- [ ] Monitoring tools configured

### **Deployment**
- [ ] Application deployed and configured
- [ ] Service startup scripts created
- [ ] Load balancer configured
- [ ] Health checks implemented
- [ ] Performance testing completed
- [ ] Security testing passed

### **Post-Deployment**
- [ ] User training completed
- [ ] Documentation updated
- [ ] Monitoring alerts configured
- [ ] Backup procedures tested
- [ ] Disaster recovery plan created
- [ ] Performance baseline established

## 🎯 **Best Practices**

### **Security**
- Use strong authentication and authorization
- Implement proper network segmentation
- Regular security updates and patches
- Encrypt data in transit and at rest
- Monitor access logs and suspicious activities

### **Performance**
- Implement proper caching strategies
- Use CDN for static assets
- Optimize database queries
- Monitor and tune resource usage
- Implement proper log rotation

### **Reliability**
- Setup redundancy and failover
- Implement proper backup and recovery
- Monitor service health continuously
- Use infrastructure as code
- Test disaster recovery procedures

---

**🚀 Ready for Enterprise Deployment!**

*For additional support, contact your system administrator or refer to the comprehensive documentation.*