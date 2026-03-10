# web_app.py - Professional Flask Web Application for AgentForce CRM
from flask import Flask, render_template_string, jsonify, request
from app import AgentForceCRM
import json
import os
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Initialize AgentForce CRM
crm = AgentForceCRM()

# HTML Template with Beautiful Card Design
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AgentForce CRM - AI-Powered Salesforce Automation</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 30px 20px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        /* Header Section */
        .header {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            border: 1px solid rgba(255,255,255,0.2);
            backdrop-filter: blur(10px);
        }
        
        .header h1 {
            font-size: 2.8em;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }
        
        .header h2 {
            color: #333;
            font-size: 1.4em;
            font-weight: 400;
            margin-bottom: 20px;
        }
        
        .badge-container {
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            margin: 20px 0;
        }
        
        .badge {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 8px 20px;
            border-radius: 50px;
            font-size: 0.9em;
            font-weight: 500;
            box-shadow: 0 4px 10px rgba(102, 126, 234, 0.3);
        }
        
        .badge.outline {
            background: transparent;
            border: 2px solid #667eea;
            color: #667eea;
        }
        
        /* Team Info */
        .team-info {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 20px;
            margin-top: 20px;
            padding-top: 20px;
            border-top: 2px solid #f0f0f0;
        }
        
        .team-info p {
            color: #666;
            font-size: 1.1em;
        }
        
        .team-info strong {
            color: #667eea;
            font-size: 1.2em;
        }
        
        /* Connection Status */
        .connection-status {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 15px 20px;
            background: #f8f9fa;
            border-radius: 12px;
            margin: 20px 0;
        }
        
        .status-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }
        
        .status-dot.connected {
            background: #48bb78;
            box-shadow: 0 0 0 rgba(72, 187, 120, 0.4);
        }
        
        .status-dot.disconnected {
            background: #f56565;
            box-shadow: 0 0 0 rgba(245, 101, 101, 0.4);
        }
        
        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(72, 187, 120, 0.4); }
            70% { box-shadow: 0 0 0 10px rgba(72, 187, 120, 0); }
            100% { box-shadow: 0 0 0 0 rgba(72, 187, 120, 0); }
        }
        
        /* Input Section */
        .input-section {
            background: white;
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            border: 1px solid rgba(255,255,255,0.2);
        }
        
        .input-section h3 {
            color: #333;
            font-size: 1.6em;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .input-section h3:before {
            content: "📥";
            font-size: 1.2em;
        }
        
        .input-group {
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
        }
        
        .input-group select {
            flex: 2;
            padding: 15px 20px;
            border: 2px solid #e2e8f0;
            border-radius: 12px;
            font-size: 1em;
            background: white;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .input-group select:hover {
            border-color: #667eea;
        }
        
        .input-group select:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        .btn {
            flex: 1;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 12px;
            font-size: 1.1em;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        }
        
        .btn:active {
            transform: translateY(0);
        }
        
        .btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            transform: none;
        }
        
        /* API Endpoint Badge */
        .api-badge {
            display: inline-block;
            background: #2d3748;
            color: white;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.8em;
            margin-left: 15px;
            cursor: pointer;
        }
        
        .api-badge:hover {
            background: #1a202c;
        }
        
        /* Cards Grid */
        .cards-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 25px;
            margin: 30px 0;
        }
        
        .card {
            background: white;
            border-radius: 20px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            border: 1px solid rgba(255,255,255,0.2);
            position: relative;
            overflow: hidden;
        }
        
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.15);
        }
        
        .card.planner { border-top: 5px solid #4299e1; }
        .card.retriever { border-top: 5px solid #48bb78; }
        .card.executor { border-top: 5px solid #ed8936; }
        
        .card-header {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 20px;
        }
        
        .card-icon {
            font-size: 2.5em;
        }
        
        .card-title {
            font-size: 1.6em;
            font-weight: 600;
            color: #333;
        }
        
        .card-subtitle {
            color: #666;
            font-size: 0.9em;
            margin-top: 5px;
        }
        
        .card-model {
            background: #f7fafc;
            padding: 10px 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            font-size: 0.9em;
            color: #4a5568;
            border-left: 3px solid #667eea;
        }
        
        .card-content {
            margin-bottom: 20px;
        }
        
        .metric-item {
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid #e2e8f0;
        }
        
        .metric-label {
            color: #718096;
            font-weight: 500;
        }
        
        .metric-value {
            font-weight: 600;
            color: #2d3748;
        }
        
        .confidence-high {
            color: #48bb78;
            font-weight: 600;
        }
        
        .confidence-medium {
            color: #ecc94b;
            font-weight: 600;
        }
        
        .card-footer {
            margin-top: 20px;
            padding-top: 15px;
            border-top: 2px solid #f0f0f0;
            font-size: 0.9em;
            color: #718096;
        }
        
        /* Result Section */
        .result-section {
            background: white;
            border-radius: 20px;
            padding: 30px;
            margin: 30px 0;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        
        .result-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        
        .result-header h3 {
            color: #333;
            font-size: 1.4em;
        }
        
        .json-btn {
            background: #2d3748;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 0.9em;
            transition: all 0.3s ease;
        }
        
        .json-btn:hover {
            background: #1a202c;
        }
        
        pre {
            background: #1a202c;
            color: #a0aec0;
            padding: 20px;
            border-radius: 12px;
            overflow-x: auto;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            line-height: 1.5;
            max-height: 400px;
            overflow-y: auto;
        }
        
        /* Loading Spinner */
        .spinner {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid #f3f3f3;
            border-top: 3px solid #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-right: 10px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        /* Footer */
        .footer {
            text-align: center;
            color: rgba(255,255,255,0.9);
            margin-top: 50px;
            padding: 20px;
        }
        
        .footer a {
            color: white;
            text-decoration: none;
            font-weight: 600;
        }
        
        .footer a:hover {
            text-decoration: underline;
        }
        
        /* Responsive Design */
        @media (max-width: 1024px) {
            .cards-grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }
        
        @media (max-width: 768px) {
            .cards-grid {
                grid-template-columns: 1fr;
            }
            
            .input-group {
                flex-direction: column;
            }
            
            .header h1 {
                font-size: 2em;
            }
            
            .team-info {
                flex-direction: column;
                text-align: center;
            }
        }
        
        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .card {
            animation: fadeIn 0.5s ease-out forwards;
        }
        
        .card:nth-child(1) { animation-delay: 0.1s; }
        .card:nth-child(2) { animation-delay: 0.2s; }
        .card:nth-child(3) { animation-delay: 0.3s; }
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>🤖 AgentForce CRM</h1>
            <h2>Three-Agent AI System for Automated Salesforce Data Completion</h2>
            
            <div class="badge-container">
                <span class="badge">🏆 Microsoft AI Unlocked 2026</span>
                <span class="badge">🎯 Track 4: Agent Teamwork</span>
                <span class="badge">🥇 Top 250 Team</span>
            </div>
            
            <!-- Team Information -->
            <div class="team-info">
                <div>
                    <p><strong>Shahzada Moon</strong> | Team MOON-Lab</p>
                    <p>Indian Institute of Technology Madras</p>
                </div>
                <div>
                    <p>📧 23f2002668@ds.study.iitm.ac.in</p>
                    <p>🔗 github.com/23f2002668</p>
                </div>
            </div>
            
            <!-- Salesforce Connection Status -->
            <div class="connection-status" id="connectionStatus">
                <div class="status-dot" id="statusDot"></div>
                <span id="statusText">Checking Salesforce connection...</span>
            </div>
        </div>
        
        <!-- Input Section -->
        <div class="input-section">
            <h3>Process Opportunity</h3>
            <div class="input-group">
                <select id="opportunitySelect">
                    <option value="OPP-001">OPP-001: Acme Corp - Q1 Deal (Missing: Stage, Date, Amount)</option>
                    <option value="OPP-002">OPP-002: TechCorp - Enterprise License (Complete)</option>
                    <option value="OPP-003">OPP-003: HealthInc - Implementation (Missing: Stage, Date)</option>
                    <option value="OPP-015">OPP-015: Technology Deal (Missing: Stage, Date, Amount)</option>
                </select>
                <button class="btn" onclick="processOpportunity()" id="processBtn">
                    <span class="spinner" id="spinner" style="display: none;"></span>
                    <span id="btnText">🚀 Process Opportunity</span>
                </button>
            </div>
            <div style="margin-top: 15px;">
                <span class="api-badge" onclick="window.open('/api/process/OPP-001', '_blank')">🔗 API Endpoint: /api/process/OPP-001</span>
                <span class="api-badge" onclick="window.open('/api/json', '_blank')">📋 Raw JSON Output</span>
            </div>
        </div>
        
        <!-- Agent Cards -->
        <div class="cards-grid" id="cardsGrid">
            <!-- Planner Card (Initially Hidden) -->
            <div class="card planner" id="plannerCard" style="display: none;">
                <div class="card-header">
                    <span class="card-icon">🧠</span>
                    <div>
                        <div class="card-title">Planner Agent</div>
                        <div class="card-subtitle">Strategist</div>
                    </div>
                </div>
                <div class="card-model">Phi-4-reasoning (14B parameters)</div>
                <div class="card-content" id="plannerContent">
                    <div class="metric-item">
                        <span class="metric-label">Missing Fields:</span>
                        <span class="metric-value" id="missingFields">-</span>
                    </div>
                    <div class="metric-item">
                        <span class="metric-label">Strategy:</span>
                        <span class="metric-value" id="strategy">Detecting...</span>
                    </div>
                </div>
                <div class="card-footer">
                    ⏱️ Detection complete
                </div>
            </div>
            
            <!-- Retriever Card (Initially Hidden) -->
            <div class="card retriever" id="retrieverCard" style="display: none;">
                <div class="card-header">
                    <span class="card-icon">🔍</span>
                    <div>
                        <div class="card-title">Retriever Agent</div>
                        <div class="card-subtitle">Researcher</div>
                    </div>
                </div>
                <div class="card-model">Phi-4-mini-instruct (3.8B parameters)</div>
                <div class="card-content" id="retrieverContent">
                    <div class="metric-item">
                        <span class="metric-label">Historical Deals:</span>
                        <span class="metric-value" id="historyCount">-</span>
                    </div>
                    <div class="metric-item">
                        <span class="metric-label">Similar Deals:</span>
                        <span class="metric-value" id="similarCount">-</span>
                    </div>
                    <div class="metric-item">
                        <span class="metric-label">Industry:</span>
                        <span class="metric-value" id="industry">-</span>
                    </div>
                </div>
                <div class="card-footer">
                    📊 Context retrieved
                </div>
            </div>
            
            <!-- Executor Card (Initially Hidden) -->
            <div class="card executor" id="executorCard" style="display: none;">
                <div class="card-header">
                    <span class="card-icon">⚡</span>
                    <div>
                        <div class="card-title">Executor Agent</div>
                        <div class="card-subtitle">Doer</div>
                    </div>
                </div>
                <div class="card-model">Phi-4-mini-instruct (3.8B parameters)</div>
                <div class="card-content" id="executorContent">
                    <div class="metric-item">
                        <span class="metric-label">Fields Updated:</span>
                        <span class="metric-value" id="fieldsUpdated">-</span>
                    </div>
                    <div class="metric-item">
                        <span class="metric-label">Time Saved:</span>
                        <span class="metric-value" id="timeSaved">-</span>
                    </div>
                    <div class="metric-item">
                        <span class="metric-label">Avg Confidence:</span>
                        <span class="metric-value confidence-high" id="avgConfidence">-</span>
                    </div>
                    <div class="metric-item">
                        <span class="metric-label">Salesforce Updated:</span>
                        <span class="metric-value" id="sfUpdated">-</span>
                    </div>
                </div>
                <div class="card-footer" id="updatesList">
                    
                </div>
            </div>
        </div>
        
        <!-- Results Section -->
        <div class="result-section">
            <div class="result-header">
                <h3>📋 Complete JSON Output</h3>
                <button class="json-btn" onclick="copyJSON()">📋 Copy JSON</button>
            </div>
            <pre id="result">Click "Process Opportunity" to see results...</pre>
        </div>
        
        <!-- Footer -->
        <div class="footer">
            <p>Created with ❤️ by <strong>Shahzada Moon</strong> | Team MOON-Lab | IIT Madras</p>
            <p>Microsoft AI Unlocked 2026 - Track 4: Agent Teamwork</p>
            <p>🔗 <a href="https://github.com/23f2002668" target="_blank">GitHub</a> • <a href="https://23f2002668.github.io/Portfolio" target="_blank">Portfolio</a> • 📧 23f2002668@ds.study.iitm.ac.in</p>
        </div>
    </div>
    
    <script>
        // Check connection on load
        window.onload = checkConnection;
        
        function checkConnection() {
            fetch('/api/status')
                .then(response => response.json())
                .then(data => {
                    const dot = document.getElementById('statusDot');
                    const text = document.getElementById('statusText');
                    
                    if (data.connected) {
                        dot.className = 'status-dot connected';
                        text.textContent = '✅ Connected to Salesforce • Ready to process';
                    } else {
                        dot.className = 'status-dot disconnected';
                        text.textContent = '⚠️ Using mock data • ' + data.message;
                    }
                });
        }
        
        function processOpportunity() {
            const select = document.getElementById('opportunitySelect');
            const oppId = select.value;
            const btn = document.getElementById('processBtn');
            const spinner = document.getElementById('spinner');
            const btnText = document.getElementById('btnText');
            const result = document.getElementById('result');
            
            // Hide previous cards
            document.getElementById('plannerCard').style.display = 'none';
            document.getElementById('retrieverCard').style.display = 'none';
            document.getElementById('executorCard').style.display = 'none';
            
            // Show loading state
            btn.disabled = true;
            spinner.style.display = 'inline-block';
            btnText.textContent = ' Processing...';
            result.textContent = 'Processing... 🤔';
            
            fetch('/api/process', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ opportunity_id: oppId })
            })
            .then(response => response.json())
            .then(data => {
                // Display JSON
                result.textContent = JSON.stringify(data, null, 2);
                
                // Update Planner Card
                if (data.planner) {
                    document.getElementById('plannerCard').style.display = 'block';
                    document.getElementById('missingFields').textContent = 
                        data.planner.missing_fields?.join(', ') || 'None';
                }
                
                // Update Retriever Card
                if (data.retriever) {
                    document.getElementById('retrieverCard').style.display = 'block';
                    document.getElementById('historyCount').textContent = 
                        data.retriever.account_history_count || 0;
                    document.getElementById('similarCount').textContent = 
                        data.retriever.similar_deals_count || 0;
                    document.getElementById('industry').textContent = 
                        data.retriever.industry || 'Unknown';
                }
                
                // Update Executor Card
                if (data.executor) {
                    document.getElementById('executorCard').style.display = 'block';
                    document.getElementById('fieldsUpdated').textContent = 
                        data.executor.fields_updated || 0;
                    document.getElementById('timeSaved').textContent = 
                        data.executor.time_saved?.minutes_saved + ' min' || '0 min';
                    
                    const confidence = data.executor.avg_confidence || 0;
                    const confElement = document.getElementById('avgConfidence');
                    confElement.textContent = confidence + '%';
                    confElement.className = confidence >= 90 ? 'metric-value confidence-high' : 
                                           confidence >= 80 ? 'metric-value confidence-medium' : 
                                           'metric-value';
                    
                    document.getElementById('sfUpdated').textContent = 
                        data.executor.salesforce_updated ? '✅ Yes' : '⚠️ Simulation';
                    
                    // Show updates made
                    const updatesList = document.getElementById('updatesList');
                    if (data.executor.updates_made && data.executor.updates_made.length > 0) {
                        let updates = '✅ Updates: ';
                        data.executor.updates_made.forEach(u => {
                            updates += `${u.field}=${u.value} (${u.confidence}%) `;
                        });
                        updatesList.textContent = updates;
                    }
                }
            })
            .catch(error => {
                result.textContent = 'Error: ' + error;
            })
            .finally(() => {
                btn.disabled = false;
                spinner.style.display = 'none';
                btnText.textContent = '🚀 Process Opportunity';
            });
        }
        
        function copyJSON() {
            const result = document.getElementById('result').textContent;
            navigator.clipboard.writeText(result).then(() => {
                alert('JSON copied to clipboard!');
            });
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

# API Endpoint for JSON output
@app.route('/api/json')
def api_json():
    """Return raw JSON output for the default opportunity"""
    result = crm.process_opportunity("OPP-001")
    return jsonify(result)

# API Endpoint for specific opportunity
@app.route('/api/process/<opportunity_id>')
def api_process_opportunity(opportunity_id):
    """Return JSON output for a specific opportunity"""
    result = crm.process_opportunity(opportunity_id)
    return jsonify(result)

@app.route('/api/process', methods=['POST'])
def process():
    """Process an opportunity via POST request"""
    data = request.json
    opp_id = data.get('opportunity_id', 'OPP-001')
    result = crm.process_opportunity(opp_id)
    return jsonify(result)

@app.route('/api/status')
def status():
    """Check Salesforce connection status"""
    return jsonify({
        'connected': not crm.sf.mock_mode,
        'message': 'Connected to Salesforce' if not crm.sf.mock_mode else 'Using mock data (Salesforce credentials not configured)'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
