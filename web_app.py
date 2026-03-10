from flask import Flask, render_template_string, jsonify, request
from app import AgentForceCRM
import os

app = Flask(__name__)
crm = AgentForceCRM()

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>AgentForce CRM | Shahzada Moon</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f8fafc;
            color: #0f172a;
            padding-top: 80px;  /* Space for fixed header */
            padding-bottom: 100px; /* Space for fixed footer */
            min-height: 100vh;
            position: relative;
        }
        
        /* Fixed Header - Always at top */
        header {
            background: white;
            padding: 16px 40px;
            border-bottom: 1px solid #e2e8f0;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 20px;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 1000;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }
        
        .logo-area {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .logo-icon {
            font-size: 28px;
        }
        
        .logo-text h1 {
            font-size: 20px;
            font-weight: 600;
            color: #0f172a;
        }
        
        .logo-text p {
            font-size: 13px;
            color: #64748b;
        }
        
        .badge-container {
            display: flex;
            gap: 8px;
        }
        
        .badge {
            background: #f1f5f9;
            padding: 6px 12px;
            border-radius: 30px;
            font-size: 12px;
            font-weight: 500;
            color: #334155;
        }
        
        .badge.primary {
            background: #2563eb;
            color: white;
        }
        
        /* Fixed Footer - Always at bottom */
        footer {
            background: white;
            border-top: 1px solid #e2e8f0;
            padding: 24px 40px;
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            z-index: 1000;
            box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
        }
        
        .footer-content {
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 20px;
        }
        
        .footer-left p {
            color: #64748b;
            font-size: 14px;
        }
        
        .footer-left strong {
            color: #2563eb;
        }
        
        .footer-right {
            display: flex;
            gap: 24px;
            align-items: center;
        }
        
        .footer-right a {
            color: #64748b;
            text-decoration: none;
            font-size: 14px;
            transition: color 0.2s;
        }
        
        .footer-right a:hover {
            color: #2563eb;
        }
        
        /* Main Content - Scrolls between fixed header and footer */
        .main-content {
            max-width: 1200px;
            margin: 0 auto 40px;
            padding: 0 40px;
            width: 100%;
        }
        
        /* Opportunity Selector */
        .selector-section {
            background: white;
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 30px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            border: 1px solid #e2e8f0;
        }
        
        .selector-title {
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 16px;
            color: #0f172a;
        }
        
        .selector-row {
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
        }
        
        select {
            flex: 1;
            min-width: 250px;
            padding: 12px 16px;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            font-size: 14px;
            background: white;
            cursor: pointer;
        }
        
        select:focus {
            outline: none;
            border-color: #2563eb;
        }
        
        .btn-primary {
            background: #2563eb;
            color: white;
            border: none;
            padding: 12px 28px;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .btn-primary:hover {
            background: #1d4ed8;
        }
        
        .btn-secondary {
            background: #f1f5f9;
            color: #334155;
            border: 1px solid #e2e8f0;
            padding: 12px 20px;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }
        
        .btn-secondary:hover {
            background: #e2e8f0;
        }
        
        .api-buttons {
            display: flex;
            gap: 12px;
            margin-top: 16px;
            flex-wrap: wrap;
        }
        
        /* Cards Grid */
        .cards {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 24px;
            margin: 30px 0;
        }
        
        .card {
            background: white;
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid #e2e8f0;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            transition: transform 0.2s;
        }
        
        .card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        }
        
        .card-header {
            padding: 16px 20px;
            font-weight: 600;
            font-size: 16px;
            border-bottom: 1px solid #e2e8f0;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .card-header.planner { background: #2563eb10; border-left: 3px solid #2563eb; }
        .card-header.retriever { background: #05966910; border-left: 3px solid #059669; }
        .card-header.executor { background: #ea580c10; border-left: 3px solid #ea580c; }
        
        .card-body {
            padding: 20px;
        }
        
        .metric-item {
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid #f1f5f9;
            font-size: 14px;
        }
        
        .metric-item:last-child {
            border-bottom: none;
        }
        
        .metric-label {
            color: #64748b;
        }
        
        .metric-value {
            font-weight: 600;
            color: #0f172a;
        }
        
        .updates-container {
            margin-top: 12px;
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }
        
        .update-tag {
            background: #f1f5f9;
            padding: 4px 10px;
            border-radius: 30px;
            font-size: 12px;
            font-weight: 500;
            color: #334155;
        }
        
        .update-tag.success {
            background: #05966920;
            color: #059669;
            border: 1px solid #05966940;
        }
        
        .card-footer {
            padding: 12px 20px;
            background: #f8fafc;
            border-top: 1px solid #e2e8f0;
            font-size: 12px;
            color: #64748b;
        }
        
        /* JSON Output */
        .json-section {
            background: white;
            border-radius: 12px;
            padding: 24px;
            margin: 30px 0;
            border: 1px solid #e2e8f0;
        }
        
        .json-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
        }
        
        .json-header h3 {
            font-size: 16px;
            font-weight: 600;
        }
        
        .json-output {
            background: #0f172a;
            padding: 20px;
            border-radius: 8px;
            font-family: 'Monaco', 'Menlo', monospace;
            font-size: 13px;
            line-height: 1.6;
            color: #a0aec0;
            overflow-x: auto;
            white-space: pre-wrap;
        }
        
        /* Loading */
        .spinner {
            display: inline-block;
            width: 16px;
            height: 16px;
            border: 2px solid rgba(37, 99, 235, 0.2);
            border-top-color: #2563eb;
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        .loading {
            opacity: 0.6;
            pointer-events: none;
        }
        
        /* Ensure content doesn't get hidden behind fixed elements */
        @media (max-width: 768px) {
            body {
                padding-top: 120px;  /* More space for wrapped header on mobile */
            }
        }
    </style>
</head>
<body>
    <!-- Fixed Header - Always at top of screen -->
    <header>
        <div class="logo-area">
            <span class="logo-icon">🤖</span>
            <div class="logo-text">
                <h1>AgentForce CRM</h1>
                <p>AI-Powered Salesforce Automation</p>
            </div>
        </div>
        <div class="badge-container">
            <span class="badge">🏆 Microsoft AI Unlocked 2026</span>
            <span class="badge primary">Track 4: Agent Teamwork</span>
            <span class="badge">🥇 Top 250</span>
        </div>
    </header>
    
    <!-- Scrollable Main Content -->
    <div class="main-content">
        <!-- Opportunity Selector -->
        <div class="selector-section">
            <div class="selector-title">🎯 Select Opportunity to Process</div>
            <div class="selector-row">
                <select id="opportunitySelect">
                    <option value="OPP-001">OPP-001: Acme Corp - Q1 Deal (Missing: Stage, Date, Amount)</option>
                    <option value="OPP-002">OPP-002: TechCorp - Enterprise License (Complete)</option>
                    <option value="OPP-003">OPP-003: HealthInc - Implementation (Missing: Stage, Date)</option>
                    <option value="OPP-015">OPP-015: Technology Deal (Missing: Stage, Date, Amount)</option>
                </select>
                <button class="btn-primary" onclick="runAgent()" id="processBtn">
                    <span class="spinner" id="btnSpinner" style="display: none;"></span>
                    <span id="btnText">🚀 Process</span>
                </button>
            </div>
            
            <!-- API Buttons -->
            <div class="api-buttons">
                <a href="/api/process/OPP-001" target="_blank" class="btn-secondary">🔗 /api/process/OPP-001</a>
                <a href="/api/json" target="_blank" class="btn-secondary">📋 Raw JSON Output</a>
            </div>
        </div>
        
        <!-- Cards Grid -->
        <div class="cards">
            <!-- Planner Card - Shows all 3 missing fields -->
            <div class="card">
                <div class="card-header planner">🧠 Planner · Phi-4-reasoning</div>
                <div class="card-body">
                    <div class="metric-item">
                        <span class="metric-label">StageName:</span>
                        <span class="metric-value" id="missingStage">—</span>
                    </div>
                    <div class="metric-item">
                        <span class="metric-label">CloseDate:</span>
                        <span class="metric-value" id="missingDate">—</span>
                    </div>
                    <div class="metric-item">
                        <span class="metric-label">Amount:</span>
                        <span class="metric-value" id="missingAmount">—</span>
                    </div>
                </div>
                <div class="card-footer">Detects missing fields & creates strategy</div>
            </div>
            
            <!-- Retriever Card -->
            <div class="card">
                <div class="card-header retriever">🔍 Retriever · Phi-4-mini-instruct</div>
                <div class="card-body">
                    <div class="metric-item">
                        <span class="metric-label">Historical Deals:</span>
                        <span class="metric-value" id="historyCount">—</span>
                    </div>
                    <div class="metric-item">
                        <span class="metric-label">Similar Deals:</span>
                        <span class="metric-value" id="similarCount">—</span>
                    </div>
                    <div class="metric-item">
                        <span class="metric-label">Industry:</span>
                        <span class="metric-value" id="industry">—</span>
                    </div>
                </div>
                <div class="card-footer">Fetches account history & similar deals</div>
            </div>
            
            <!-- Executor Card -->
            <div class="card">
                <div class="card-header executor">⚡ Executor · Phi-4-mini-instruct</div>
                <div class="card-body">
                    <div class="metric-item">
                        <span class="metric-label">Fields Updated:</span>
                        <span class="metric-value" id="fieldsUpdated">—</span>
                    </div>
                    <div class="metric-item">
                        <span class="metric-label">Time Saved:</span>
                        <span class="metric-value" id="timeSaved">—</span>
                    </div>
                    <div class="metric-item">
                        <span class="metric-label">Avg Confidence:</span>
                        <span class="metric-value" id="avgConfidence">—</span>
                    </div>
                    <div class="metric-item">
                        <span class="metric-label">Salesforce:</span>
                        <span class="metric-value" id="sfUpdated">—</span>
                    </div>
                    
                    <!-- Updates appear here -->
                    <div class="updates-container" id="updatesContainer"></div>
                </div>
                <div class="card-footer">Updates Salesforce & calculates time saved</div>
            </div>
        </div>
        
        <!-- JSON Output -->
        <div class="json-section">
            <div class="json-header">
                <h3>📋 Complete JSON Output</h3>
                <button class="btn-secondary" onclick="copyJSON()" style="padding: 6px 12px;">Copy</button>
            </div>
            <div class="json-output" id="jsonOutput">
                Click "Process" to see results
            </div>
        </div>
    </div>
    
    <!-- Fixed Footer - Always at bottom of screen -->
    <footer>
        <div class="footer-content">
            <div class="footer-left">
                <p>Developed by <strong>Shahzada Moon</strong> (Team MOON-Lab) · IIT Madras · Copyright 2026 | All rights reserved.</p>
            </div>
            <div class="footer-right">
                <a href="https://github.com/23f2002668" target="_blank">GitHub</a>
                <a href="https://23f2002668.github.io/Portfolio" target="_blank">Portfolio</a>
                <a href="mailto:23f2002668@ds.study.iitm.ac.in">Email</a>
            </div>
        </div>
    </footer>
    
    <script>
        async function runAgent() {
            const btn = document.getElementById('processBtn');
            const spinner = document.getElementById('btnSpinner');
            const btnText = document.getElementById('btnText');
            const select = document.getElementById('opportunitySelect');
            const oppId = select.value;
            
            // Loading state
            btn.classList.add('loading');
            spinner.style.display = 'inline-block';
            btnText.innerHTML = ' Processing...';
            
            try {
                const response = await fetch('/api/process', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({opportunity_id: oppId})
                });
                const data = await response.json();
                
                // Update JSON output
                document.getElementById('jsonOutput').innerText = JSON.stringify(data, null, 2);
                
                // Update Planner - Show each missing field individually
                if (data.planner && data.planner.missing_fields) {
                    const missingFields = data.planner.missing_fields;
                    document.getElementById('missingStage').innerText = 
                        missingFields.includes('StageName') ? '❌ Missing' : '✅ Present';
                    document.getElementById('missingDate').innerText = 
                        missingFields.includes('CloseDate') ? '❌ Missing' : '✅ Present';
                    document.getElementById('missingAmount').innerText = 
                        missingFields.includes('Amount') ? '❌ Missing' : '✅ Present';
                }
                
                // Update Retriever
                if (data.retriever) {
                    document.getElementById('historyCount').innerText = 
                        data.retriever.account_history_count || 0;
                    document.getElementById('similarCount').innerText = 
                        data.retriever.similar_deals_count || 0;
                    document.getElementById('industry').innerText = 
                        data.retriever.industry || 'Unknown';
                }
                
                // Update Executor
                if (data.executor) {
                    document.getElementById('fieldsUpdated').innerText = 
                        data.executor.fields_updated || 0;
                    document.getElementById('timeSaved').innerText = 
                        (data.executor.time_saved?.minutes_saved || 0) + ' min';
                    
                    const confidence = data.executor.avg_confidence || 0;
                    document.getElementById('avgConfidence').innerText = confidence + '%';
                    
                    document.getElementById('sfUpdated').innerText = 
                        data.executor.salesforce_updated ? '✅ Updated' : '⚠️ Simulation';
                    
                    // Show field updates as tags
                    const updatesContainer = document.getElementById('updatesContainer');
                    updatesContainer.innerHTML = '';
                    
                    if (data.executor.updates_made && data.executor.updates_made.length > 0) {
                        data.executor.updates_made.forEach(update => {
                            const tag = document.createElement('span');
                            tag.className = 'update-tag success';
                            tag.innerText = `${update.field}: ${update.value} (${update.confidence}%)`;
                            updatesContainer.appendChild(tag);
                        });
                    }
                }
            } catch (error) {
                document.getElementById('jsonOutput').innerText = '❌ Error: ' + error;
            } finally {
                btn.classList.remove('loading');
                spinner.style.display = 'none';
                btnText.innerHTML = '🚀 Process';
            }
        }
        
        function copyJSON() {
            const json = document.getElementById('jsonOutput').innerText;
            navigator.clipboard.writeText(json).then(() => {
                alert('✅ JSON copied!');
            });
        }
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/api/process/<opp>")
def process_opp(opp):
    result = crm.process_opportunity(opp)
    return jsonify(result)

@app.route("/api/process", methods=["POST"])
def process():
    data = request.json
    opp = data.get("opportunity_id", "OPP-001")
    result = crm.process_opportunity(opp)
    return jsonify(result)

@app.route("/api/json")
def json_output():
    return jsonify(crm.process_opportunity("OPP-001"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)