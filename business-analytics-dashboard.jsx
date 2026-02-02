import React, { useState, useEffect } from 'react';
import { BarChart3, FileText, Download, Upload, TrendingUp, AlertCircle, CheckCircle, Loader } from 'lucide-react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

export default function BusinessAnalyticsDashboard() {
  const [file, setFile] = useState(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [analysisComplete, setAnalysisComplete] = useState(false);
  const [analysisData, setAnalysisData] = useState(null);
  const [exportStatus, setExportStatus] = useState('');
  
  // Simulated analysis data structure
  const [dashboardData, setDashboardData] = useState({
    summary: {
      totalRevenue: 0,
      growthRate: 0,
      topProduct: '',
      totalTransactions: 0
    },
    revenueData: [],
    productPerformance: [],
    categoryDistribution: [],
    trends: []
  });

  const handleFileUpload = (event) => {
    const uploadedFile = event.target.files[0];
    if (uploadedFile) {
      setFile(uploadedFile);
      setAnalysisComplete(false);
      performAnalysis(uploadedFile);
    }
  };

  const performAnalysis = async (uploadedFile) => {
    setAnalyzing(true);
    setExportStatus('');
    
    // Simulate file parsing and analysis
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // Generate simulated analysis results
    const mockData = {
      summary: {
        totalRevenue: 2847523,
        growthRate: 18.5,
        topProduct: 'Enterprise SaaS License',
        totalTransactions: 3421
      },
      revenueData: [
        { month: 'Jan', revenue: 245000, target: 220000 },
        { month: 'Feb', revenue: 268000, target: 240000 },
        { month: 'Mar', revenue: 292000, target: 260000 },
        { month: 'Apr', revenue: 315000, target: 280000 },
        { month: 'May', revenue: 338000, target: 300000 },
        { month: 'Jun', revenue: 365000, target: 320000 }
      ],
      productPerformance: [
        { product: 'SaaS License', sales: 145000, margin: 68 },
        { product: 'Consulting', sales: 98000, margin: 45 },
        { product: 'Support', sales: 76000, margin: 72 },
        { product: 'Training', sales: 54000, margin: 58 },
        { product: 'Integration', sales: 42000, margin: 52 }
      ],
      categoryDistribution: [
        { name: 'Software', value: 45, color: '#6366f1' },
        { name: 'Services', value: 30, color: '#8b5cf6' },
        { name: 'Support', value: 15, color: '#ec4899' },
        { name: 'Other', value: 10, color: '#f59e0b' }
      ],
      trends: [
        { metric: 'Customer Acquisition Cost', change: -12.3, positive: true },
        { metric: 'Churn Rate', change: -2.1, positive: true },
        { metric: 'Average Deal Size', change: 24.7, positive: true },
        { metric: 'Sales Cycle Length', change: 8.4, positive: false }
      ]
    };
    
    setDashboardData(mockData);
    setAnalysisData(mockData);
    setAnalyzing(false);
    setAnalysisComplete(true);
  };

  const exportToPBIX = async () => {
    setExportStatus('preparing');
    
    // Simulate PBIX generation process
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    try {
      // In production, this would call your backend API
      // const response = await fetch('/api/export-pbix', {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify({ data: analysisData })
      // });
      
      // For now, create a mock download
      const pbixContent = generatePBIXStructure(analysisData);
      const blob = new Blob([pbixContent], { type: 'application/octet-stream' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `business-analysis-${new Date().getTime()}.pbix`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
      
      setExportStatus('success');
      setTimeout(() => setExportStatus(''), 3000);
    } catch (error) {
      setExportStatus('error');
      setTimeout(() => setExportStatus(''), 3000);
    }
  };

  const generatePBIXStructure = (data) => {
    // In production, this would generate actual PBIX format
    // PBIX is essentially a ZIP file containing DataModelSchema, Report, and metadata
    const pbixMock = JSON.stringify({
      version: "1.0",
      dataModel: {
        tables: [
          {
            name: "Revenue",
            columns: data.revenueData.map(item => ({
              month: item.month,
              revenue: item.revenue,
              target: item.target
            }))
          },
          {
            name: "Products",
            columns: data.productPerformance
          }
        ]
      },
      report: {
        pages: [
          {
            name: "Overview",
            visuals: [
              { type: "card", field: "totalRevenue" },
              { type: "lineChart", data: "Revenue" },
              { type: "barChart", data: "Products" }
            ]
          }
        ]
      }
    }, null, 2);
    
    return pbixMock;
  };

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0
    }).format(value);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-purple-950 to-slate-900">
      {/* Animated background elements */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-indigo-500/10 rounded-full blur-3xl animate-pulse" style={{animationDelay: '1s'}}></div>
      </div>

      <div className="relative z-10 p-8">
        {/* Header */}
        <div className="mb-12">
          <div className="flex items-center gap-4 mb-4">
            <div className="p-3 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl shadow-lg shadow-purple-500/50">
              <BarChart3 className="w-8 h-8 text-white" />
            </div>
            <div>
              <h1 className="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-white to-purple-200">
                Business Analytics Automator
              </h1>
              <p className="text-purple-300 text-sm mt-1">Upload, Analyze, Export to Power BI</p>
            </div>
          </div>
        </div>

        {/* File Upload Section */}
        <div className="max-w-7xl mx-auto mb-8">
          <div className="bg-slate-900/50 backdrop-blur-xl border-2 border-purple-500/30 rounded-2xl p-8 shadow-2xl">
            <label className="flex flex-col items-center justify-center cursor-pointer group">
              <input
                type="file"
                className="hidden"
                accept=".csv,.xlsx,.xls,.json"
                onChange={handleFileUpload}
              />
              <div className="flex flex-col items-center gap-4 group-hover:scale-105 transition-transform duration-300">
                <div className="p-6 bg-gradient-to-br from-purple-600/20 to-indigo-600/20 rounded-full border-2 border-purple-400/50 group-hover:border-purple-400 transition-colors">
                  <Upload className="w-12 h-12 text-purple-300 group-hover:text-purple-200 transition-colors" />
                </div>
                <div className="text-center">
                  <p className="text-xl font-semibold text-white mb-2">
                    {file ? file.name : 'Drop your business data file here'}
                  </p>
                  <p className="text-purple-300 text-sm">
                    Supports CSV, Excel, JSON formats
                  </p>
                </div>
              </div>
            </label>

            {analyzing && (
              <div className="mt-6 flex items-center justify-center gap-3">
                <Loader className="w-6 h-6 text-purple-400 animate-spin" />
                <span className="text-purple-300">Analyzing your data...</span>
              </div>
            )}
          </div>
        </div>

        {/* Analytics Dashboard */}
        {analysisComplete && (
          <div className="max-w-7xl mx-auto space-y-8 animate-fadeIn">
            {/* Summary Cards */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              <div className="bg-gradient-to-br from-indigo-900/50 to-purple-900/50 backdrop-blur-xl border border-indigo-500/30 rounded-2xl p-6 shadow-xl">
                <div className="flex items-center justify-between mb-3">
                  <span className="text-indigo-300 text-sm font-medium">Total Revenue</span>
                  <TrendingUp className="w-5 h-5 text-green-400" />
                </div>
                <p className="text-3xl font-bold text-white mb-1">
                  {formatCurrency(dashboardData.summary.totalRevenue)}
                </p>
                <p className="text-green-400 text-sm">↑ {dashboardData.summary.growthRate}% growth</p>
              </div>

              <div className="bg-gradient-to-br from-purple-900/50 to-pink-900/50 backdrop-blur-xl border border-purple-500/30 rounded-2xl p-6 shadow-xl">
                <div className="flex items-center justify-between mb-3">
                  <span className="text-purple-300 text-sm font-medium">Transactions</span>
                  <FileText className="w-5 h-5 text-purple-400" />
                </div>
                <p className="text-3xl font-bold text-white mb-1">
                  {dashboardData.summary.totalTransactions.toLocaleString()}
                </p>
                <p className="text-purple-300 text-sm">Total processed</p>
              </div>

              <div className="bg-gradient-to-br from-pink-900/50 to-rose-900/50 backdrop-blur-xl border border-pink-500/30 rounded-2xl p-6 shadow-xl">
                <div className="flex items-center justify-between mb-3">
                  <span className="text-pink-300 text-sm font-medium">Top Product</span>
                  <BarChart3 className="w-5 h-5 text-pink-400" />
                </div>
                <p className="text-xl font-bold text-white mb-1">
                  {dashboardData.summary.topProduct}
                </p>
                <p className="text-pink-300 text-sm">Best performer</p>
              </div>

              <div className="bg-gradient-to-br from-violet-900/50 to-indigo-900/50 backdrop-blur-xl border border-violet-500/30 rounded-2xl p-6 shadow-xl">
                <button
                  onClick={exportToPBIX}
                  disabled={exportStatus === 'preparing'}
                  className="w-full h-full flex flex-col items-center justify-center gap-3 hover:scale-105 transition-transform duration-200 disabled:opacity-50"
                >
                  {exportStatus === 'preparing' ? (
                    <>
                      <Loader className="w-8 h-8 text-violet-300 animate-spin" />
                      <span className="text-violet-300 text-sm font-medium">Preparing PBIX...</span>
                    </>
                  ) : exportStatus === 'success' ? (
                    <>
                      <CheckCircle className="w-8 h-8 text-green-400" />
                      <span className="text-green-400 text-sm font-medium">Export Successful!</span>
                    </>
                  ) : exportStatus === 'error' ? (
                    <>
                      <AlertCircle className="w-8 h-8 text-red-400" />
                      <span className="text-red-400 text-sm font-medium">Export Failed</span>
                    </>
                  ) : (
                    <>
                      <Download className="w-8 h-8 text-violet-300" />
                      <span className="text-white text-lg font-semibold">Export to PBIX</span>
                      <span className="text-violet-300 text-xs">Power BI Desktop</span>
                    </>
                  )}
                </button>
              </div>
            </div>

            {/* Charts Row 1 */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Revenue Trend */}
              <div className="bg-slate-900/50 backdrop-blur-xl border border-purple-500/20 rounded-2xl p-6 shadow-xl">
                <h3 className="text-xl font-bold text-white mb-6 flex items-center gap-2">
                  <TrendingUp className="w-5 h-5 text-purple-400" />
                  Revenue Trend vs Target
                </h3>
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={dashboardData.revenueData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                    <XAxis dataKey="month" stroke="#9ca3af" />
                    <YAxis stroke="#9ca3af" />
                    <Tooltip 
                      contentStyle={{ 
                        backgroundColor: '#1e1b4b', 
                        border: '1px solid #6366f1',
                        borderRadius: '8px'
                      }} 
                    />
                    <Legend />
                    <Line 
                      type="monotone" 
                      dataKey="revenue" 
                      stroke="#8b5cf6" 
                      strokeWidth={3}
                      dot={{ fill: '#8b5cf6', r: 5 }}
                    />
                    <Line 
                      type="monotone" 
                      dataKey="target" 
                      stroke="#6366f1" 
                      strokeWidth={2}
                      strokeDasharray="5 5"
                      dot={{ fill: '#6366f1', r: 4 }}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>

              {/* Product Performance */}
              <div className="bg-slate-900/50 backdrop-blur-xl border border-purple-500/20 rounded-2xl p-6 shadow-xl">
                <h3 className="text-xl font-bold text-white mb-6 flex items-center gap-2">
                  <BarChart3 className="w-5 h-5 text-purple-400" />
                  Product Performance
                </h3>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={dashboardData.productPerformance}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                    <XAxis dataKey="product" stroke="#9ca3af" angle={-15} textAnchor="end" height={80} />
                    <YAxis stroke="#9ca3af" />
                    <Tooltip 
                      contentStyle={{ 
                        backgroundColor: '#1e1b4b', 
                        border: '1px solid #6366f1',
                        borderRadius: '8px'
                      }} 
                    />
                    <Bar dataKey="sales" fill="#8b5cf6" radius={[8, 8, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Charts Row 2 */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Category Distribution */}
              <div className="bg-slate-900/50 backdrop-blur-xl border border-purple-500/20 rounded-2xl p-6 shadow-xl">
                <h3 className="text-xl font-bold text-white mb-6">Category Distribution</h3>
                <ResponsiveContainer width="100%" height={250}>
                  <PieChart>
                    <Pie
                      data={dashboardData.categoryDistribution}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {dashboardData.categoryDistribution.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </div>

              {/* Key Trends */}
              <div className="lg:col-span-2 bg-slate-900/50 backdrop-blur-xl border border-purple-500/20 rounded-2xl p-6 shadow-xl">
                <h3 className="text-xl font-bold text-white mb-6">Key Performance Indicators</h3>
                <div className="space-y-4">
                  {dashboardData.trends.map((trend, index) => (
                    <div key={index} className="flex items-center justify-between p-4 bg-slate-800/50 rounded-xl border border-slate-700/50">
                      <span className="text-purple-200 font-medium">{trend.metric}</span>
                      <div className="flex items-center gap-2">
                        <span className={`text-lg font-bold ${trend.positive ? 'text-green-400' : 'text-red-400'}`}>
                          {trend.positive ? '↑' : '↓'} {Math.abs(trend.change)}%
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      <style jsx>{`
        @keyframes fadeIn {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        
        .animate-fadeIn {
          animation: fadeIn 0.8s ease-out;
        }
      `}</style>
    </div>
  );
}
