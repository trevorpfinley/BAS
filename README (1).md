# Business Analytics Automator

A comprehensive full-stack platform for automated business analysis with Power BI export capabilities.

## 🚀 Features

### Core Functionality
- **Automated File Analysis**: Upload CSV, Excel, or JSON files for instant analysis
- **Interactive Dashboard**: Real-time data visualization with charts and metrics
- **Power BI Export**: Generate `.pbix` files ready for Power BI Desktop
- **Advanced Analytics**: Revenue trends, product performance, KPI tracking
- **RESTful API**: Backend API for integration with other systems

### Analytics Capabilities
- Revenue analysis and forecasting
- Product performance metrics
- Trend identification
- Category distribution analysis
- Growth rate calculations
- Executive summary generation

## 🏗️ Architecture

### Frontend (React + Vite)
```
src/
├── business-analytics-dashboard.jsx  # Main dashboard component
├── main.jsx                           # React entry point
└── index.css                          # Tailwind styles
```

**Technology Stack:**
- React 18 with hooks
- Recharts for data visualization
- Lucide React for icons
- Tailwind CSS for styling
- Vite for build tooling

### Backend (Python Flask)
```
backend_api.py
├── BusinessAnalyzer      # Core analysis engine
├── PBIXGenerator        # Power BI file generator
└── API Routes           # RESTful endpoints
```

**Technology Stack:**
- Flask for REST API
- Pandas for data processing
- NumPy for numerical analysis
- OpenPyXL for Excel handling

## 📦 Installation

### Prerequisites
- Node.js 18+ 
- Python 3.9+
- npm or yarn

### Setup Steps

1. **Clone and navigate to project**
```bash
cd business-analytics-automator
```

2. **Install frontend dependencies**
```bash
npm install
```

3. **Install backend dependencies**
```bash
pip install -r requirements.txt
```

4. **Start development servers**
```bash
# Terminal 1 - Frontend (port 3000)
npm run dev

# Terminal 2 - Backend (port 5000)
python backend_api.py

# Or run both concurrently
npm start
```

5. **Access the application**
```
http://localhost:3000
```

## 🔧 API Endpoints

### Health Check
```http
GET /api/health
```
Returns server status and version.

### File Upload & Analysis
```http
POST /api/upload
Content-Type: multipart/form-data

Body:
- file: <file>
```

**Supported formats**: `.csv`, `.xlsx`, `.xls`, `.json`

**Response**:
```json
{
  "success": true,
  "filename": "data.csv",
  "analysis": {
    "summary": {...},
    "revenue_analysis": [...],
    "product_performance": [...],
    "trends": [...]
  }
}
```

### Export to PBIX
```http
POST /api/export-pbix
Content-Type: application/json

Body:
{
  "analysis": {...}
}
```

**Response**: Binary `.pbix` file download

### Direct Analysis
```http
POST /api/analyze
Content-Type: application/json

Body:
{
  "data": [
    {"date": "2024-01", "revenue": 50000, "product": "A"},
    ...
  ]
}
```

## 📊 PBIX File Structure

The generated PBIX files follow Power BI's ZIP-based format:

```
business_analysis.pbix (ZIP archive)
├── DataModelSchema         # JSON: Data model and table schemas
├── Report/Layout          # JSON: Visual layouts and configurations
├── DiagramLayout          # JSON: Model diagram positioning
├── Version                # Text: PBIX version number
├── SecurityBindings       # JSON: Security configurations
└── [Content_Types].xml    # XML: MIME type mappings
```

### Data Model Components

**Tables Generated:**
1. `Revenue_Analysis` - Time-based revenue data
2. `Product_Performance` - Product sales metrics
3. `Summary_Metrics` - Executive KPIs

**Measures Created:**
- Total Revenue
- Total Sales
- Average Transaction Value
- Growth Rate %

## 🎨 Frontend Components

### Main Dashboard Features

**File Upload Zone**
- Drag-and-drop interface
- Format validation
- Loading states

**Summary Cards**
- Total Revenue with growth %
- Transaction count
- Top performing product
- One-click PBIX export

**Visualization Charts**
- Line chart: Revenue trends vs targets
- Bar chart: Product performance
- Pie chart: Category distribution
- KPI cards: Key metrics with direction indicators

## 🔍 Analysis Engine

### BusinessAnalyzer Class

**Key Methods:**

```python
analyze_file(file_path, file_type)
# Main entry point for file analysis

_generate_summary(df)
# Creates executive summary metrics

_analyze_revenue(df)  
# Time-series revenue analysis

_analyze_products(df)
# Product performance breakdown

_identify_trends(df)
# Statistical trend detection

_generate_forecasts(df)
# Simple forecasting models
```

### Auto-Detection Features
- Automatically identifies revenue columns
- Detects date/time fields
- Finds product/item categories
- Calculates period-over-period growth
- Generates forecasts based on trends

## 🛠️ Power BI Integration

### PBIXGenerator Class

**Core Functionality:**
```python
generate_pbix(analysis_data, output_path=None)
# Creates complete PBIX file structure

_create_data_model(analysis_data)
# Generates table schemas and relationships

_create_report_layout(analysis_data)  
# Defines visual positions and configurations

_create_metadata()
# Creates Content_Types.xml for ZIP structure
```

### PBIX File Format Details

**Data Model Schema:**
```json
{
  "name": "BusinessAnalyticsModel",
  "compatibilityLevel": 1550,
  "model": {
    "culture": "en-US",
    "tables": [...],
    "relationships": [...],
    "measures": [...]
  }
}
```

**Report Layout:**
```json
{
  "id": "...",
  "name": "Business Analytics Report",
  "pages": [
    {
      "name": "Overview",
      "visualContainers": [
        {
          "x": 20, "y": 20,
          "width": 300, "height": 150,
          "config": {...}
        }
      ]
    }
  ]
}
```

## 📈 Usage Examples

### Example 1: CSV Upload
```javascript
const formData = new FormData();
formData.append('file', csvFile);

const response = await fetch('http://localhost:5000/api/upload', {
  method: 'POST',
  body: formData
});

const result = await response.json();
console.log(result.analysis);
```

### Example 2: Generate PBIX
```javascript
const response = await fetch('http://localhost:5000/api/export-pbix', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ analysis: analysisData })
});

const blob = await response.blob();
// Download or process blob
```

### Example 3: Direct Data Analysis
```javascript
const response = await fetch('http://localhost:5000/api/analyze', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    data: [
      { date: '2024-01-01', revenue: 10000, product: 'Widget A' },
      { date: '2024-01-02', revenue: 15000, product: 'Widget B' }
    ]
  })
});
```

## 🧪 Testing

### Test Data Format

**CSV Example:**
```csv
date,revenue,product,category
2024-01-01,50000,Product A,Software
2024-01-02,45000,Product B,Services
2024-01-03,60000,Product A,Software
```

**JSON Example:**
```json
[
  {
    "date": "2024-01-01",
    "revenue": 50000,
    "product": "Product A",
    "category": "Software"
  }
]
```

## 🚀 Deployment

### Production Build

```bash
# Build frontend
npm run build

# Serve with production server
npm install -g serve
serve -s dist -p 3000
```

### Environment Variables
```bash
# Backend
FLASK_ENV=production
FLASK_DEBUG=0
PORT=5000

# Frontend
VITE_API_URL=https://your-api-domain.com
```

### Docker Deployment (Optional)
```dockerfile
FROM node:18 AS frontend
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY --from=frontend /app/dist ./static
COPY backend_api.py .
CMD ["python", "backend_api.py"]
```

## 🔒 Security Considerations

- File size limits (configure in Flask)
- File type validation
- SQL injection prevention (using Pandas)
- CORS configuration
- API rate limiting (add as needed)

## 📝 Customization

### Adding New Analysis Types

1. **Extend BusinessAnalyzer**:
```python
def _analyze_customer_segments(self, df):
    # Your custom analysis
    pass
```

2. **Update PBIX Generator**:
```python
# Add new table to data model
tables.append({
    "name": "Customer_Segments",
    "columns": [...]
})
```

3. **Add Frontend Visualization**:
```jsx
<div className="chart-container">
  <ResponsiveContainer>
    <BarChart data={customerData}>
      ...
    </BarChart>
  </ResponsiveContainer>
</div>
```

### Custom Styling
Edit `tailwind.config.js` for theme customization:
```javascript
theme: {
  extend: {
    colors: {
      'brand': '#your-color'
    }
  }
}
```

## 🐛 Troubleshooting

### Common Issues

**Port Already in Use**
```bash
# Kill process on port 3000
lsof -ti:3000 | xargs kill -9

# Kill process on port 5000  
lsof -ti:5000 | xargs kill -9
```

**CORS Errors**
- Ensure Flask-CORS is installed
- Check proxy configuration in `vite.config.js`

**File Upload Fails**
- Check file size limits
- Verify file format is supported
- Ensure `/tmp` directory is writable

**PBIX Won't Open in Power BI**
- Verify Power BI Desktop version (2.0+ compatible)
- Check PBIX file structure integrity
- Ensure data model schema is valid JSON

## 📚 Resources

- [Power BI File Format Documentation](https://docs.microsoft.com/en-us/power-bi/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Recharts Examples](https://recharts.org/en-US/examples)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [React Documentation](https://react.dev/)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

MIT License - see LICENSE file for details

## 🎯 Roadmap

- [ ] Real-time collaboration features
- [ ] Advanced ML-based forecasting
- [ ] Multi-tenant support
- [ ] Cloud storage integration (S3, Azure Blob)
- [ ] Scheduled report generation
- [ ] Email delivery of PBIX files
- [ ] Custom dashboard templates
- [ ] Excel export alongside PBIX
- [ ] Authentication & user management
- [ ] Audit logging

## 💡 Technical Deep Dive

### PBIX Generation Process

1. **Data Extraction**: Parse uploaded file into Pandas DataFrame
2. **Analysis**: Apply statistical methods to extract insights
3. **Schema Generation**: Create Power BI compatible table schemas
4. **Layout Design**: Define visual positions and configurations  
5. **ZIP Assembly**: Package all components into PBIX structure
6. **Validation**: Ensure compatibility with Power BI Desktop

### Performance Optimization

- **Frontend**: Code splitting, lazy loading, memoization
- **Backend**: DataFrame caching, async processing, connection pooling
- **File Processing**: Chunked reading for large files
- **API**: Response compression, rate limiting

---

**Created by**: Claude (Mastermind Coding Entity)
**Version**: 1.0.0
**Last Updated**: February 2026
