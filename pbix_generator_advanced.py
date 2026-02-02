"""
Advanced PBIX Generator Module
Handles complete Power BI file format generation with proper structure
"""

import json
import zipfile
import io
import base64
from datetime import datetime
from typing import Dict, List, Any, Optional
import xml.etree.ElementTree as ET
from xml.dom import minidom


class PowerBIDataModel:
    """
    Represents the Power BI data model structure
    Compatible with Power BI Desktop 2.0+
    """
    
    def __init__(self):
        self.tables = []
        self.relationships = []
        self.measures = []
        self.perspectives = []
        self.cultures = ["en-US"]
        self.compatibility_level = 1550  # Power BI compatible
    
    def add_table(self, name: str, columns: List[Dict], data: List[Dict] = None):
        """Add a table to the data model"""
        table = {
            "name": name,
            "columns": columns,
            "partitions": [
                {
                    "name": f"{name}_Partition",
                    "mode": "import",
                    "source": {
                        "type": "m",
                        "expression": self._generate_m_expression(name, data)
                    }
                }
            ],
            "measures": []
        }
        self.tables.append(table)
    
    def add_measure(self, table_name: str, measure_name: str, expression: str, format: str = None):
        """Add a DAX measure to a table"""
        measure = {
            "name": measure_name,
            "expression": expression,
            "formatString": format or "#,0"
        }
        
        for table in self.tables:
            if table["name"] == table_name:
                table["measures"].append(measure)
                break
    
    def add_relationship(self, from_table: str, from_column: str, to_table: str, to_column: str):
        """Add a relationship between tables"""
        relationship = {
            "name": f"{from_table}_{to_table}",
            "fromTable": from_table,
            "fromColumn": from_column,
            "toTable": to_table,
            "toColumn": to_column,
            "crossFilteringBehavior": "bothDirections"
        }
        self.relationships.append(relationship)
    
    def _generate_m_expression(self, table_name: str, data: List[Dict] = None) -> str:
        """Generate Power Query M expression for data"""
        if data:
            # Convert data to M expression
            return f'''
let
    Source = Table.FromRecords({{
        {json.dumps(data)}
    }}),
    #"Changed Type" = Table.TransformColumnTypes(Source, {{}})
in
    #"Changed Type"
'''
        else:
            return f'let Source = Table.FromRows({{}}) in Source'
    
    def to_json(self) -> str:
        """Export data model to JSON format"""
        model = {
            "name": "SemanticModel",
            "compatibilityLevel": self.compatibility_level,
            "model": {
                "culture": self.cultures[0],
                "dataAccessOptions": {
                    "legacyRedirects": True,
                    "returnErrorValuesAsNull": True
                },
                "tables": self.tables,
                "relationships": self.relationships,
                "annotations": [
                    {
                        "name": "PBI_QueryOrder",
                        "value": json.dumps([table["name"] for table in self.tables])
                    },
                    {
                        "name": "PBI_ProTooling",
                        "value": json.dumps(["DevMode"])
                    }
                ]
            }
        }
        return json.dumps(model, indent=2)


class PowerBIReport:
    """
    Represents the Power BI report layout and visualizations
    """
    
    def __init__(self, name: str = "Report"):
        self.name = name
        self.pages = []
        self.report_id = str(datetime.now().timestamp()).replace('.', '')
    
    def add_page(self, name: str, display_name: str = None):
        """Add a page to the report"""
        page = {
            "name": name,
            "displayName": display_name or name,
            "width": 1280,
            "height": 720,
            "displayOrder": len(self.pages),
            "visualContainers": [],
            "filters": "[]"
        }
        self.pages.append(page)
        return page
    
    def add_visual(self, page_name: str, visual_type: str, x: int, y: int, 
                   width: int, height: int, config: Dict):
        """Add a visual to a page"""
        visual = {
            "x": x,
            "y": y,
            "z": 0,
            "width": width,
            "height": height,
            "config": json.dumps({
                "name": config.get("name", "Visual"),
                "singleVisual": {
                    "visualType": visual_type,
                    "projections": config.get("projections", {}),
                    "prototypeQuery": config.get("query", {}),
                    "objects": config.get("objects", {})
                }
            })
        }
        
        for page in self.pages:
            if page["name"] == page_name:
                visual["z"] = len(page["visualContainers"])
                page["visualContainers"].append(visual)
                break
    
    def to_json(self) -> str:
        """Export report to JSON format"""
        report = {
            "id": self.report_id,
            "name": self.name,
            "pages": self.pages,
            "config": json.dumps({
                "theme": {
                    "name": "__default__"
                }
            }),
            "layoutOptimization": 0,
            "resourcePackages": []
        }
        return json.dumps(report, indent=2)


class PBIXBuilder:
    """
    Complete PBIX file builder with proper Power BI format
    """
    
    def __init__(self):
        self.data_model = PowerBIDataModel()
        self.report = PowerBIReport()
        self.version = "2.0"
    
    def build_from_analysis(self, analysis_data: Dict) -> bytes:
        """
        Build complete PBIX from analysis data
        """
        # Create data model tables
        self._create_revenue_table(analysis_data)
        self._create_product_table(analysis_data)
        self._create_summary_table(analysis_data)
        
        # Add measures
        self._add_measures()
        
        # Create report pages
        self._create_overview_page()
        self._create_details_page()
        
        # Generate PBIX file
        return self._generate_pbix()
    
    def _create_revenue_table(self, analysis_data: Dict):
        """Create revenue analysis table"""
        if 'revenue_analysis' in analysis_data and analysis_data['revenue_analysis']:
            columns = [
                {"name": "Period", "dataType": "string", "sourceColumn": "Period"},
                {"name": "Revenue", "dataType": "double", "sourceColumn": "Revenue", 
                 "formatString": "$#,0.00", "summarizeBy": "sum"},
                {"name": "Target", "dataType": "double", "sourceColumn": "Target",
                 "formatString": "$#,0.00", "summarizeBy": "sum"}
            ]
            
            self.data_model.add_table(
                "Revenue_Analysis",
                columns,
                analysis_data['revenue_analysis']
            )
    
    def _create_product_table(self, analysis_data: Dict):
        """Create product performance table"""
        if 'product_performance' in analysis_data and analysis_data['product_performance']:
            columns = [
                {"name": "Product", "dataType": "string", "sourceColumn": "Product"},
                {"name": "Sales", "dataType": "double", "sourceColumn": "Sales",
                 "formatString": "$#,0.00", "summarizeBy": "sum"},
                {"name": "Transactions", "dataType": "int64", "sourceColumn": "Transactions",
                 "formatString": "#,0", "summarizeBy": "sum"}
            ]
            
            self.data_model.add_table(
                "Product_Performance",
                columns,
                analysis_data['product_performance']
            )
    
    def _create_summary_table(self, analysis_data: Dict):
        """Create summary metrics table"""
        if 'summary' in analysis_data:
            summary = analysis_data['summary']
            
            # Convert summary dict to table format
            summary_data = [
                {"Metric": key, "Value": value}
                for key, value in summary.items()
                if isinstance(value, (int, float))
            ]
            
            columns = [
                {"name": "Metric", "dataType": "string", "sourceColumn": "Metric"},
                {"name": "Value", "dataType": "double", "sourceColumn": "Value",
                 "formatString": "#,0.00", "summarizeBy": "none"}
            ]
            
            self.data_model.add_table("Summary_Metrics", columns, summary_data)
    
    def _add_measures(self):
        """Add DAX measures to tables"""
        # Revenue measures
        self.data_model.add_measure(
            "Revenue_Analysis",
            "Total Revenue",
            "SUM(Revenue_Analysis[Revenue])",
            "$#,0"
        )
        
        self.data_model.add_measure(
            "Revenue_Analysis",
            "Revenue vs Target",
            "SUM(Revenue_Analysis[Revenue]) - SUM(Revenue_Analysis[Target])",
            "$#,0"
        )
        
        self.data_model.add_measure(
            "Revenue_Analysis",
            "Target Achievement %",
            "DIVIDE(SUM(Revenue_Analysis[Revenue]), SUM(Revenue_Analysis[Target]), 0) * 100",
            "0.00%"
        )
        
        # Product measures
        self.data_model.add_measure(
            "Product_Performance",
            "Total Sales",
            "SUM(Product_Performance[Sales])",
            "$#,0"
        )
        
        self.data_model.add_measure(
            "Product_Performance",
            "Average Transaction Value",
            "DIVIDE(SUM(Product_Performance[Sales]), SUM(Product_Performance[Transactions]), 0)",
            "$#,0.00"
        )
    
    def _create_overview_page(self):
        """Create overview page with key visuals"""
        page = self.report.add_page("Overview", "Executive Overview")
        
        # Add KPI cards
        self.report.add_visual(
            "Overview",
            "card",
            x=20, y=20, width=300, height=150,
            config={
                "name": "Total Revenue Card",
                "projections": {
                    "Values": [
                        {
                            "queryRef": "Revenue_Analysis.Total Revenue"
                        }
                    ]
                }
            }
        )
        
        # Add line chart for revenue trend
        self.report.add_visual(
            "Overview",
            "lineChart",
            x=20, y=200, width=600, height=400,
            config={
                "name": "Revenue Trend",
                "projections": {
                    "Category": [{"queryRef": "Revenue_Analysis.Period"}],
                    "Values": [
                        {"queryRef": "Revenue_Analysis.Revenue"},
                        {"queryRef": "Revenue_Analysis.Target"}
                    ]
                }
            }
        )
        
        # Add bar chart for products
        self.report.add_visual(
            "Overview",
            "barChart",
            x=650, y=200, width=600, height=400,
            config={
                "name": "Product Performance",
                "projections": {
                    "Category": [{"queryRef": "Product_Performance.Product"}],
                    "Values": [{"queryRef": "Product_Performance.Sales"}]
                }
            }
        )
    
    def _create_details_page(self):
        """Create detailed analysis page"""
        page = self.report.add_page("Details", "Detailed Analysis")
        
        # Add table visual
        self.report.add_visual(
            "Details",
            "tableEx",
            x=20, y=20, width=1240, height=680,
            config={
                "name": "Data Table",
                "projections": {
                    "Values": [
                        {"queryRef": "Product_Performance.Product"},
                        {"queryRef": "Product_Performance.Sales"},
                        {"queryRef": "Product_Performance.Transactions"}
                    ]
                }
            }
        )
    
    def _generate_pbix(self) -> bytes:
        """Generate the complete PBIX file"""
        memory_file = io.BytesIO()
        
        with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            # Add DataModelSchema
            zf.writestr('DataModelSchema', self.data_model.to_json())
            
            # Add Report Layout
            zf.writestr('Report/Layout', self.report.to_json())
            
            # Add DiagramLayout
            diagram_layout = self._create_diagram_layout()
            zf.writestr('DiagramLayout', diagram_layout)
            
            # Add DiagramState  
            diagram_state = self._create_diagram_state()
            zf.writestr('DiagramState', diagram_state)
            
            # Add Version
            zf.writestr('Version', self.version)
            
            # Add Content_Types.xml
            content_types = self._create_content_types_xml()
            zf.writestr('[Content_Types].xml', content_types)
            
            # Add SecurityBindings (empty)
            zf.writestr('SecurityBindings', '[]')
            
            # Add Settings
            settings = self._create_settings()
            zf.writestr('Settings', settings)
            
            # Add Metadata
            metadata = self._create_metadata()
            zf.writestr('Metadata', metadata)
        
        memory_file.seek(0)
        return memory_file.read()
    
    def _create_diagram_layout(self) -> str:
        """Create diagram layout JSON"""
        layout = {
            "version": 1,
            "diagramLayout": {
                "tables": [
                    {
                        "name": table["name"],
                        "x": 100 + (i * 250),
                        "y": 100,
                        "width": 200,
                        "height": 200
                    }
                    for i, table in enumerate(self.data_model.tables)
                ]
            }
        }
        return json.dumps(layout, indent=2)
    
    def _create_diagram_state(self) -> str:
        """Create diagram state JSON"""
        state = {
            "version": 1,
            "activeTable": self.data_model.tables[0]["name"] if self.data_model.tables else ""
        }
        return json.dumps(state, indent=2)
    
    def _create_content_types_xml(self) -> str:
        """Create Content_Types.xml"""
        xml = '''<?xml version="1.0" encoding="utf-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="json" ContentType="application/json"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/DataModelSchema" ContentType="application/json"/>
  <Override PartName="/Report/Layout" ContentType="application/json"/>
  <Override PartName="/DiagramLayout" ContentType="application/json"/>
  <Override PartName="/DiagramState" ContentType="application/json"/>
  <Override PartName="/Version" ContentType="text/plain"/>
  <Override PartName="/Settings" ContentType="application/json"/>
  <Override PartName="/Metadata" ContentType="application/json"/>
</Types>'''
        return xml
    
    def _create_settings(self) -> str:
        """Create settings JSON"""
        settings = {
            "version": "1.0",
            "settings": {
                "useEnhancedTooltips": True,
                "exportDataMode": 1
            }
        }
        return json.dumps(settings, indent=2)
    
    def _create_metadata(self) -> str:
        """Create metadata JSON"""
        metadata = {
            "version": "1.0",
            "author": "Business Analytics Automator",
            "created": datetime.now().isoformat(),
            "description": "Automatically generated business analytics report"
        }
        return json.dumps(metadata, indent=2)


# Example usage and testing
if __name__ == "__main__":
    # Sample analysis data
    sample_data = {
        "summary": {
            "total_revenue": 1000000,
            "growth_rate": 15.5,
            "total_transactions": 500
        },
        "revenue_analysis": [
            {"period": "2024-01", "revenue": 80000, "target": 75000},
            {"period": "2024-02", "revenue": 85000, "target": 80000},
            {"period": "2024-03", "revenue": 90000, "target": 85000}
        ],
        "product_performance": [
            {"product": "Product A", "sales": 50000, "transactions": 100},
            {"product": "Product B", "sales": 40000, "transactions": 80},
            {"product": "Product C", "sales": 30000, "transactions": 60}
        ]
    }
    
    # Build PBIX
    builder = PBIXBuilder()
    pbix_data = builder.build_from_analysis(sample_data)
    
    # Save to file
    with open('test_output.pbix', 'wb') as f:
        f.write(pbix_data)
    
    print("PBIX file generated successfully!")
    print(f"File size: {len(pbix_data)} bytes")
