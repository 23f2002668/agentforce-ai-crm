# web_app.py - Flask web interface for AgentForce CRM
from flask import Flask, render_template_string, jsonify, request
from app import AgentForceCRM
import json
import os

# Initialize Flask app
app = Flask(__name__)

# Initialize AgentForce CRM
crm = AgentForceCRM()

# HTML Template (simplified version)
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>AgentForce CRM</title>
    <style>
        body { font-family: Arial; margin: 0; padding: 20px; background: #f5f5f5; }
        .header { background: linear-gradient(135deg, #0078D4, #00A1E0); color: white; padding: 20px; border-radius: 10px; }
        .metrics { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin: 20px 0; }
        .card { background: white; padding: 20px; border-radius: 10px; text-align: center; }
        .value { font-size: 2em; font-weight: bold; color: #0078D4; }
        pre { background: #f0f0f0; padding: 15px; border-radius: 5px; overflow-x: auto; }
        .btn { background: #0078D4; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🤖 AgentForce CRM</h1>
        <p>Three-Agent AI System for Salesforce Data Completion</p>
        <p>Microsoft AI Unlocked 2026 | Track 4: Agent Teamwork</p>
    </div>
    
    <div class="metrics">
        <div class="card"><div class="value" id="fields">3</div><div>Fields Updated</div></div>
        <div class="card"><div class="value" id="time">45</div><div>Minutes Saved</div></div>
        <div class="card"><div class="value" id="confidence">88%</div><div>Avg Confidence</div></div>
        <div class="card"><div class="value" id="deals">10</div><div>Similar Deals</div></div>
    </div>
    
    <h2>📊 Process Opportunity</h2>
    <input type="text" id="oppId" value="OPP-001" placeholder="Opportunity ID">
    <button class="btn" onclick="process()">Process</button>
    
    <h3>Result:</h3>
    <pre id="result">Click Process to run...</pre>
    
    <script>
        async function process() {
            const oppId = document.getElementById('oppId').value;
            document.getElementById('result').textContent = 'Processing...';
            
            const response = await fetch('/api/process', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({opportunity_id: oppId})
            });
            const result = await response.json();
            document.getElementById('result').textContent = JSON.stringify(result, null, 2);
            
            // Update metrics
            if (result.executor) {
                document.getElementById('fields').textContent = result.executor.fields_updated || 0;
                document.getElementById('time').textContent = result.executor.time_saved?.minutes_saved || 0;
                document.getElementById('confidence').textContent = (result.executor.avg_confidence || 0) + '%';
                document.getElementById('deals').textContent = result.retriever?.similar_deals_count || 0;
            }
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/process', methods=['POST'])
def process():
    data = request.json
    opp_id = data.get('opportunity_id', 'OPP-001')
    result = crm.process_opportunity(opp_id)
    return jsonify(result)

@app.route('/api/status')
def status():
    return jsonify({
        'connected': not crm.sf.mock_mode,
        'message': 'Connected to Salesforce' if not crm.sf.mock_mode else 'Using mock data'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)