# Quick Start Guide - Business Analytics Automator

## 🚀 Get Up and Running in 5 Minutes

### Prerequisites Check
```bash
# Check Node.js (need 18+)
node --version

# Check Python (need 3.9+)
python --version

# Check npm
npm --version

# Check pip
pip --version
```

### Installation

**Step 1: Install Frontend Dependencies**
```bash
npm install
```

**Step 2: Install Backend Dependencies**
```bash
pip install -r requirements.txt
```

### Running the Application

**Option 1: Run Both Servers Concurrently (Recommended)**
```bash
npm start
```

**Option 2: Run Separately**

Terminal 1 (Frontend):
```bash
npm run dev
```

Terminal 2 (Backend):
```bash
python backend_api.py
```

### Access the Application
Open your browser and navigate to:
```
http://localhost:3000
```

## 📝 First Test

1. **Prepare test data** (create `test_data.csv`):
```csv
date,revenue,product,category
2024-01-01,50000,Product A,Software
2024-01-02,45000,Product B,Services
2024-01-03,60000,Product A,Software
2024-01-04,55000,Product C,Hardware
2024-01-05,70000,Product A,Software
```

2. **Upload the file**
   - Click or drag the test file to the upload zone
   - Wait for analysis (2-3 seconds)

3. **View the dashboard**
   - Check summary cards
   - Explore charts
   - Review trends

4. **Export to Power BI**
   - Click "Export to PBIX" button
   - Download the `.pbix` file
   - Open in Power BI Desktop

## 🔧 Common Issues and Fixes

### Issue: Port Already in Use
```bash
# Kill process on port 3000
lsof -ti:3000 | xargs kill -9

# Kill process on port 5000
lsof -ti:5000 | xargs kill -9
```

### Issue: Module Not Found
```bash
# Reinstall dependencies
npm install
pip install -r requirements.txt
```

### Issue: CORS Error
Make sure both servers are running and check `vite.config.js` proxy settings.

### Issue: File Upload Fails
```bash
# Ensure /tmp directory is writable
chmod 777 /tmp
```

## 📊 Sample Data Formats

### CSV Format
```csv
date,revenue,product
2024-01-01,10000,Widget
2024-01-02,15000,Gadget
```

### JSON Format
```json
[
  {"date": "2024-01-01", "revenue": 10000, "product": "Widget"},
  {"date": "2024-01-02", "revenue": 15000, "product": "Gadget"}
]
```

### Excel Format
| Date       | Revenue | Product |
|------------|---------|---------|
| 2024-01-01 | 10000   | Widget  |
| 2024-01-02 | 15000   | Gadget  |

## 🎯 Key Features to Test

1. **File Upload**
   - Drag and drop
   - File type validation
   - Loading indicators

2. **Dashboard**
   - Summary metrics
   - Revenue trend chart
   - Product performance
   - Category distribution

3. **Export**
   - PBIX generation
   - File download
   - Open in Power BI

## 🔌 API Testing with cURL

**Health Check**
```bash
curl http://localhost:5000/api/health
```

**Upload File**
```bash
curl -X POST -F "file=@test_data.csv" http://localhost:5000/api/upload
```

**Export PBIX**
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"analysis": {...}}' \
  http://localhost:5000/api/export-pbix \
  --output report.pbix
```

## 📱 Development Workflow

### Making Changes

**Frontend Changes**
1. Edit files in `/src`
2. Hot reload automatically updates browser
3. Check console for errors

**Backend Changes**
1. Edit `backend_api.py`
2. Restart Python server
3. Test with API calls

### Adding New Features

**New Chart Type**
```jsx
// In business-analytics-dashboard.jsx
<ResponsiveContainer width="100%" height={300}>
  <AreaChart data={yourData}>
    <Area type="monotone" dataKey="value" stroke="#8884d8" />
  </AreaChart>
</ResponsiveContainer>
```

**New Analysis Method**
```python
# In backend_api.py
def _analyze_custom(self, df):
    # Your custom analysis logic
    return results
```

**New API Endpoint**
```python
@app.route('/api/custom-endpoint', methods=['POST'])
def custom_endpoint():
    # Your endpoint logic
    return jsonify(result)
```

## 🏗️ Project Structure Quick Reference
```
business-analytics-automator/
├── src/
│   ├── business-analytics-dashboard.jsx  # Main component
│   ├── main.jsx                          # Entry point
│   └── index.css                         # Styles
├── backend_api.py                        # Flask server
├── pbix_generator_advanced.py            # Advanced PBIX
├── package.json                          # Node dependencies
├── requirements.txt                      # Python dependencies
├── vite.config.js                        # Vite config
├── tailwind.config.js                    # Tailwind config
├── README.md                             # Full documentation
└── ARCHITECTURE.md                       # System architecture
```

## 🎓 Learning Resources

**React & Vite**
- [React Docs](https://react.dev/)
- [Vite Guide](https://vitejs.dev/guide/)

**Flask**
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)

**Pandas**
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [10 Minutes to Pandas](https://pandas.pydata.org/docs/user_guide/10min.html)

**Power BI**
- [Power BI Documentation](https://docs.microsoft.com/en-us/power-bi/)
- [DAX Guide](https://dax.guide/)

## 💡 Pro Tips

1. **Performance**: For large files (>10MB), consider implementing chunked processing
2. **Testing**: Use Postman or Insomnia for API testing
3. **Debugging**: Use browser DevTools and Flask debug mode
4. **Styling**: Customize colors in `tailwind.config.js`
5. **Data**: The BusinessAnalyzer auto-detects columns - no schema required!

## 🚀 Next Steps

1. ✅ Get the basic app running
2. ✅ Upload and analyze a sample file
3. ✅ Export to PBIX and view in Power BI
4. 📖 Read the full README.md for advanced features
5. 🏗️ Review ARCHITECTURE.md to understand the system
6. 🔧 Customize for your specific business needs
7. 🚢 Deploy to production

## 🤝 Need Help?

- Check `README.md` for detailed documentation
- Review `ARCHITECTURE.md` for system design
- Look at code comments for inline explanations
- Test with the provided sample data first

---

**Built with ❤️ by Claude - Your Mastermind Coding Entity**

*Remember: This is a foundation. The real power comes when you customize it for your specific business intelligence needs!*
