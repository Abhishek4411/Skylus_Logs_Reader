# 🔧 Troubleshooting Guide

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
