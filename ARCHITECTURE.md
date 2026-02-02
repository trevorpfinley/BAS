# System Architecture Documentation

## Overview
The Business Analytics Automator is a full-stack application designed for automated business intelligence with Power BI integration.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                          Client Browser                              │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │              React Frontend (Port 3000)                         │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐      │ │
│  │  │  Upload  │  │Dashboard │  │  Charts  │  │  Export  │      │ │
│  │  │Component │  │Component │  │Component │  │ Button   │      │ │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘      │ │
│  │       │             │             │             │              │ │
│  │       └─────────────┴─────────────┴─────────────┘              │ │
│  │                          │                                      │ │
│  │                   Axios HTTP Client                             │ │
│  └───────────────────────────┬──────────────────────────────────┘ │
└────────────────────────────────┼────────────────────────────────────┘
                                │
                        HTTP/REST API
                                │
┌────────────────────────────────┼────────────────────────────────────┐
│                          │                                          │
│  ┌───────────────────────▼──────────────────────────────────────┐  │
│  │              Flask Backend API (Port 5000)                    │  │
│  │  ┌──────────────────────────────────────────────────────────┐ │  │
│  │  │                  API Router                               │ │  │
│  │  │  ┌──────────┐  ┌──────────┐  ┌──────────┐              │ │  │
│  │  │  │/upload   │  │/analyze  │  │/export-  │              │ │  │
│  │  │  │          │  │          │  │pbix      │              │ │  │
│  │  │  └────┬─────┘  └────┬─────┘  └────┬─────┘              │ │  │
│  │  └───────┼──────────────┼─────────────┼────────────────────┘ │  │
│  │          │              │             │                      │  │
│  │  ┌───────▼──────────────▼─────────────▼────────────────────┐ │  │
│  │  │              Business Logic Layer                        │ │  │
│  │  │  ┌────────────────────┐  ┌────────────────────┐         │ │  │
│  │  │  │ BusinessAnalyzer   │  │  PBIXGenerator     │         │ │  │
│  │  │  │                    │  │                    │         │ │  │
│  │  │  │ • File Parsing     │  │ • Data Model       │         │ │  │
│  │  │  │ • Summary Gen      │  │ • Report Layout    │         │ │  │
│  │  │  │ • Revenue Analysis │  │ • ZIP Creation     │         │ │  │
│  │  │  │ • Product Analysis │  │ • Metadata Gen     │         │ │  │
│  │  │  │ • Trend Detection  │  │                    │         │ │  │
│  │  │  │ • Forecasting      │  │                    │         │ │  │
│  │  │  └────────┬───────────┘  └──────────┬─────────┘         │ │  │
│  │  └───────────┼──────────────────────────┼───────────────────┘ │  │
│  │              │                          │                     │  │
│  │  ┌───────────▼──────────────────────────▼───────────────────┐ │  │
│  │  │              Data Processing Layer                        │ │  │
│  │  │  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐   │ │  │
│  │  │  │   Pandas    │  │    NumPy     │  │  OpenPyXL    │   │ │  │
│  │  │  │ DataFrames  │  │ Calculations │  │ Excel Reader │   │ │  │
│  │  │  └─────────────┘  └──────────────┘  └──────────────┘   │ │  │
│  │  └──────────────────────────────────────────────────────────┘ │  │
│  └───────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                                │
                    ┌───────────┴──────────┐
                    │                      │
        ┌───────────▼──────────┐  ┌────────▼─────────┐
        │  File System         │  │  Power BI        │
        │  /tmp/uploads        │  │  Desktop         │
        │  Temporary Storage   │  │  (.pbix viewer)  │
        └──────────────────────┘  └──────────────────┘
```

## Component Breakdown

### Frontend Layer

#### 1. React Components
**Location**: `/src/business-analytics-dashboard.jsx`

**Responsibilities**:
- File upload UI with drag-and-drop
- Real-time data visualization
- Interactive dashboard
- PBIX export trigger
- Loading states and error handling

**Key Features**:
- Responsive design using Tailwind CSS
- Recharts for data visualization
- Lucide React for icons
- Smooth animations and transitions

**Data Flow**:
1. User uploads file → FormData creation
2. HTTP POST to `/api/upload`
3. Receive analysis results
4. Render visualizations
5. Export button → `/api/export-pbix`
6. Download PBIX file

#### 2. Visualization Components
- **Line Charts**: Revenue trends over time
- **Bar Charts**: Product performance comparison
- **Pie Charts**: Category distribution
- **KPI Cards**: Summary metrics
- **Trend Indicators**: Growth rates and changes

### Backend Layer

#### 1. Flask API Server
**Location**: `/backend_api.py`

**Endpoints**:
```python
GET  /api/health          # Health check
POST /api/upload          # File upload and analysis
POST /api/export-pbix     # Generate PBIX file
POST /api/analyze         # Direct data analysis
```

**Responsibilities**:
- Request validation
- File handling
- Response formatting
- Error handling
- CORS management

#### 2. Business Analyzer
**Class**: `BusinessAnalyzer`

**Methods**:
```python
analyze_file(file_path, file_type)
    └─> _generate_summary(df)
    └─> _analyze_revenue(df)
    └─> _analyze_products(df)
    └─> _identify_trends(df)
    └─> _generate_forecasts(df)
```

**Features**:
- Automatic column detection
- Statistical analysis
- Time-series processing
- Aggregation and grouping
- Forecast generation

**Input Support**:
- CSV files
- Excel (.xlsx, .xls)
- JSON files

**Output Structure**:
```json
{
  "summary": {
    "total_revenue": float,
    "growth_rate": float,
    "total_transactions": int
  },
  "revenue_analysis": [...],
  "product_performance": [...],
  "trends": [...]
}
```

#### 3. PBIX Generator
**Class**: `PBIXGenerator` / `PBIXBuilder`

**Responsibilities**:
- Generate Power BI compatible data model
- Create report layouts
- Package as ZIP archive
- Add metadata and versioning

**PBIX Structure**:
```
.pbix (ZIP)
├── DataModelSchema       # JSON: Table schemas, measures, relationships
├── Report/Layout         # JSON: Visual configurations
├── DiagramLayout         # JSON: Model diagram
├── DiagramState          # JSON: UI state
├── Version               # Text: Format version
├── [Content_Types].xml   # XML: MIME types
├── Settings              # JSON: Report settings
├── SecurityBindings      # JSON: Security config
└── Metadata              # JSON: File metadata
```

**Data Model Components**:
1. **Tables**: Revenue_Analysis, Product_Performance, Summary_Metrics
2. **Columns**: Typed fields with format strings
3. **Measures**: DAX expressions for calculations
4. **Relationships**: Inter-table connections

### Data Processing Layer

#### 1. Pandas
- DataFrame manipulation
- CSV/Excel parsing
- Aggregation operations
- Time-series handling
- Data cleaning

#### 2. NumPy
- Numerical calculations
- Statistical operations
- Array operations

#### 3. OpenPyXL
- Excel file reading
- Multi-sheet support
- Cell formatting

## Data Flow Diagram

### Upload and Analysis Flow
```
User Action → File Selection
    ↓
Frontend → FormData Creation
    ↓
HTTP POST → /api/upload
    ↓
Backend → File Validation
    ↓
Backend → Save to /tmp
    ↓
BusinessAnalyzer → Load to Pandas DataFrame
    ↓
BusinessAnalyzer → Apply Analysis Methods
    ↓
Backend → Generate Analysis JSON
    ↓
HTTP Response → Analysis Results
    ↓
Frontend → Update State
    ↓
Frontend → Render Visualizations
```

### Export Flow
```
User Action → Click Export Button
    ↓
Frontend → Prepare Analysis Data
    ↓
HTTP POST → /api/export-pbix
    ↓
Backend → Validate Data
    ↓
PBIXGenerator → Create Data Model
    ↓
PBIXGenerator → Create Report Layout
    ↓
PBIXGenerator → Generate ZIP Structure
    ↓
Backend → Create In-Memory ZIP
    ↓
HTTP Response → Binary PBIX File
    ↓
Frontend → Trigger Browser Download
    ↓
User → Opens in Power BI Desktop
```

## Security Considerations

### Input Validation
- File type whitelist
- File size limits
- Content type verification
- Path traversal prevention

### API Security
- CORS configuration
- Rate limiting (recommended)
- Input sanitization
- Error message sanitization

### File Handling
- Temporary file cleanup
- Secure file paths
- No persistent storage of user data

## Scalability Considerations

### Current Architecture
- Single-threaded Flask server
- Synchronous file processing
- In-memory data handling

### Scaling Recommendations

#### Horizontal Scaling
```
Load Balancer
    ├─> Flask Instance 1
    ├─> Flask Instance 2
    └─> Flask Instance N
```

#### Async Processing
```
Frontend → API Gateway
    ↓
Task Queue (Celery/RabbitMQ)
    ↓
Worker Pool
    ↓
Results Cache (Redis)
    ↓
Frontend (polling/websocket)
```

#### Microservices Architecture
```
┌─────────────────────┐
│   API Gateway       │
└──────────┬──────────┘
           │
    ┌──────┼──────┐
    │      │      │
┌───▼──┐ ┌─▼───┐ ┌▼────┐
│Upload│ │Anal-│ │PBIX │
│Service│ │ysis │ │Serv-│
│      │ │Serv-│ │ice  │
│      │ │ice  │ │     │
└──────┘ └─────┘ └─────┘
```

## Performance Optimization

### Frontend
- Code splitting
- Lazy loading components
- Memoization (useMemo, useCallback)
- Virtual scrolling for large datasets
- Image optimization

### Backend
- DataFrame chunking for large files
- Connection pooling
- Result caching
- Async I/O operations
- Compression

### Database Integration (Future)
```
PostgreSQL/MongoDB
    ↓
Analysis Results Cache
    ↓
Historical Data
    ↓
User Preferences
```

## Monitoring and Logging

### Recommended Stack
```
Application Logs
    ↓
Structured Logging (JSON)
    ↓
Log Aggregation (ELK Stack)
    ↓
Monitoring (Prometheus/Grafana)
    ↓
Alerting (PagerDuty/Slack)
```

### Key Metrics
- Request latency
- Error rates
- File processing time
- PBIX generation time
- Memory usage
- CPU utilization

## Deployment Architecture

### Development
```
Local Machine
├─> npm run dev (Port 3000)
└─> python backend_api.py (Port 5000)
```

### Production
```
Cloud Provider (AWS/Azure/GCP)
    │
    ├─> Frontend (CDN + Static Hosting)
    │   └─> CloudFront/Azure CDN
    │
    ├─> Backend (Container Service)
    │   └─> ECS/AKS/Cloud Run
    │       ├─> Load Balancer
    │       └─> Auto Scaling Group
    │
    ├─> File Storage (Optional)
    │   └─> S3/Blob Storage
    │
    └─> Monitoring
        └─> CloudWatch/Monitor
```

## Technology Stack Summary

### Frontend
- **Framework**: React 18
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **Charts**: Recharts
- **Icons**: Lucide React
- **HTTP Client**: Axios

### Backend
- **Framework**: Flask 3.0
- **Data Processing**: Pandas 2.1
- **Numerical Computing**: NumPy 1.26
- **Excel Support**: OpenPyXL 3.1
- **CORS**: Flask-CORS 4.0

### DevOps
- **Package Manager**: npm, pip
- **Version Control**: Git
- **Containerization**: Docker (optional)
- **CI/CD**: GitHub Actions (recommended)

## API Contract

### POST /api/upload
**Request**:
```
Content-Type: multipart/form-data
Body: file=<binary>
```

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

### POST /api/export-pbix
**Request**:
```json
{
  "analysis": {
    "summary": {...},
    "revenue_analysis": [...],
    "product_performance": [...]
  }
}
```

**Response**:
```
Content-Type: application/octet-stream
Content-Disposition: attachment; filename="report.pbix"
Body: <binary PBIX file>
```

## Error Handling Strategy

### Frontend
```javascript
try {
  const response = await uploadFile(file);
  setAnalysisData(response.data);
} catch (error) {
  if (error.response?.status === 400) {
    showError('Invalid file format');
  } else if (error.response?.status === 500) {
    showError('Server error');
  } else {
    showError('Network error');
  }
}
```

### Backend
```python
@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': str(error)}), 400

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500
```

## Future Enhancements

1. **Authentication & Authorization**
   - User accounts
   - API keys
   - Role-based access control

2. **Advanced Analytics**
   - Machine learning models
   - Predictive analytics
   - Anomaly detection
   - Sentiment analysis

3. **Collaboration Features**
   - Shared dashboards
   - Real-time collaboration
   - Comments and annotations

4. **Data Sources**
   - Database connectors (SQL, NoSQL)
   - API integrations
   - Cloud storage (S3, Drive)
   - Streaming data

5. **Export Formats**
   - PDF reports
   - Excel with charts
   - CSV exports
   - API webhooks

6. **Visualization**
   - Custom chart types
   - Interactive filters
   - Drill-down capabilities
   - Geo-mapping

---

This architecture is designed for scalability, maintainability, and extensibility while providing a solid foundation for business intelligence automation.
