"""
Business Analytics Automation - Backend API Server
Handles file upload, analysis, and PBIX export generation
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
import numpy as np
import json
import zipfile
import io
import os
from datetime import datetime
from typing import Dict, List, Any
import xml.etree.ElementTree as ET
from xml.dom import minidom

app = Flask(__name__)
CORS(app)

class BusinessAnalyzer:
    """Core business analysis engine"""
    
    def __init__(self):
        self.supported_formats = ['.csv', '.xlsx', '.xls', '.json']
    
    def analyze_file(self, file_path: str, file_type: str) -> Dict[str, Any]:
        """
        Analyzes uploaded business data file and extracts insights
        """
        try:
            # Load data based on file type
            if file_type in ['.csv']:
                df = pd.read_csv(file_path)
            elif file_type in ['.xlsx', '.xls']:
                df = pd.read_excel(file_path)
            elif file_type == '.json':
                df = pd.read_json(file_path)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
            
            # Perform comprehensive analysis
            analysis_results = {
                'summary': self._generate_summary(df),
                'revenue_analysis': self._analyze_revenue(df),
                'product_performance': self._analyze_products(df),
                'trends': self._identify_trends(df),
                'forecasts': self._generate_forecasts(df),
                'metadata': {
                    'rows': len(df),
                    'columns': len(df.columns),
                    'column_names': df.columns.tolist(),
                    'timestamp': datetime.now().isoformat()
                }
            }
            
            return analysis_results
            
        except Exception as e:
            raise Exception(f"Analysis failed: {str(e)}")
    
    def _generate_summary(self, df: pd.DataFrame) -> Dict:
        """Generate executive summary metrics"""
        summary = {}
        
        # Try to identify revenue columns
        revenue_cols = [col for col in df.columns if 'revenue' in col.lower() or 'sales' in col.lower() or 'amount' in col.lower()]
        
        if revenue_cols:
            summary['total_revenue'] = float(df[revenue_cols[0]].sum())
            summary['average_transaction'] = float(df[revenue_cols[0]].mean())
            summary['max_transaction'] = float(df[revenue_cols[0]].max())
            
            # Calculate growth rate if date column exists
            date_cols = [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower()]
            if date_cols:
                df_sorted = df.sort_values(by=date_cols[0])
                first_period = df_sorted[revenue_cols[0]].iloc[:len(df)//2].sum()
                second_period = df_sorted[revenue_cols[0]].iloc[len(df)//2:].sum()
                if first_period > 0:
                    summary['growth_rate'] = float(((second_period - first_period) / first_period) * 100)
        
        summary['total_transactions'] = len(df)
        
        return summary
    
    def _analyze_revenue(self, df: pd.DataFrame) -> List[Dict]:
        """Analyze revenue trends over time"""
        revenue_data = []
        
        date_cols = [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower()]
        revenue_cols = [col for col in df.columns if 'revenue' in col.lower() or 'sales' in col.lower()]
        
        if date_cols and revenue_cols:
            df[date_cols[0]] = pd.to_datetime(df[date_cols[0]], errors='coerce')
            df['period'] = df[date_cols[0]].dt.to_period('M')
            
            grouped = df.groupby('period')[revenue_cols[0]].sum()
            
            for period, revenue in grouped.items():
                revenue_data.append({
                    'period': str(period),
                    'revenue': float(revenue),
                    'target': float(revenue * 0.9)  # Mock target
                })
        
        return revenue_data
    
    def _analyze_products(self, df: pd.DataFrame) -> List[Dict]:
        """Analyze product performance"""
        product_data = []
        
        product_cols = [col for col in df.columns if 'product' in col.lower() or 'item' in col.lower()]
        revenue_cols = [col for col in df.columns if 'revenue' in col.lower() or 'sales' in col.lower() or 'amount' in col.lower()]
        
        if product_cols and revenue_cols:
            grouped = df.groupby(product_cols[0])[revenue_cols[0]].agg(['sum', 'count']).reset_index()
            grouped.columns = ['product', 'total_sales', 'transactions']
            
            for _, row in grouped.head(10).iterrows():
                product_data.append({
                    'product': str(row['product']),
                    'sales': float(row['total_sales']),
                    'transactions': int(row['transactions']),
                    'avg_value': float(row['total_sales'] / row['transactions'])
                })
        
        return sorted(product_data, key=lambda x: x['sales'], reverse=True)
    
    def _identify_trends(self, df: pd.DataFrame) -> List[Dict]:
        """Identify key business trends"""
        trends = []
        
        # Analyze numerical columns for trends
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols[:5]:  # Top 5 numeric columns
            if len(df[col].dropna()) > 1:
                first_half = df[col].iloc[:len(df)//2].mean()
                second_half = df[col].iloc[len(df)//2:].mean()
                
                if first_half != 0:
                    change = ((second_half - first_half) / first_half) * 100
                    trends.append({
                        'metric': col.replace('_', ' ').title(),
                        'change_percent': float(change),
                        'direction': 'up' if change > 0 else 'down',
                        'is_positive': change > 0
                    })
        
        return trends
    
    def _generate_forecasts(self, df: pd.DataFrame) -> Dict:
        """Generate simple forecasts based on historical data"""
        forecasts = {}
        
        revenue_cols = [col for col in df.columns if 'revenue' in col.lower() or 'sales' in col.lower()]
        
        if revenue_cols:
            recent_avg = df[revenue_cols[0]].tail(3).mean()
            overall_avg = df[revenue_cols[0]].mean()
            
            forecasts['next_period_estimate'] = float(recent_avg * 1.05)  # 5% growth assumption
            forecasts['confidence'] = 'medium'
        
        return forecasts


class PBIXGenerator:
    """
    Generates Power BI (.pbix) files from analysis data
    PBIX is a ZIP archive containing JSON/XML metadata and data model
    """
    
    def __init__(self):
        self.version = "2.0"
    
    def generate_pbix(self, analysis_data: Dict, output_path: str = None) -> bytes:
        """
        Creates a PBIX file structure with the analysis data
        """
        # Create in-memory ZIP file
        memory_file = io.BytesIO()
        
        with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            # Add DataModelSchema (simplified structure)
            data_model = self._create_data_model(analysis_data)
            zf.writestr('DataModelSchema', data_model)
            
            # Add Report layout
            report_layout = self._create_report_layout(analysis_data)
            zf.writestr('Report/Layout', report_layout)
            
            # Add metadata
            metadata = self._create_metadata()
            zf.writestr('[Content_Types].xml', metadata)
            
            # Add Version file
            version_content = self._create_version()
            zf.writestr('Version', version_content)
            
            # Add DiagramLayout
            diagram = self._create_diagram_layout()
            zf.writestr('DiagramLayout', diagram)
            
            # Add SecurityBindings
            security = self._create_security_bindings()
            zf.writestr('SecurityBindings', security)
        
        memory_file.seek(0)
        return memory_file.read()
    
    def _create_data_model(self, analysis_data: Dict) -> str:
        """Create the data model schema JSON"""
        
        tables = []
        
        # Revenue table
        if 'revenue_analysis' in analysis_data and analysis_data['revenue_analysis']:
            revenue_columns = [
                {"name": "Period", "dataType": "string"},
                {"name": "Revenue", "dataType": "double"},
                {"name": "Target", "dataType": "double"}
            ]
            tables.append({
                "name": "Revenue_Analysis",
                "columns": revenue_columns,
                "measures": [
                    {
                        "name": "Total Revenue",
                        "expression": "SUM(Revenue_Analysis[Revenue])"
                    }
                ]
            })
        
        # Product table
        if 'product_performance' in analysis_data and analysis_data['product_performance']:
            product_columns = [
                {"name": "Product", "dataType": "string"},
                {"name": "Sales", "dataType": "double"},
                {"name": "Transactions", "dataType": "int64"}
            ]
            tables.append({
                "name": "Product_Performance",
                "columns": product_columns,
                "measures": [
                    {
                        "name": "Total Sales",
                        "expression": "SUM(Product_Performance[Sales])"
                    }
                ]
            })
        
        # Summary table
        if 'summary' in analysis_data:
            summary_columns = [
                {"name": "Metric", "dataType": "string"},
                {"name": "Value", "dataType": "double"}
            ]
            tables.append({
                "name": "Summary_Metrics",
                "columns": summary_columns
            })
        
        data_model = {
            "name": "BusinessAnalyticsModel",
            "compatibilityLevel": 1550,
            "model": {
                "culture": "en-US",
                "tables": tables,
                "relationships": [],
                "annotations": [
                    {
                        "name": "ClientCompatibilityLevel",
                        "value": "700"
                    }
                ]
            }
        }
        
        return json.dumps(data_model, indent=2)
    
    def _create_report_layout(self, analysis_data: Dict) -> str:
        """Create the report layout JSON"""
        
        report = {
            "id": str(datetime.now().timestamp()),
            "name": "Business Analytics Report",
            "pages": [
                {
                    "name": "Overview",
                    "displayName": "Executive Overview",
                    "width": 1280,
                    "height": 720,
                    "displayOrder": 0,
                    "visualContainers": [
                        {
                            "x": 20,
                            "y": 20,
                            "z": 1,
                            "width": 300,
                            "height": 150,
                            "config": {
                                "name": "Total Revenue Card",
                                "singleVisual": {
                                    "visualType": "card",
                                    "dataRoles": [
                                        {"name": "Values", "kind": 0}
                                    ]
                                }
                            }
                        },
                        {
                            "x": 20,
                            "y": 200,
                            "z": 2,
                            "width": 600,
                            "height": 400,
                            "config": {
                                "name": "Revenue Trend",
                                "singleVisual": {
                                    "visualType": "lineChart",
                                    "dataRoles": [
                                        {"name": "Category", "kind": 0},
                                        {"name": "Values", "kind": 1}
                                    ]
                                }
                            }
                        },
                        {
                            "x": 650,
                            "y": 200,
                            "z": 3,
                            "width": 600,
                            "height": 400,
                            "config": {
                                "name": "Product Performance",
                                "singleVisual": {
                                    "visualType": "barChart",
                                    "dataRoles": [
                                        {"name": "Category", "kind": 0},
                                        {"name": "Values", "kind": 1}
                                    ]
                                }
                            }
                        }
                    ]
                }
            ],
            "config": {
                "theme": "default"
            }
        }
        
        return json.dumps(report, indent=2)
    
    def _create_metadata(self) -> str:
        """Create Content Types XML"""
        xml_content = '''<?xml version="1.0" encoding="utf-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="json" ContentType="application/json"/>
  <Override PartName="/DataModelSchema" ContentType="application/json"/>
  <Override PartName="/Report/Layout" ContentType="application/json"/>
  <Override PartName="/Version" ContentType="text/plain"/>
</Types>'''
        return xml_content
    
    def _create_version(self) -> str:
        """Create version file"""
        return "2.0"
    
    def _create_diagram_layout(self) -> str:
        """Create diagram layout JSON"""
        diagram = {
            "version": 1,
            "model": {
                "tables": []
            }
        }
        return json.dumps(diagram, indent=2)
    
    def _create_security_bindings(self) -> str:
        """Create security bindings (empty for basic reports)"""
        return json.dumps({"version": 1, "bindings": []})


# API Routes

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })


@app.route('/api/upload', methods=['POST'])
def upload_file():
    """
    Handles file upload and triggers analysis
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Validate file type
    file_ext = os.path.splitext(file.filename)[1].lower()
    analyzer = BusinessAnalyzer()
    
    if file_ext not in analyzer.supported_formats:
        return jsonify({
            'error': f'Unsupported file type. Supported formats: {", ".join(analyzer.supported_formats)}'
        }), 400
    
    try:
        # Save file temporarily
        temp_path = f'/tmp/{file.filename}'
        file.save(temp_path)
        
        # Analyze the file
        analysis_results = analyzer.analyze_file(temp_path, file_ext)
        
        # Clean up
        os.remove(temp_path)
        
        return jsonify({
            'success': True,
            'filename': file.filename,
            'analysis': analysis_results
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Analysis failed: {str(e)}'
        }), 500


@app.route('/api/export-pbix', methods=['POST'])
def export_pbix():
    """
    Generates and returns a PBIX file from analysis data
    """
    try:
        data = request.get_json()
        
        if not data or 'analysis' not in data:
            return jsonify({'error': 'No analysis data provided'}), 400
        
        analysis_data = data['analysis']
        
        # Generate PBIX file
        generator = PBIXGenerator()
        pbix_bytes = generator.generate_pbix(analysis_data)
        
        # Create response with file
        filename = f'business_analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pbix'
        
        return send_file(
            io.BytesIO(pbix_bytes),
            mimetype='application/octet-stream',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        return jsonify({
            'error': f'PBIX export failed: {str(e)}'
        }), 500


@app.route('/api/analyze', methods=['POST'])
def analyze_endpoint():
    """
    Direct analysis endpoint (for pre-loaded data)
    """
    try:
        data = request.get_json()
        
        if not data or 'data' not in data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Create temporary DataFrame from JSON
        df = pd.DataFrame(data['data'])
        
        analyzer = BusinessAnalyzer()
        
        # Run analysis methods
        results = {
            'summary': analyzer._generate_summary(df),
            'revenue_analysis': analyzer._analyze_revenue(df),
            'product_performance': analyzer._analyze_products(df),
            'trends': analyzer._identify_trends(df)
        }
        
        return jsonify({
            'success': True,
            'analysis': results
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Analysis failed: {str(e)}'
        }), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
