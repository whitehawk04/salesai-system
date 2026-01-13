#!/usr/bin/env python
"""
Demo server - runs without MongoDB
Shows the UI with mock data
"""
from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
from datetime import datetime

class DemoHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sales Performance System - Demo</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: #f8f9fa;
            color: #212529;
            line-height: 1.6;
            min-height: 100vh;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
        }
        
        header {
            margin-bottom: 48px;
            padding-bottom: 24px;
            border-bottom: 1px solid #e9ecef;
        }
        
        h1 {
            color: #212529;
            font-size: 32px;
            font-weight: 600;
            margin-bottom: 8px;
            letter-spacing: -0.5px;
        }
        
        .subtitle {
            color: #6c757d;
            font-size: 16px;
            font-weight: 400;
        }
        
        .nav {
            display: flex;
            gap: 12px;
            margin: 24px 0 0 0;
        }
        
        .nav a {
            padding: 8px 16px;
            background: #fff;
            color: #495057;
            text-decoration: none;
            border: 1px solid #dee2e6;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 500;
            transition: all 0.2s;
        }
        
        .nav a:hover {
            background: #f8f9fa;
            border-color: #adb5bd;
            color: #212529;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            margin-bottom: 32px;
        }
        
        .stat-card {
            background: #fff;
            border: 1px solid #e9ecef;
            padding: 24px;
            border-radius: 8px;
        }
        
        .stat-card h3 {
            font-size: 32px;
            font-weight: 600;
            margin-bottom: 4px;
            color: #212529;
        }
        
        .stat-card p {
            font-size: 14px;
            color: #6c757d;
            font-weight: 500;
        }
        
        h2 {
            font-size: 16px;
            font-weight: 600;
            color: #212529;
            margin-bottom: 16px;
        }
        
        .agents-grid {
            display: grid;
            gap: 16px;
        }
        
        .agent-card {
            background: #fff;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 24px;
            transition: all 0.2s;
        }
        
        .agent-card:hover {
            border-color: #dee2e6;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        }
        
        .agent-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 24px;
            padding-bottom: 16px;
            border-bottom: 1px solid #e9ecef;
        }
        
        .agent-name {
            font-size: 18px;
            font-weight: 600;
            color: #212529;
            margin-bottom: 4px;
        }
        
        .agent-id {
            font-size: 13px;
            color: #6c757d;
            font-weight: 400;
        }
        
        .risk-badge {
            padding: 4px 12px;
            border-radius: 4px;
            font-weight: 500;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .risk-HIGH {
            background: #fff5f5;
            color: #c53030;
            border: 1px solid #fc8181;
        }
        
        .risk-MEDIUM {
            background: #fffbeb;
            color: #d97706;
            border: 1px solid #fbbf24;
        }
        
        .risk-LOW {
            background: #f0fdf4;
            color: #15803d;
            border: 1px solid #86efac;
        }
        
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 12px;
            margin: 16px 0;
        }
        
        .metric {
            text-align: center;
            padding: 16px 12px;
            background: #f8f9fa;
            border-radius: 6px;
            border: 1px solid #e9ecef;
        }
        
        .metric-value {
            font-size: 24px;
            font-weight: 600;
            color: #212529;
            line-height: 1;
        }
        
        .metric-label {
            font-size: 12px;
            color: #6c757d;
            margin-top: 4px;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .progress-section {
            margin: 20px 0;
        }
        
        .progress-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }
        
        .progress-header span:first-child {
            font-size: 13px;
            font-weight: 500;
            color: #495057;
        }
        
        .progress-header span:last-child {
            font-size: 13px;
            font-weight: 600;
            color: #212529;
        }
        
        .progress-bar {
            width: 100%;
            height: 8px;
            background: #e9ecef;
            border-radius: 4px;
            overflow: hidden;
        }
        
        .progress-fill {
            height: 100%;
            background: #212529;
            transition: width 0.3s ease;
        }
        
        .progress-label {
            font-size: 13px;
            color: #495057;
            margin-top: 4px;
            font-weight: 500;
        }
        
        .prediction-box {
            background: #f8f9fa;
            padding: 16px;
            border-radius: 6px;
            margin-top: 16px;
            border: 1px solid #e9ecef;
        }
        
        .prediction-result {
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .prediction-HIT {
            color: #15803d;
        }
        
        .prediction-MISS {
            color: #c53030;
        }
        
        .prediction-info {
            font-size: 13px;
            color: #6c757d;
            margin: 4px 0;
        }
        
        footer {
            text-align: center;
            margin-top: 64px;
            padding-top: 24px;
            border-top: 1px solid #e9ecef;
            color: #6c757d;
            font-size: 14px;
        }
        
        .demo-banner {
            background: #ebf8ff;
            border: 1px solid #63b3ed;
            border-left: 3px solid #2c5282;
            padding: 16px 20px;
            border-radius: 6px;
            margin-bottom: 32px;
            font-size: 14px;
            color: #2c5282;
        }
        
        .demo-banner strong {
            font-weight: 600;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Sales Performance System</h1>
            <p class="subtitle">AI-powered sales tracking and predictions</p>
            
            <div class="nav">
                <a href="/">Dashboard</a>
                <a href="#" onclick="alert('Train model feature requires MongoDB setup'); return false;">Train Model</a>
            </div>
        </header>
        
        <div class="demo-banner">
            <strong>Demo Mode</strong> - This is a preview with mock data. Set up MongoDB to use the full system with real data.
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <h3>6</h3>
                <p>Total Agents</p>
            </div>
            <div class="stat-card">
                <h3>6</h3>
                <p>Active This Month</p>
            </div>
        </div>
        
        <h2>Agents</h2>
        <div class="agents-grid">
            <div class="agent-card">
                <div class="agent-header">
                    <div>
                        <div class="agent-name">Maria Santos</div>
                        <div class="agent-id">A101</div>
                    </div>
                    <div class="risk-badge risk-LOW">LOW</div>
                </div>
                
                <div class="metrics-grid">
                    <div class="metric">
                        <div class="metric-value">95</div>
                        <div class="metric-label">Calls</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">42</div>
                        <div class="metric-label">Meetings</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">32</div>
                        <div class="metric-label">Leads</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">18</div>
                        <div class="metric-label">Deals</div>
                    </div>
                </div>
                
                <div class="progress-section">
                    <div class="progress-header">
                        <span>Sales Progress</span>
                        <span>87%</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: 87%"></div>
                    </div>
                    <div class="progress-label">$522,000 of $600,000</div>
                </div>
                
                <div class="prediction-box">
                    <div class="prediction-result prediction-HIT">
                        <span>Prediction:</span>
                        <strong>HIT</strong>
                    </div>
                    <div class="prediction-info">Confidence: 89.2%</div>
                    <div class="prediction-info" style="margin-top: 8px;">Score: 85% • Excellent</div>
                </div>
            </div>
            
            <div class="agent-card">
                <div class="agent-header">
                    <div>
                        <div class="agent-name">John Smith</div>
                        <div class="agent-id">A102</div>
                    </div>
                    <div class="risk-badge risk-MEDIUM">MEDIUM</div>
                </div>
                
                <div class="metrics-grid">
                    <div class="metric">
                        <div class="metric-value">68</div>
                        <div class="metric-label">Calls</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">31</div>
                        <div class="metric-label">Meetings</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">22</div>
                        <div class="metric-label">Leads</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">11</div>
                        <div class="metric-label">Deals</div>
                    </div>
                </div>
                
                <div class="progress-section">
                    <div class="progress-header">
                        <span>Sales Progress</span>
                        <span>70%</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: 70%"></div>
                    </div>
                    <div class="progress-label">$385,000 of $550,000</div>
                </div>
                
                <div class="prediction-box">
                    <div class="prediction-result prediction-HIT">
                        <span>Prediction:</span>
                        <strong>HIT</strong>
                    </div>
                    <div class="prediction-info">Confidence: 62.5%</div>
                    <div class="prediction-info" style="margin-top: 8px;">Score: 71% • Good</div>
                </div>
            </div>
            
            <div class="agent-card">
                <div class="agent-header">
                    <div>
                        <div class="agent-name">Michael Chen</div>
                        <div class="agent-id">A104</div>
                    </div>
                    <div class="risk-badge risk-HIGH">HIGH</div>
                </div>
                
                <div class="metrics-grid">
                    <div class="metric">
                        <div class="metric-value">32</div>
                        <div class="metric-label">Calls</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">18</div>
                        <div class="metric-label">Meetings</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">11</div>
                        <div class="metric-label">Leads</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">5</div>
                        <div class="metric-label">Deals</div>
                    </div>
                </div>
                
                <div class="progress-section">
                    <div class="progress-header">
                        <span>Sales Progress</span>
                        <span>45%</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: 45%"></div>
                    </div>
                    <div class="progress-label">$225,000 of $500,000</div>
                </div>
                
                <div class="prediction-box">
                    <div class="prediction-result prediction-MISS">
                        <span>Prediction:</span>
                        <strong>MISS</strong>
                    </div>
                    <div class="prediction-info">Confidence: 78.3%</div>
                    <div class="prediction-info" style="margin-top: 8px;">Score: 42% • Average</div>
                </div>
            </div>
        </div>
        
        <footer>
            <p>Sales Performance System • Powered by AI</p>
        </footer>
    </div>
</body>
</html>
"""
            self.wfile.write(html.encode())
        else:
            super().do_GET()

if __name__ == '__main__':
    port = 8080
    server = HTTPServer(('localhost', port), DemoHandler)
    print("=" * 70)
    print("🎨 Demo Server - Sales Performance System")
    print("=" * 70)
    print()
    print(f"✅ Server running at: http://localhost:{port}")
    print()
    print("📊 Features:")
    print("   • See the new minimalist design")
    print("   • View mock agent data")
    print("   • Test the user interface")
    print()
    print("⚠️  Note: This is demo mode with mock data")
    print("   Set up MongoDB for the full system")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 70)
    print()
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped. Goodbye!")
