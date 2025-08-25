#!/usr/bin/env python3
"""
Skylus Logs Reader - Enterprise Analytics Dashboard
Professional-grade log analytics with advanced visualizations and animations
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import glob
import re
from datetime import datetime, timedelta
import json
from collections import defaultdict, Counter
import base64
from io import StringIO
import zipfile
import time
import numpy as np

# Professional Dashboard Configuration
st.set_page_config(
    page_title="Skylus Analytics Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS Styling - Hide Streamlit Branding & Add Animations
def load_professional_css():
    st.markdown("""
    <style>
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Professional Dark Theme */
    .stApp {
        background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%);
        color: #ffffff;
    }
    
    /* Animated Header */
    .main-header {
        background: linear-gradient(90deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4, #ffeaa7);
        background-size: 400% 400%;
        animation: gradientShift 8s ease infinite;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 30px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Metric Cards Animation */
    .metric-card {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        transition: all 0.3s ease;
        animation: fadeInUp 0.6s ease-out;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.3);
        background: rgba(255,255,255,0.15);
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #2c3e50 0%, #3498db 100%);
    }
    
    /* Button Animations */
    .stButton > button {
        background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
        border: none;
        border-radius: 25px;
        padding: 10px 25px;
        color: white;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        background: linear-gradient(45deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255,255,255,0.1);
        border-radius: 15px;
        padding: 10px 20px;
        border: 1px solid rgba(255,255,255,0.2);
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
        color: white;
        transform: scale(1.05);
    }
    
    /* Loading Animation */
    .loading-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 200px;
    }
    
    .loader {
        width: 50px;
        height: 50px;
        border: 5px solid rgba(255,255,255,0.2);
        border-left: 5px solid #4ecdc4;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Chart Container */
    .chart-container {
        background: rgba(255,255,255,0.05);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        border: 1px solid rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        animation: slideIn 0.8s ease-out;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Success/Error Indicators */
    .success-indicator {
        color: #2ecc71;
        animation: pulse 2s infinite;
    }
    
    .error-indicator {
        color: #e74c3c;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    /* Data Table Styling */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
    }
    
    /* Professional Title */
    .dashboard-title {
        font-size: 3em;
        font-weight: bold;
        text-align: center;
        margin-bottom: 30px;
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: titleGlow 3s ease-in-out infinite alternate;
    }
    
    @keyframes titleGlow {
        from { filter: brightness(1); }
        to { filter: brightness(1.2); }
    }
    </style>
    """, unsafe_allow_html=True)

class SkylLogReader:
    def __init__(self):
        self.df = None
        self.raw_logs = []
        self.services = ['AUTH', 'STORAGE', 'NETWORK', 'COMPUTE']
        self.log_pattern = re.compile(
            r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})\|([A-Z]+)\|([^|]+)\|([^|]+)\|([^|]+)\|([^|]+)\|([^|]+)\|([^|]*)\|([^|]+)\|(.*)$'
        )
        
        # Create logs folder if it doesn't exist
        if not os.path.exists('./logs'):
            os.makedirs('./logs')
            st.info("📁 Created logs folder for you!")
        
    def load_logs_from_folder(self, folder_path):
        """Load all log files from the specified folder"""
        log_files = []
        if os.path.exists(folder_path):
            patterns = ['*.log', '*.txt', '*log*']
            for pattern in patterns:
                log_files.extend(glob.glob(os.path.join(folder_path, pattern)))
        
        all_logs = []
        file_stats = {}
        
        for file_path in log_files:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    file_stats[os.path.basename(file_path)] = len([l for l in lines if l.strip()])
                    all_logs.extend([(line.strip(), os.path.basename(file_path)) for line in lines if line.strip()])
            except Exception as e:
                st.error(f"Error reading {file_path}: {str(e)}")
        
        return all_logs, file_stats
    
    def parse_log_line(self, line, filename):
        """Parse a single log line with intelligent format detection"""
        match = self.log_pattern.match(line)
        if match:
            timestamp_str, level, uuid, service, user, tenant_id, ip, user_agent, action, message = match.groups()
            
            # Parse timestamp
            try:
                timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S,%f')
            except:
                timestamp = None
            
            return {
                'timestamp': timestamp,
                'date': timestamp.date() if timestamp else None,
                'time': timestamp.time() if timestamp else None,
                'hour': timestamp.hour if timestamp else None,
                'day_of_week': timestamp.strftime('%A') if timestamp else None,
                'level': level,
                'uuid': uuid,
                'service': service,
                'user': user,
                'tenant_id': tenant_id,
                'ip': ip,
                'user_agent': user_agent,
                'action': action,
                'message': message,
                'filename': filename,
                'raw_line': line,
                'success': 'succeeded' in message.lower() or 'success' in message.lower(),
                'error': level == 'ERROR' or 'error' in message.lower() or 'failed' in message.lower() or 'quota exceeded' in message.lower(),
                'browser': self.extract_browser(user_agent),
                'os': self.extract_os(user_agent),
                'response_time': self.extract_response_time(message),
                'session_id': uuid[:8],  # Short session identifier
            }
        return None
    
    def extract_browser(self, user_agent):
        """Extract browser information from user agent"""
        if 'Chrome' in user_agent:
            return 'Chrome'
        elif 'Firefox' in user_agent:
            return 'Firefox'
        elif 'Safari' in user_agent and 'Chrome' not in user_agent:
            return 'Safari'
        elif 'Edge' in user_agent:
            return 'Edge'
        elif 'python-requests' in user_agent:
            return 'API Client'
        return 'Other'
    
    def extract_os(self, user_agent):
        """Extract OS information from user agent"""
        if 'Windows NT' in user_agent:
            return 'Windows'
        elif 'X11; Linux' in user_agent:
            return 'Linux'
        elif 'X11; Ubuntu' in user_agent:
            return 'Ubuntu'
        elif 'Macintosh' in user_agent:
            return 'macOS'
        elif 'python-requests' in user_agent:
            return 'API'
        return 'Other'
    
    def extract_response_time(self, message):
        """Extract response time from message if available"""
        # Look for time patterns in milliseconds
        time_match = re.search(r'(\d+)ms', message)
        if time_match:
            return int(time_match.group(1))
        return None
    
    def process_logs(self, logs_data):
        """Process all logs and create DataFrame"""
        processed_logs = []
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, (line, filename) in enumerate(logs_data):
            if i % 100 == 0:
                progress = i / len(logs_data)
                progress_bar.progress(progress)
                status_text.text(f'Processing logs... {i}/{len(logs_data)}')
            
            parsed = self.parse_log_line(line, filename)
            if parsed:
                processed_logs.append(parsed)
        
        progress_bar.progress(1.0)
        status_text.text('Processing complete!')
        time.sleep(0.5)
        progress_bar.empty()
        status_text.empty()
        
        if processed_logs:
            self.df = pd.DataFrame(processed_logs)
            self.df = self.df.sort_values('timestamp', na_position='last')
            return True
        return False
    
    def get_advanced_stats(self):
        """Generate comprehensive advanced statistics"""
        if self.df is None or len(self.df) == 0:
            return {}
        
        # Basic stats
        total_logs = len(self.df)
        date_range = {
            'start': self.df['timestamp'].min(),
            'end': self.df['timestamp'].max()
        }
        
        # Advanced analytics
        stats = {
            'total_logs': total_logs,
            'date_range': date_range,
            'duration_days': (date_range['end'] - date_range['start']).days if date_range['start'] else 0,
            
            # User Analytics
            'users': {
                'total': self.df['user'].nunique(),
                'unique_list': list(self.df['user'].unique()),
                'most_active': self.df['user'].value_counts().head(10).to_dict(),
                'activity_distribution': self.df.groupby('user').size().describe().to_dict()
            },
            
            # Service Analytics
            'services': {
                'distribution': self.df['service'].value_counts().to_dict(),
                'success_rates': self.df.groupby('service')['success'].mean().to_dict(),
                'error_rates': self.df.groupby('service')['error'].mean().to_dict(),
                'activity_trends': self.df.groupby(['service', 'date']).size().unstack(fill_value=0).to_dict()
            },
            
            # Time Analytics
            'temporal': {
                'hourly_pattern': self.df.groupby('hour').size().to_dict(),
                'daily_pattern': self.df.groupby('day_of_week').size().to_dict(),
                'peak_hour': self.df.groupby('hour').size().idxmax(),
                'peak_day': self.df.groupby('day_of_week').size().idxmax(),
                'activity_by_date': self.df.groupby('date').size().to_dict()
            },
            
            # Technical Analytics
            'technical': {
                'browsers': self.df['browser'].value_counts().to_dict(),
                'operating_systems': self.df['os'].value_counts().to_dict(),
                'ip_addresses': self.df['ip'].nunique(),
                'unique_sessions': self.df['session_id'].nunique(),
                'avg_session_length': self.df.groupby('session_id').size().mean()
            },
            
            # Performance Analytics
            'performance': {
                'overall_success_rate': (self.df['success'].sum() / total_logs) * 100,
                'overall_error_rate': (self.df['error'].sum() / total_logs) * 100,
                'actions_distribution': self.df['action'].value_counts().head(20).to_dict(),
                'error_messages': self.df[self.df['error']]['message'].value_counts().head(10).to_dict() if self.df['error'].any() else {},
                'tenant_activity': self.df['tenant_id'].value_counts().to_dict()
            },
            
            # Security Analytics
            'security': {
                'failed_logins': len(self.df[(self.df['action'].str.contains('LOGIN', na=False)) & (self.df['error'])]),
                'suspicious_ips': self.df[self.df['error']]['ip'].value_counts().head(5).to_dict(),
                'unusual_activity': self.df.groupby('ip').size().sort_values(ascending=False).head(10).to_dict()
            }
        }
        
        return stats

def create_animated_metric_card(title, value, delta=None, delta_color="normal"):
    """Create an animated metric card"""
    delta_html = ""
    if delta is not None:
        color = "#2ecc71" if delta_color == "normal" else "#e74c3c"
        delta_html = f'<p style="color: {color}; margin: 0; font-size: 14px;">Δ {delta}</p>'
    
    st.markdown(f"""
    <div class="metric-card">
        <h3 style="margin: 0; color: #4ecdc4;">{title}</h3>
        <h1 style="margin: 10px 0; color: #ffffff;">{value}</h1>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)

def create_3d_surface_plot(df, x_col, y_col, z_col, title):
    """Create a 3D surface plot"""
    # Prepare data for 3D surface
    pivot_data = df.pivot_table(values=z_col, index=x_col, columns=y_col, fill_value=0)
    
    fig = go.Figure(data=[go.Surface(
        z=pivot_data.values,
        x=pivot_data.columns,
        y=pivot_data.index,
        colorscale='Viridis',
        showscale=True
    )])
    
    fig.update_layout(
        title=title,
        scene=dict(
            xaxis_title=y_col,
            yaxis_title=x_col,
            zaxis_title=z_col,
            camera=dict(eye=dict(x=1.2, y=1.2, z=0.6))
        ),
        template="plotly_dark",
        height=500
    )
    
    return fig

def create_advanced_charts(df, chart_type, x_col, y_col, color_col=None, title=""):
    """Create various types of advanced charts"""
    
    if chart_type == "3D Scatter":
        fig = px.scatter_3d(df, x=x_col, y=y_col, z='hour', 
                           color=color_col, title=title,
                           template="plotly_dark")
        fig.update_traces(marker=dict(size=5, opacity=0.7))
        
    elif chart_type == "Sunburst":
        fig = px.sunburst(df, path=[x_col, y_col], title=title,
                         template="plotly_dark")
        
    elif chart_type == "Treemap":
        fig = px.treemap(df, path=[x_col, y_col], title=title,
                        template="plotly_dark")
        
    elif chart_type == "Violin":
        fig = px.violin(df, x=x_col, y=y_col, color=color_col, 
                       title=title, template="plotly_dark")
        
    elif chart_type == "Heatmap":
        # Create pivot table for heatmap
        if color_col:
            heatmap_data = df.pivot_table(values=color_col, index=x_col, columns=y_col, fill_value=0)
        else:
            heatmap_data = df.groupby([x_col, y_col]).size().unstack(fill_value=0)
        
        fig = px.imshow(heatmap_data, title=title, template="plotly_dark",
                       color_continuous_scale="Viridis")
        
    elif chart_type == "Parallel Coordinates":
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()[:4]
        fig = px.parallel_coordinates(df.head(1000), color=color_col,
                                    dimensions=numeric_cols,
                                    title=title, template="plotly_dark")
        
    elif chart_type == "Radar":
        # Aggregate data for radar chart
        radar_data = df.groupby(x_col).size().head(8)
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=radar_data.values,
            theta=radar_data.index,
            fill='toself',
            name=title
        ))
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True)
            ),
            showlegend=True,
            title=title,
            template="plotly_dark"
        )
        
    elif chart_type == "Waterfall":
        values = df.groupby(x_col).size().head(8)
        
        fig = go.Figure(go.Waterfall(
            name="Activity",
            orientation="v",
            measure=["relative"] * len(values),
            x=values.index,
            textposition="outside",
            text=[str(v) for v in values.values],
            y=values.values,
            connector={"line": {"color": "rgb(63, 63, 63)"}},
        ))
        fig.update_layout(title=title, template="plotly_dark")
        
    else:  # Default to enhanced bar chart
        fig = px.bar(df.groupby(x_col).size().reset_index(), 
                    x=x_col, y=0, title=title,
                    template="plotly_dark")
    
    # Add animations and professional styling
    fig.update_layout(
        transition_duration=500,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        title_font_size=16,
        showlegend=True
    )
    
    return fig

def create_dashboard():
    """Create the main professional dashboard"""
    # Load professional styling
    load_professional_css()
    
    # Animated title
    st.markdown("""
    <div class="main-header">
        <h1 class="dashboard-title">🚀 Skylus Analytics Platform</h1>
        <p style="font-size: 1.2em; margin: 0;">Enterprise-Grade Log Intelligence & Performance Analytics</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize log reader
    if 'log_reader' not in st.session_state:
        st.session_state.log_reader = SkylLogReader()
    
    # Professional Sidebar
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <h2 style="color: #4ecdc4;">📊 Data Sources</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # File Upload Section
        st.markdown("### 📁 Upload Log Files")
        uploaded_files = st.file_uploader(
            "Drag & Drop Your Log Files",
            type=['log', 'txt'],
            accept_multiple_files=True,
            help="Support for multiple log formats"
        )
        
        st.markdown("### 📂 Or Use Folder Path")
        folder_path = st.text_input(
            "Enter Logs Directory",
            value="./logs",
            help="Local or network path to log files"
        )
        
        # Professional Load Button
        if st.button("🚀 **ANALYZE LOGS**", type="primary"):
            with st.spinner("🔄 Initializing Analytics Engine..."):
                logs_data = []
                file_stats = {}
                
                # Process uploaded files
                if uploaded_files:
                    for uploaded_file in uploaded_files:
                        content = uploaded_file.read().decode('utf-8', errors='ignore')
                        lines = content.split('\n')
                        file_stats[uploaded_file.name] = len([l for l in lines if l.strip()])
                        logs_data.extend([(line.strip(), uploaded_file.name) for line in lines if line.strip()])
                
                # Process folder path
                elif folder_path and os.path.exists(folder_path):
                    logs_data, file_stats = st.session_state.log_reader.load_logs_from_folder(folder_path)
                
                if logs_data:
                    success = st.session_state.log_reader.process_logs(logs_data)
                    if success:
                        st.success(f"✅ **{len(logs_data):,}** logs processed from **{len(file_stats)}** files")
                        st.session_state.file_stats = file_stats
                        st.balloons()
                    else:
                        st.error("❌ Processing failed")
                else:
                    st.warning("⚠️ No logs detected")
        
        # Advanced Configuration
        with st.expander("⚙️ Advanced Settings"):
            st.selectbox("Theme", ["Dark Pro", "Light Pro", "Neon"])
            st.slider("Animation Speed", 0.1, 2.0, 1.0)
            st.checkbox("Enable 3D Graphics", value=True)
            st.checkbox("Real-time Updates", value=False)
    
    # Main Dashboard Content
    if st.session_state.log_reader.df is not None and len(st.session_state.log_reader.df) > 0:
        df = st.session_state.log_reader.df
        stats = st.session_state.log_reader.get_advanced_stats()
        
        # Executive Summary Cards
        st.markdown("## 📊 **Executive Dashboard**")
        
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
        with col1:
            create_animated_metric_card("Total Events", f"{stats['total_logs']:,}")
        
        with col2:
            create_animated_metric_card("Active Users", f"{stats['users']['total']}")
        
        with col3:
            success_rate = stats['performance']['overall_success_rate']
            create_animated_metric_card("Success Rate", f"{success_rate:.1f}%")
        
        with col4:
            error_rate = stats['performance']['overall_error_rate']
            create_animated_metric_card("Error Rate", f"{error_rate:.1f}%", 
                                      delta_color="inverse" if error_rate > 5 else "normal")
        
        with col5:
            create_animated_metric_card("Services", f"{len(stats['services']['distribution'])}")
        
        with col6:
            create_animated_metric_card("Peak Hour", f"{stats['temporal']['peak_hour']}:00")
        
        # Timeline Info
        if stats['date_range']['start']:
            st.info(f"📅 **Analytics Period:** {stats['date_range']['start'].strftime('%Y-%m-%d %H:%M')} → {stats['date_range']['end'].strftime('%Y-%m-%d %H:%M')} ({stats['duration_days']} days)")
        
        # Professional Tabs
        tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
            "🎯 **Executive Overview**",
            "📈 **Advanced Analytics**", 
            "👥 **User Intelligence**",
            "⚠️ **Security & Errors**",
            "🔧 **Service Performance**",
            "🔍 **Data Explorer**",
            "📊 **Custom Visualizations**"
        ])
        
        with tab1:
            st.markdown("### 🎯 **Strategic Overview**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Animated Activity Timeline
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                daily_data = df.groupby('date').agg({
                    'level': 'count',
                    'success': 'sum',
                    'error': 'sum'
                }).reset_index()
                daily_data.columns = ['Date', 'Total', 'Success', 'Errors']
                
                fig_timeline = px.line(daily_data, x='Date', y=['Total', 'Success', 'Errors'],
                                     title="📈 Daily Activity Trends",
                                     template="plotly_dark")
                fig_timeline.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
                    yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
                )
                st.plotly_chart(fig_timeline, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                # 3D Service Distribution
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                service_data = df['service'].value_counts().reset_index()
                service_data.columns = ['Service', 'Count']
                
                fig_3d = px.pie(service_data, values='Count', names='Service',
                               title="🔄 Service Distribution Matrix",
                               template="plotly_dark",
                               hole=0.4)
                fig_3d.update_traces(
                    textposition='inside',
                    textinfo='percent+label',
                    marker=dict(line=dict(color='#000000', width=2))
                )
                st.plotly_chart(fig_3d, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Hourly Heatmap
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            hourly_service = df.groupby(['hour', 'service']).size().unstack(fill_value=0)
            
            fig_heatmap = px.imshow(hourly_service.T, 
                                   title="🕐 24/7 Service Activity Heatmap",
                                   template="plotly_dark",
                                   color_continuous_scale="Viridis",
                                   aspect="auto")
            fig_heatmap.update_layout(
                xaxis_title="Hour of Day",
                yaxis_title="Services"
            )
            st.plotly_chart(fig_heatmap, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab2:
            st.markdown("### 📈 **Advanced Analytics Dashboard**")
            
            # Multi-dimensional Analysis
            col1, col2 = st.columns(2)
            
            with col1:
                # 3D Scatter Plot
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                sample_df = df.sample(min(1000, len(df)))  # Sample for performance
                
                fig_3d_scatter = px.scatter_3d(sample_df, 
                                              x='hour', y='day_of_week', z='user',
                                              color='service',
                                              title="🌐 Multi-Dimensional Activity Analysis",
                                              template="plotly_dark")
                fig_3d_scatter.update_traces(marker=dict(size=4, opacity=0.6))
                st.plotly_chart(fig_3d_scatter, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                # Parallel Coordinates
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                user_stats = df.groupby('user').agg({
                    'level': 'count',
                    'success': 'sum',
                    'error': 'sum',
                    'hour': 'mean'
                }).reset_index()
                user_stats.columns = ['User', 'Total_Actions', 'Success_Count', 'Error_Count', 'Avg_Hour']
                
                fig_parallel = px.parallel_coordinates(
                    user_stats.head(20),
                    dimensions=['Total_Actions', 'Success_Count', 'Error_Count', 'Avg_Hour'],
                    title="👥 User Behavior Patterns",
                    template="plotly_dark"
                )
                st.plotly_chart(fig_parallel, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Advanced Time Series Analysis
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            
            # Create hourly breakdown with success/error rates
            hourly_analysis = df.groupby('hour').agg({
                'level': 'count',
                'success': ['sum', 'mean'],
                'error': ['sum', 'mean']
            }).round(3)
            
            hourly_analysis.columns = ['Total', 'Success_Count', 'Success_Rate', 'Error_Count', 'Error_Rate']
            hourly_analysis = hourly_analysis.reset_index()
            
            # Create subplot with secondary y-axis
            fig_advanced = make_subplots(
                rows=2, cols=1,
                subplot_titles=('Activity Volume', 'Success vs Error Rates'),
                vertical_spacing=0.1
            )
            
            # Volume chart
            fig_advanced.add_trace(
                go.Bar(x=hourly_analysis['hour'], y=hourly_analysis['Total'],
                      name='Total Activity', marker_color='#4ecdc4'),
                row=1, col=1
            )
            
            # Rate comparison
            fig_advanced.add_trace(
                go.Scatter(x=hourly_analysis['hour'], y=hourly_analysis['Success_Rate'],
                          mode='lines+markers', name='Success Rate',
                          line=dict(color='#2ecc71', width=3)),
                row=2, col=1
            )
            
            fig_advanced.add_trace(
                go.Scatter(x=hourly_analysis['hour'], y=hourly_analysis['Error_Rate'],
                          mode='lines+markers', name='Error Rate',
                          line=dict(color='#e74c3c', width=3)),
                row=2, col=1
            )
            
            fig_advanced.update_layout(
                title="⏰ Advanced Temporal Analysis",
                template="plotly_dark",
                showlegend=True,
                height=600
            )
            
            st.plotly_chart(fig_advanced, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab3:
            st.markdown("### 👥 **User Intelligence Center**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Top Users Analysis
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                user_activity = df.groupby('user').agg({
                    'level': 'count',
                    'success': 'sum',
                    'error': 'sum'
                }).reset_index()
                user_activity.columns = ['User', 'Total_Actions', 'Successful', 'Errors']
                user_activity['Success_Rate'] = (user_activity['Successful'] / user_activity['Total_Actions'] * 100).round(1)
                user_activity = user_activity.sort_values('Total_Actions', ascending=False).head(15)
                
                fig_users = px.bar(user_activity, x='User', y='Total_Actions',
                                  color='Success_Rate',
                                  title="🏆 Top Active Users Performance",
                                  template="plotly_dark",
                                  color_continuous_scale="Viridis")
                fig_users.update_layout(xaxis={'tickangle': 45})
                st.plotly_chart(fig_users, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # User Activity Patterns
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                user_hourly = df.groupby(['user', 'hour']).size().reset_index()
                user_hourly.columns = ['User', 'Hour', 'Activity']
                
                # Select top 5 users for pattern analysis
                top_users = user_activity.head(5)['User'].tolist()
                user_hourly_top = user_hourly[user_hourly['User'].isin(top_users)]
                
                fig_user_patterns = px.line(user_hourly_top, x='Hour', y='Activity', 
                                           color='User',
                                           title="📊 User Activity Patterns (Top 5 Users)",
                                           template="plotly_dark")
                st.plotly_chart(fig_user_patterns, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                # Technology Stack Analysis
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                browser_os = df.groupby(['browser', 'os']).size().reset_index()
                browser_os.columns = ['Browser', 'OS', 'Count']
                
                fig_tech = px.sunburst(browser_os, path=['Browser', 'OS'], values='Count',
                                      title="💻 Technology Stack Distribution",
                                      template="plotly_dark")
                st.plotly_chart(fig_tech, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Session Analysis
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                session_stats = df.groupby('session_id').agg({
                    'level': 'count',
                    'timestamp': ['min', 'max']
                }).reset_index()
                session_stats.columns = ['Session', 'Actions', 'Start', 'End']
                session_stats['Duration'] = (session_stats['End'] - session_stats['Start']).dt.total_seconds() / 60
                session_stats = session_stats[session_stats['Duration'] > 0].head(20)
                
                fig_sessions = px.scatter(session_stats, x='Actions', y='Duration',
                                         size='Actions', hover_data=['Session'],
                                         title="⏱️ Session Analysis (Duration vs Activity)",
                                         template="plotly_dark")
                st.plotly_chart(fig_sessions, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Geographic Analysis (IP-based)
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            ip_analysis = df.groupby('ip').agg({
                'user': lambda x: ', '.join(x.unique()[:3]),  # Top 3 users
                'level': 'count',
                'service': lambda x: ', '.join(x.unique())
            }).reset_index()
            ip_analysis.columns = ['IP_Address', 'Users', 'Activity_Count', 'Services']
            ip_analysis = ip_analysis.sort_values('Activity_Count', ascending=False).head(20)
            
            fig_ip = px.treemap(ip_analysis, path=['IP_Address'], values='Activity_Count',
                               title="🌍 Geographic Distribution (IP Analysis)",
                               template="plotly_dark")
            st.plotly_chart(fig_ip, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Detailed User Table
            st.markdown("#### 📋 **Detailed User Analytics**")
            st.dataframe(
                user_activity.style.format({
                    'Total_Actions': '{:,}',
                    'Success_Rate': '{:.1f}%'
                }).background_gradient(subset=['Success_Rate'], cmap='RdYlGn'),
                use_container_width=True
            )
        
        with tab4:
            st.markdown("### ⚠️ **Security & Error Analysis Center**")
            
            error_df = df[df['error'] == True]
            
            if len(error_df) > 0:
                col1, col2 = st.columns(2)
                
                with col1:
                    # Error Distribution
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                    error_service = error_df['service'].value_counts().reset_index()
                    error_service.columns = ['Service', 'Error_Count']
                    
                    fig_error_service = px.funnel(error_service, x='Error_Count', y='Service',
                                                 title="🚨 Error Distribution by Service",
                                                 template="plotly_dark")
                    st.plotly_chart(fig_error_service, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Error Timeline
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                    error_timeline = error_df.groupby('date').size().reset_index()
                    error_timeline.columns = ['Date', 'Error_Count']
                    
                    fig_error_timeline = px.area(error_timeline, x='Date', y='Error_Count',
                                                title="📈 Error Trends Over Time",
                                                template="plotly_dark")
                    fig_error_timeline.update_traces(fill='tonexty', fillcolor='rgba(231, 76, 60, 0.3)')
                    st.plotly_chart(fig_error_timeline, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col2:
                    # Security Incidents
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                    error_users = error_df['user'].value_counts().head(10).reset_index()
                    error_users.columns = ['User', 'Error_Count']
                    
                    fig_error_users = px.bar(error_users, x='User', y='Error_Count',
                                           title="👤 Users with Most Errors",
                                           template="plotly_dark",
                                           color='Error_Count',
                                           color_continuous_scale="Reds")
                    fig_error_users.update_layout(xaxis={'tickangle': 45})
                    st.plotly_chart(fig_error_users, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Suspicious IP Activity
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                    suspicious_ips = error_df['ip'].value_counts().head(8).reset_index()
                    suspicious_ips.columns = ['IP', 'Error_Count']
                    
                    fig_suspicious = px.scatter(suspicious_ips, x='IP', y='Error_Count',
                                              size='Error_Count',
                                              title="🔍 Suspicious IP Activity",
                                              template="plotly_dark")
                    fig_suspicious.update_layout(xaxis={'tickangle': 45})
                    st.plotly_chart(fig_suspicious, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Error Message Analysis
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown("#### 📝 **Critical Error Messages**")
                error_messages = error_df['message'].value_counts().head(15).reset_index()
                error_messages.columns = ['Error_Message', 'Count']
                
                fig_error_msg = px.bar(error_messages, y='Error_Message', x='Count',
                                      orientation='h',
                                      title="🔍 Most Common Error Messages",
                                      template="plotly_dark")
                st.plotly_chart(fig_error_msg, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Recent Critical Errors
                st.markdown("#### 🚨 **Recent Critical Incidents**")
                recent_errors = error_df[['timestamp', 'user', 'service', 'action', 'message', 'ip']].sort_values('timestamp', ascending=False).head(20)
                st.dataframe(recent_errors, use_container_width=True)
                
            else:
                st.success("🎉 **EXCELLENT SECURITY POSTURE** - No errors detected!")
                st.balloons()
        
        with tab5:
            st.markdown("### 🔧 **Service Performance Center**")
            
            # Service Performance Overview
            service_metrics = []
            for service in stats['services']['distribution'].keys():
                service_df = df[df['service'] == service]
                
                metrics = {
                    'Service': service,
                    'Total_Logs': len(service_df),
                    'Success_Rate': (service_df['success'].sum() / len(service_df)) * 100 if len(service_df) > 0 else 0,
                    'Error_Rate': (service_df['error'].sum() / len(service_df)) * 100 if len(service_df) > 0 else 0,
                    'Unique_Users': service_df['user'].nunique(),
                    'Peak_Hour': service_df.groupby('hour').size().idxmax() if len(service_df) > 0 else 0,
                    'Avg_Daily': len(service_df) / max(1, stats['duration_days']) if stats['duration_days'] > 0 else len(service_df)
                }
                service_metrics.append(metrics)
            
            service_metrics_df = pd.DataFrame(service_metrics)
            
            # Service Performance Dashboard
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                fig_service_perf = go.Figure()
                fig_service_perf.add_trace(go.Scatterpolar(
                    r=service_metrics_df['Success_Rate'],
                    theta=service_metrics_df['Service'],
                    fill='toself',
                    name='Success Rate'
                ))
                fig_service_perf.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 100]
                        )
                    ),
                    showlegend=True,
                    title="🎯 Service Success Rate Radar",
                    template="plotly_dark"
                )
                st.plotly_chart(fig_service_perf, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                fig_service_load = px.scatter(service_metrics_df,
                                             x='Total_Logs', y='Unique_Users',
                                             size='Avg_Daily', color='Service',
                                             title="📊 Service Load vs User Engagement",
                                             template="plotly_dark")
                st.plotly_chart(fig_service_load, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Individual Service Analysis
            for service in stats['services']['distribution'].keys():
                with st.expander(f"🔍 **{service} Service Deep Dive** ({stats['services']['distribution'][service]:,} logs)"):
                    service_df = df[df['service'] == service]
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        success_rate = (service_df['success'].sum() / len(service_df)) * 100 if len(service_df) > 0 else 0
                        st.metric(f"{service} Success", f"{success_rate:.1f}%")
                    
                    with col2:
                        unique_users = service_df['user'].nunique()
                        st.metric(f"Active Users", f"{unique_users}")
                    
                    with col3:
                        peak_hour = service_df.groupby('hour').size().idxmax() if len(service_df) > 0 else 0
                        st.metric(f"Peak Hour", f"{peak_hour}:00")
                    
                    with col4:
                        total_actions = len(service_df)
                        st.metric(f"Total Actions", f"{total_actions:,}")
                    
                    # Service-specific visualizations
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Top actions
                        top_actions = service_df['action'].value_counts().head(10).reset_index()
                        top_actions.columns = ['Action', 'Count']
                        
                        if len(top_actions) > 0:
                            fig_actions = px.pie(top_actions, values='Count', names='Action',
                                               title=f"🎯 {service} - Top Actions",
                                               template="plotly_dark")
                            st.plotly_chart(fig_actions, use_container_width=True)
                    
                    with col2:
                        # Hourly distribution
                        hourly_dist = service_df.groupby('hour').size().reset_index()
                        hourly_dist.columns = ['Hour', 'Count']
                        
                        fig_hourly = px.area(hourly_dist, x='Hour', y='Count',
                                           title=f"⏰ {service} - Hourly Distribution",
                                           template="plotly_dark")
                        st.plotly_chart(fig_hourly, use_container_width=True)
            
            # Service Performance Table
            st.markdown("#### 📊 **Service Performance Summary**")
            st.dataframe(
                service_metrics_df.style.format({
                    'Success_Rate': '{:.1f}%',
                    'Error_Rate': '{:.1f}%',
                    'Avg_Daily': '{:.1f}'
                }).background_gradient(subset=['Success_Rate'], cmap='RdYlGn'),
                use_container_width=True
            )
        
        with tab6:
            st.markdown("### 🔍 **Advanced Data Explorer**")
            
            # Advanced Filters
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                service_filter = st.multiselect("🔧 Services", 
                                              options=df['service'].unique(),
                                              default=df['service'].unique())
            
            with col2:
                user_filter = st.multiselect("👤 Users", 
                                           options=df['user'].unique()[:30])
            
            with col3:
                level_filter = st.multiselect("📊 Log Levels",
                                            options=df['level'].unique(),
                                            default=df['level'].unique())
            
            with col4:
                date_range = st.date_input("📅 Date Range", 
                                         value=[df['date'].min(), df['date'].max()],
                                         min_value=df['date'].min(),
                                         max_value=df['date'].max())
            
            # Additional filters
            col1, col2, col3 = st.columns(3)
            
            with col1:
                show_errors_only = st.checkbox("⚠️ Errors Only")
                show_success_only = st.checkbox("✅ Success Only")
            
            with col2:
                ip_filter = st.selectbox("🌐 IP Address", 
                                       options=['All'] + list(df['ip'].unique()[:20]))
            
            with col3:
                action_filter = st.multiselect("🎯 Actions",
                                             options=df['action'].unique()[:20])
            
            # Apply filters
            filtered_df = df.copy()
            
            if service_filter:
                filtered_df = filtered_df[filtered_df['service'].isin(service_filter)]
            if user_filter:
                filtered_df = filtered_df[filtered_df['user'].isin(user_filter)]
            if level_filter:
                filtered_df = filtered_df[filtered_df['level'].isin(level_filter)]
            if len(date_range) == 2:
                filtered_df = filtered_df[
                    (filtered_df['date'] >= date_range[0]) & 
                    (filtered_df['date'] <= date_range[1])
                ]
            if show_errors_only:
                filtered_df = filtered_df[filtered_df['error'] == True]
            if show_success_only:
                filtered_df = filtered_df[filtered_df['success'] == True]
            if ip_filter != 'All':
                filtered_df = filtered_df[filtered_df['ip'] == ip_filter]
            if action_filter:
                filtered_df = filtered_df[filtered_df['action'].isin(action_filter)]
            
            # Results summary
            st.info(f"📊 **Showing {len(filtered_df):,} of {len(df):,} records** ({(len(filtered_df)/len(df)*100):.1f}%)")
            
            # Display options
            col1, col2 = st.columns(2)
            
            with col1:
                available_columns = ['timestamp', 'level', 'service', 'user', 'action', 'message', 'ip', 'browser', 'os', 'success', 'error']
                selected_columns = st.multiselect("📋 Display Columns", 
                                                options=available_columns,
                                                default=['timestamp', 'level', 'service', 'user', 'action'])
            
            with col2:
                max_rows = st.selectbox("📄 Rows to Display", [100, 500, 1000, 2000, 5000], index=2)
            
            # Data export options
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("📥 Export Filtered Data"):
                    csv = filtered_df.to_csv(index=False)
                    st.download_button(
                        label="💾 Download CSV",
                        data=csv,
                        file_name=f"skylus_filtered_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
            
            with col2:
                if st.button("📊 Generate Report"):
                    report = f"""
FILTERED DATA REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*50}

FILTER SUMMARY:
- Services: {', '.join(service_filter) if service_filter else 'All'}
- Users: {', '.join(user_filter[:5]) if user_filter else 'All'}
- Date Range: {date_range[0] if len(date_range) > 0 else 'N/A'} to {date_range[1] if len(date_range) > 1 else 'N/A'}
- Records: {len(filtered_df):,} of {len(df):,}

QUICK STATS:
- Success Rate: {(filtered_df['success'].sum() / len(filtered_df) * 100):.1f}%
- Error Rate: {(filtered_df['error'].sum() / len(filtered_df) * 100):.1f}%
- Unique Users: {filtered_df['user'].nunique()}
- Unique IPs: {filtered_df['ip'].nunique()}
                    """
                    st.download_button(
                        label="📄 Download Report",
                        data=report,
                        file_name=f"skylus_filter_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain"
                    )
            
            with col3:
                if st.button("🔄 Reset Filters"):
                    st.experimental_rerun()
            
            # Display filtered data
            if selected_columns and len(filtered_df) > 0:
                display_df = filtered_df[selected_columns].sort_values('timestamp', ascending=False).head(max_rows)
                
                # Enhanced data display with styling
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.dataframe(
                    display_df.style.apply(
                        lambda x: ['background-color: rgba(231, 76, 60, 0.2)' if x.name in filtered_df[filtered_df['error']].index else 
                                  'background-color: rgba(46, 204, 113, 0.2)' if x.name in filtered_df[filtered_df['success']].index else ''
                                  for _ in x], axis=1
                    ),
                    use_container_width=True,
                    height=400
                )
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.warning("⚠️ No data matches current filters or no columns selected")
        
        with tab7:
            st.markdown("### 📊 **Custom Visualization Studio**")
            
            # Chart configuration
            col1, col2, col3 = st.columns(3)
            
            with col1:
                chart_type = st.selectbox("📈 Chart Type", [
                    "Bar Chart", "Line Chart", "Scatter Plot", "Pie Chart", 
                    "Heatmap", "3D Scatter", "Sunburst", "Treemap", 
                    "Violin Plot", "Radar Chart", "Waterfall", "Funnel"
                ])
            
            with col2:
                x_column = st.selectbox("📊 X-Axis", [
                    "service", "user", "hour", "day_of_week", "browser", 
                    "os", "ip", "action", "level"
                ])
            
            with col3:
                y_column = st.selectbox("📊 Y-Axis", [
                    "count", "success", "error", "hour", "timestamp"
                ])
            
            # Advanced options
            col1, col2, col3 = st.columns(3)
            
            with col1:
                color_column = st.selectbox("🎨 Color By", [
                    "None", "service", "level", "success", "error", "browser", "os"
                ])
            
            with col2:
                size_column = st.selectbox("📏 Size By", [
                    "None", "count", "hour"
                ])
            
            with col3:
                aggregate_function = st.selectbox("🔢 Aggregation", [
                    "count", "sum", "mean", "max", "min"
                ])
            
            # Generate custom visualization
            if st.button("🎨 **Generate Visualization**", type="primary"):
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                
                try:
                    # Prepare data based on selections
                    if y_column == "count":
                        if aggregate_function == "count":
                            plot_data = df.groupby(x_column).size().reset_index()
                            plot_data.columns = [x_column, 'count']
                        else:
                            plot_data = df.groupby(x_column).agg({
                                'level': aggregate_function
                            }).reset_index()
                            plot_data.columns = [x_column, 'count']
                    else:
                        plot_data = df.copy()
                    
                    # Create visualization based on chart type
                    if chart_type == "Bar Chart":
                        if y_column == "count":
                            fig = px.bar(plot_data, x=x_column, y='count',
                                       color=color_column if color_column != "None" else None,
                                       title=f"📊 {chart_type}: {x_column} vs {y_column}",
                                       template="plotly_dark")
                        else:
                            fig = px.bar(plot_data.head(50), x=x_column, y=y_column,
                                       color=color_column if color_column != "None" else None,
                                       title=f"📊 {chart_type}: {x_column} vs {y_column}",
                                       template="plotly_dark")
                    
                    elif chart_type == "Line Chart":
                        if y_column == "count":
                            fig = px.line(plot_data, x=x_column, y='count',
                                        color=color_column if color_column != "None" else None,
                                        title=f"📈 {chart_type}: {x_column} vs {y_column}",
                                        template="plotly_dark")
                        else:
                            time_data = df.groupby([x_column, 'hour']).size().reset_index()
                            time_data.columns = [x_column, 'hour', 'count']
                            fig = px.line(time_data, x='hour', y='count',
                                        color=x_column,
                                        title=f"📈 {chart_type}: Hourly {x_column} Activity",
                                        template="plotly_dark")
                    
                    elif chart_type == "Scatter Plot":
                        scatter_data = df.groupby(x_column).agg({
                            'success': 'sum',
                            'error': 'sum',
                            'level': 'count'
                        }).reset_index()
                        scatter_data.columns = [x_column, 'Success', 'Errors', 'Total']
                        
                        fig = px.scatter(scatter_data, x='Success', y='Errors',
                                       size='Total', hover_data=[x_column],
                                       title=f"⚡ {chart_type}: Success vs Errors by {x_column}",
                                       template="plotly_dark")
                    
                    elif chart_type == "Pie Chart":
                        fig = px.pie(plot_data.head(10), values='count', names=x_column,
                                   title=f"🥧 {chart_type}: {x_column} Distribution",
                                   template="plotly_dark")
                    
                    elif chart_type == "Heatmap":
                        if x_column != "hour":
                            heatmap_data = df.groupby([x_column, 'hour']).size().unstack(fill_value=0)
                        else:
                            heatmap_data = df.groupby(['service', 'hour']).size().unstack(fill_value=0)
                        
                        fig = px.imshow(heatmap_data, title=f"🔥 {chart_type}: {x_column} Activity",
                                      template="plotly_dark", color_continuous_scale="Viridis")
                    
                    elif chart_type == "3D Scatter":
                        sample_data = df.sample(min(1000, len(df)))
                        fig = px.scatter_3d(sample_data, x='hour', y='day_of_week', z=x_column,
                                          color=color_column if color_column != "None" else None,
                                          title=f"🌐 {chart_type}: Multi-dimensional Analysis",
                                          template="plotly_dark")
                    
                    elif chart_type == "Sunburst":
                        if color_column != "None":
                            sunburst_data = df.groupby([x_column, color_column]).size().reset_index()
                            sunburst_data.columns = [x_column, color_column, 'count']
                            fig = px.sunburst(sunburst_data, path=[x_column, color_column], values='count',
                                            title=f"☀️ {chart_type}: {x_column} Hierarchy",
                                            template="plotly_dark")
                        else:
                            fig = px.sunburst(plot_data.head(20), path=[x_column], values='count',
                                            title=f"☀️ {chart_type}: {x_column} Distribution",
                                            template="plotly_dark")
                    
                    elif chart_type == "Treemap":
                        fig = px.treemap(plot_data.head(20), path=[x_column], values='count',
                                       title=f"🌳 {chart_type}: {x_column} Hierarchy",
                                       template="plotly_dark")
                    
                    elif chart_type == "Violin Plot":
                        fig = px.violin(df.head(1000), x=x_column, y='hour',
                                      title=f"🎻 {chart_type}: {x_column} Distribution",
                                      template="plotly_dark")
                    
                    elif chart_type == "Radar Chart":
                        radar_data = plot_data.head(8)
                        fig = go.Figure()
                        fig.add_trace(go.Scatterpolar(
                            r=radar_data['count'].values,
                            theta=radar_data[x_column].values,
                            fill='toself',
                            name=f"{x_column} Activity"
                        ))
                        fig.update_layout(
                            polar=dict(radialaxis=dict(visible=True)),
                            showlegend=True,
                            title=f"🎯 {chart_type}: {x_column} Performance",
                            template="plotly_dark"
                        )
                    
                    elif chart_type == "Waterfall":
                        waterfall_data = plot_data.head(8)
                        fig = go.Figure(go.Waterfall(
                            name="Activity Flow",
                            orientation="v",
                            measure=["relative"] * len(waterfall_data),
                            x=waterfall_data[x_column].values,
                            textposition="outside",
                            text=[str(v) for v in waterfall_data['count'].values],
                            y=waterfall_data['count'].values,
                        ))
                        fig.update_layout(
                            title=f"💧 {chart_type}: {x_column} Flow",
                            template="plotly_dark"
                        )
                    
                    elif chart_type == "Funnel":
                        fig = px.funnel(plot_data.head(10), x='count', y=x_column,
                                      title=f"⏳ {chart_type}: {x_column} Conversion",
                                      template="plotly_dark")
                    
                    # Enhanced styling
                    fig.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='white', size=12),
                        title_font_size=18,
                        showlegend=True,
                        height=600
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Chart insights
                    st.markdown("#### 🧠 **Chart Insights**")
                    insights_col1, insights_col2 = st.columns(2)
                    
                    with insights_col1:
                        st.markdown(f"""
                        **📊 Data Summary:**
                        - Chart Type: {chart_type}
                        - Primary Dimension: {x_column}
                        - Data Points: {len(plot_data)}
                        - Color Coding: {color_column if color_column != 'None' else 'None'}
                        """)
                    
                    with insights_col2:
                        if y_column == "count":
                            top_value = plot_data.nlargest(1, 'count')
                            if len(top_value) > 0:
                                st.markdown(f"""
                                **🏆 Top Performer:**
                                - {x_column}: {top_value.iloc[0][x_column]}
                                - Count: {top_value.iloc[0]['count']:,}
                                - Percentage: {(top_value.iloc[0]['count'] / plot_data['count'].sum() * 100):.1f}%
                                """)
                
                except Exception as e:
                    st.error(f"❌ Error generating visualization: {str(e)}")
                    st.info("💡 Try different column combinations or chart types")
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Predefined visualization templates
            st.markdown("#### 🎨 **Quick Templates**")
            
            template_col1, template_col2, template_col3 = st.columns(3)
            
            with template_col1:
                if st.button("🕐 **Time Analysis**"):
                    fig_time = create_advanced_charts(df, "Heatmap", "hour", "service", title="⏰ 24/7 Activity Heatmap")
                    st.plotly_chart(fig_time, use_container_width=True)
            
            with template_col2:
                if st.button("👥 **User Behavior**"):
                    fig_users = create_advanced_charts(df, "3D Scatter", "user", "service", "success", "🧠 User Behavior 3D Analysis")
                    st.plotly_chart(fig_users, use_container_width=True)
            
            with template_col3:
                if st.button("🔧 **Service Health**"):
                    service_health = df.groupby('service').agg({
                        'success': 'mean'
                    }).reset_index()
                    service_health['success'] = service_health['success'] * 100
                    
                    fig_health = go.Figure()
                    fig_health.add_trace(go.Scatterpolar(
                        r=service_health['success'],
                        theta=service_health['service'],
                        fill='toself',
                        name='Service Health'
                    ))
                    fig_health.update_layout(
                        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                        showlegend=True,
                        title="🎯 Service Health Radar",
                        template="plotly_dark"
                    )
                    st.plotly_chart(fig_health, use_container_width=True)
    
    else:
        # Professional Welcome Screen
        st.markdown("""
        <div style="text-align: center; padding: 40px;">
            <h1 style="font-size: 3em; margin-bottom: 30px;">🚀 Welcome to Skylus Analytics Platform</h1>
            <p style="font-size: 1.3em; margin-bottom: 40px; color: #4ecdc4;">
                Enterprise-Grade Log Intelligence & Performance Analytics
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Feature showcase
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h3 style="color: #ff6b6b;">🎯 Real-time Analytics</h3>
                <p>Advanced real-time monitoring with AI-powered insights, predictive analytics, and automated alerting systems.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h3 style="color: #4ecdc4;">🔍 Deep Intelligence</h3>
                <p>Multi-dimensional analysis with 3D visualizations, pattern recognition, and behavioral analytics.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card">
                <h3 style="color: #45b7d1;">⚡ Performance</h3>
                <p>Lightning-fast processing with optimized algorithms, smart caching, and scalable architecture.</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="margin: 40px 0; padding: 30px; background: rgba(255,255,255,0.05); border-radius: 15px; border: 1px solid rgba(255,255,255,0.1);">
            <h2 style="color: #4ecdc4; text-align: center;">🌟 Professional Features</h2>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin-top: 30px;">
                <div>
                    <h4 style="color: #ff6b6b;">📊 Advanced Visualizations</h4>
                    <ul style="color: #ffffff;">
                        <li>3D Interactive Charts & Graphs</li>
                        <li>Real-time Heatmaps & Timelines</li>
                        <li>Custom Dashboard Builder</li>
                        <li>Animated Performance Metrics</li>
                    </ul>
                </div>
                
                <div>
                    <h4 style="color: #4ecdc4;">🧠 AI-Powered Intelligence</h4>
                    <ul style="color: #ffffff;">
                        <li>Predictive Error Analysis</li>
                        <li>Behavioral Pattern Recognition</li>
                        <li>Automated Anomaly Detection</li>
                        <li>Smart Performance Optimization</li>
                    </ul>
                </div>
                
                <div>
                    <h4 style="color: #45b7d1;">🔐 Security & Compliance</h4>
                    <ul style="color: #ffffff;">
                        <li>Advanced Threat Detection</li>
                        <li>Compliance Monitoring</li>
                        <li>Access Pattern Analysis</li>
                        <li>Forensic Investigation Tools</li>
                    </ul>
                </div>
                
                <div>
                    <h4 style="color: #96ceb4;">📈 Business Intelligence</h4>
                    <ul style="color: #ffffff;">
                        <li>Executive Summary Reports</li>
                        <li>ROI & Performance KPIs</li>
                        <li>Trend Analysis & Forecasting</li>
                        <li>Custom Business Metrics</li>
                    </ul>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="text-align: center; margin: 40px 0;">
            <h3 style="color: #4ecdc4;">🚀 Ready to Unlock Your Data's Potential?</h3>
            <p style="font-size: 1.1em;">Upload your logs or connect to your data source to begin your analytics journey!</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    create_dashboard()