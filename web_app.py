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

# HTML Template with Beautiful Header + Footer + Cards
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
            display: flex;
            flex-direction: column;
        }
        
        /* Header Styles */
        .app-header {
            background: rgba(255, 255, 255, 0.98);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
            position: sticky;
            top: 0;
            z-index: 1000;
            backdrop-filter: blur(10px);
            border-bottom: 1px solid rgba(102, 126, 234, 0.2);
        }
        
        .header-container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 15px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 20px;
        }
        
        .logo-area {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        
        .logo-icon {
            font-size: 2.5em;
            background: linear-gradient(135deg, #667eea, #764ba2);
            width: 50px;
            height: 50px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 12px;
            color: white;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }
        
        .logo-text h1 {
            font-size: 1.8em;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            line-height: 1.2;
        }
        
        .logo-text p {
            color: #666;
            font-size: 0.9em;
        }
        
        .header-badges {
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
        }
        
        .header-badge {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 8px 16px;
            border-radius: 50px;
            font-size: 0.85em;
            font-weight: 500;
            box-shadow: 0 4px 10px rgba(102, 126, 234, 0.2);
            display: flex;
            align-items: center;
            gap: 5px;
        }
        
        .header-badge.outline {
            background: transparent;
            border: 2px solid #667eea;
            color: #667eea;
        }
        
        .header-badge i {
            font-size: 1.1em;
        }
        
        /* Main Content */
        .main-content {
            flex: 1;
            max-width: 1400px;
            margin: 30px auto;
            padding: 0 30px;
            width: 100%;
        }
        
        /* Welcome Section */
        .welcome-section {
            background: white;
            border-radius: 20px;
            padding: 25px 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            border: 1px solid rgba(255,255,255,0.2);
        }
        
        .welcome-title {
            font-size: 1.8em;
            color: #333;
            margin-bottom: 15px;
        }
        
        .welcome-title span {
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .welcome-meta {
            display: flex;
            gap: 30px;
            flex-wrap: wrap;
            color: #666;
        }
        
        .welcome-meta-item {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .welcome-meta-item i {
            color: #667eea;
            font-weight: bold;
        }
        
        /* Connection Status Bar */
        .status-bar {
            background: white;
            border-radius: 12px;
            padding: 15px 25px;
            margin-bottom: 30px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            border-left: 5px solid #48bb78;
        }
        
        .status-left {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        
        .status-dot {
            width: 14px;
            height: 14px;
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
        
        .status-text {
            font-weight: 500;
            color: #2d3748;
        }
        
        .status-right {
            display: flex;
            gap: 15px;
        }
        
        .api-badge {
            background: #2d3748;
            color: white;
            padding: 6px 15px;
            border-radius: 30px;
            font-size: 0.85em;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 5px;
        }
        
        .api-badge:hover {
            background: #1a202c;
            transform: translateY(-2px);
        }
        
        /* Input Panel */
        .input-panel {
            background: white;
            border-radius: 20px;
            padding: 25px 30px;
            margin-bottom: 40px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.1);
            border: 1px solid rgba(102, 126, 234, 0.1);
        }
        
        .input-panel h2 {
            color: #333;
            font-size: 1.5em;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .input-panel h2:before {
            content: "🎯";
            font-size: 1.2em;
        }
        
        .input-row {
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
        }
        
        .input-row select {
            flex: 3;
            padding: 15px 20px;
            border: 2px solid #e2e8f0;
            border-radius: 12px;
            font-size: 1em;
            background: white;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .input-row select:hover {
            border-color: #667eea;
        }
        
        .input-row select:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        .btn-primary {
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
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        }
        
        .btn-primary:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            transform: none;
        }
        
        .btn-secondary {
            background: #2d3748;
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 10px;
            font-size: 1em;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .btn-secondary:hover {
            background: #1a202c;
        }
        
        /* Cards Grid */
        .cards-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 25px;
            margin: 40px 0;
        }
        
        .card {
            background: white;
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            border: 1px solid rgba(255,255,255,0.2);
            position: relative;
        }
        
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.15);
        }
        
        .card-header {
            padding: 20px;
            color: white;
        }
        
        .card-header.planner { background: linear-gradient(135deg, #4299e1, #3182ce); }
        .card-header.retriever { background: linear-gradient(135deg, #48bb78, #38a169); }
        .card-header.executor { background: linear-gradient(135deg, #ed8936, #dd6b20); }
        
        .card-header-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        
        .card-icon {
            font-size: 2.5em;
            background: rgba(255,255,255,0.2);
            width: 50px;
            height: 50px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 12px;
        }
        
        .card-model {
            background: rgba(255,255,255,0.2);
            padding: 5px 12px;
            border-radius: 30px;
            font-size: 0.8em;
            font-weight: 500;
        }
        
        .card-title {
            font-size: 1.8em;
            font-weight: 600;
            margin-bottom: 5px;
        }
        
        .card-subtitle {
            font-size: 0.9em;
            opacity: 0.9;
        }
        
        .card-body {
            padding: 20px;
        }
        
        .metric-item {
            display: flex;
            justify-content: space-between;
            padding: 12px 0;
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
            font-weight: 700;
        }
        
        .confidence-medium {
            color: #ecc94b;
            font-weight: 700;
        }
        
        .card-footer {
            padding: 15px 20px;
            background: #f7fafc;
            border-top: 1px solid #e2e8f0;
            font-size: 0.9em;
            color: #718096;
        }
        
        /* Result Section */
        .result-section {
            background: white;
            border-radius: 20px;
            padding: 25px;
            margin: 40px 0;
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
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .result-header h3:before {
            content: "📋";
        }
        
        .json-output {
            background: #1a202c;
            color: #a0aec0;
            padding: 20px;
            border-radius: 12px;
            overflow-x: auto;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            line-height: 1.6;
            max-height: 400px;
            overflow-y: auto;
            border: 1px solid #2d3748;
        }
        
        /* Spinner */
        .spinner {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(255,255,255,0.3);
            border-top: 3px solid white;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        /* Footer */
        .app-footer {
            background: rgba(255, 255, 255, 0.98);
            border-top: 1px solid rgba(102, 126, 234, 0.2);
            margin-top: 50px;
            backdrop-filter: blur(10px);
        }
        
        .footer-container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 30px;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 30px;
        }
        
        .footer-section h4 {
            color: #333;
            font-size: 1.1em;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .footer-section p {
            color: #666;
            line-height: 1.6;
            margin-bottom: 10px;
        }
        
        .footer-links {
            list-style: none;
        }
        
        .footer-links li {
            margin-bottom: 10px;
        }
        
        .footer-links a {
            color: #667eea;
            text-decoration: none;
            transition: all 0.3s ease;
        }
        
        .footer-links a:hover {
            color: #764ba2;
            text-decoration: underline;
        }
        
        .social-links {
            display: flex;
            gap: 15px;
            margin-top: 15px;
        }
        
        .social-link {
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            text-decoration: none;
            transition: all 0.3s ease;
        }
        
        .social-link:hover {
            transform: translateY(-3px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        .footer-bottom {
            text-align: center;
            padding: 20px;
            border-top: 1px solid rgba(102, 126, 234, 0.1);
            color: #666;
            font-size: 0.9em;
        }
        
        .footer-bottom strong {
            color: #667eea;
        }
        
        /* Animations */
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .card {
            animation: fadeInUp 0.5s ease-out forwards;
        }
        
        .card:nth-child(1) { animation-delay: 0.1s; }
        .card:nth-child(2) { animation-delay: 0.2s; }
        .card:nth-child(3) { animation-delay: 0.3s; }
        
        /* Responsive Design */
        @media (max-width: 1024px) {
            .cards-grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }
        
        @media (max-width: 768px) {
            .header-container {
                flex-direction: column;
                text-align: center;
            }
            
            .logo-area {
                flex-direction: column;
            }
            
            .cards-grid {
                grid-template-columns: 1fr;
            }
            
            .input-row {
                flex-direction: column;
            }
            
            .status-bar {
                flex-direction: column;
                align-items: flex-start;
            }
            
            .footer-container {
                grid-template-columns: 1fr;
                text-align: center;
            }
            
            .social-links {
                justify-content: center;
            }
        }
    </style>
</head>
<body>
    <!-- Header -->
    <header class="app-header">
        <div class="header-container">
            <div class="logo-area">
                <div class="logo-icon">🤖</div>
                <div class="logo-text">
                    <h1>AgentForce CRM</h1>
                    <p>AI-Powered Salesforce Automation</p>
                </div>
            </div>
            <div class="header-badges">
                <span class="header-badge">🏆 Microsoft AI Unlocked 2026</span>
                <span class="header-badge">🎯 Track 4: Agent Teamwork</span>
                <span class="header-badge outline">🥇 Top 250 Team</span>
            </div>
        </div>
    </header>
    
    <!-- Main Content -->
    <main class="main-content">
        <!-- Welcome Section -->
        <div class="welcome-section">
            <h1 class="welcome-title">Welcome to <span>AgentForce CRM</span></h1>
            <p style="color: #666; margin-bottom: 20px; font-size: 1.1em;">Three specialized AI agents working in harmony to automatically complete missing Salesforce fields.</p>
            <div class="welcome-meta">
                <div class="welcome-meta-item"><i>👤</i> <strong>Shahzada Moon</strong> | Team MOON-Lab</div>
                <div class="welcome-meta-item"><i>🎓</i> Indian Institute of Technology Madras</div>
                <div class="welcome-meta-item"><i>📧</i> 23f2002668@ds.study.iitm.ac.in</div>
                <div class="welcome-meta-item"><i>🔗</i> github.com/23f2002668</div>
            </div>
        </div>
        
        <!-- Connection Status Bar -->
        <div class="status-bar" id="connectionStatus">
            <div class="status-left">
                <div class="status-dot" id="statusDot"></div>
                <span class="status-text" id="statusText">Checking Salesforce connection...</span>
            </div>
            <div class="status-right">
                <span class="api-badge" onclick="window.open('/api/process/OPP-001', '_blank')">
                    <span>🔗</span> API: /api/process/OPP-001
                </span>
                <span class="api-badge" onclick="window.open('/api/json', '_blank')">
                    <span>📋</span> Raw JSON Output
                </span>
            </div>
        </div>
        
        <!-- Input Panel -->
        <div class="input-panel">
            <h2>Process Opportunity</h2>
            <div class="input-row">
                <select id="opportunitySelect">
                    <option value="OPP-001">OPP-001: Acme Corp - Q1 Deal (Missing: Stage, Date, Amount)</option>
                    <option value="OPP-002">OPP-002: TechCorp - Enterprise License (Complete)</option>
                    <option value="OPP-003">OPP-003: HealthInc - Implementation (Missing: Stage, Date)</option>
                    <option value="OPP-015">OPP-015: Technology Deal (Missing: Stage, Date, Amount)</option>
                </select>
                <button class="btn-primary" onclick="processOpportunity()" id="processBtn">
                    <span class="spinner" id="spinner" style="display: none;"></span>
                    <span id="btnText">🚀 Process Opportunity</span>
                </button>
            </div>
        </div>
        
        <!-- Agent Cards Grid -->
        <div class="cards-grid" id="cardsGrid">
            <!-- Planner Card -->
            <div class="card" id="plannerCard" style="display: none;">
                <div class="card-header planner">
                    <div class="card-header-top">
                        <span class="card-icon">🧠</span>
                        <span class="card-model">Phi-4-reasoning</span>
                    </div>
                    <div class="card-title">Planner</div>
                    <div class="card-subtitle">Strategist Agent</div>
                </div>
                <div class="card-body" id="plannerContent">
                    <div class="metric-item">
                        <span class="metric-label">Missing Fields:</span>
                        <span class="metric-value" id="missingFields">-</span>
                    </div>
                    <div class="metric-item">
                        <span class="metric-label">Strategy:</span>
                        <span class="metric-value" id="strategy">Analyzing...</span>
                    </div>
                </div>
                <div class="card-footer">
                    ⏱️ Detection complete • 14B parameters
                </div>
            </div>
            
            <!-- Retriever Card -->
            <div class="card" id="retrieverCard" style="display: none;">
                <div class="card-header retriever">
                    <div class="card-header-top">
                        <span class="card-icon">🔍</span>
                        <span class="card-model">Phi-4-mini-instruct</span>
                    </div>
                    <div class="card-title">Retriever</div>
                    <div class="card-subtitle">Researcher Agent</div>
                </div>
                <div class="card-body" id="retrieverContent">
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
                    📊 Context retrieved • 128K context window
                </div>
            </div>
            
            <!-- Executor Card -->
            <div class="card" id="executorCard" style="display: none;">
                <div class="card-header executor">
                    <div class="card-header-top">
                        <span class="card-icon">⚡</span>
                        <span class="card-model">Phi-4-mini-instruct</span>
                    </div>
                    <div class="card-title">Executor</div>
                    <div class="card-subtitle">Action Agent</div>
                </div>
                <div class="card-body" id="executorContent">
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
                        <span class="metric-value" id="avgConfidence">-</span>
                    </div>
                    <div class="metric-item">
                        <span class="metric-label">Salesforce:</span>
                        <span class="metric-value" id="sfUpdated">-</span>
                    </div>
                </div>
                <div class="card-footer" id="updatesList">
                    ⏱️ 15 min per field • Real-time updates
                </div>
            </div>
        </div>
        
        <!-- Results Section -->
        <div class="result-section">
            <div class="result-header">
                <h3>Complete JSON Output</h3>
                <button class="btn-secondary" onclick="copyJSON()">
                    <span>📋</span> Copy JSON
                </button>
            </div>
            <div class="json-output" id="result">
                Click "Process Opportunity" to see results...
            </div>
        </div>
    </main>
    
    <!-- Footer -->
    <footer class="app-footer">
        <div class="footer-container">
            <div class="footer-section">
                <h4><span>🤖</span> AgentForce CRM</h4>
                <p>Three-Agent AI System for Automated Salesforce Data Completion</p>
                <p>Microsoft AI Unlocked 2026 • Track 4: Agent Teamwork</p>
            </div>
            <div class="footer-section">
                <h4><span>👤</span> Developer</h4>
                <p><strong>Shahzada Moon</strong></p>
                <p>IIT Madras • Data Science</p>
                <p>AKTU • Computer Science</p>
            </div>
            <div class="footer-section">
                <h4><span>🔗</span> Links</h4>
                <ul class="footer-links">
                    <li><a href="https://github.com/23f2002668" target="_blank">GitHub</a></li>
                    <li><a href="https://23f2002668.github.io/Portfolio" target="_blank">Portfolio</a></li>
                    <li><a href="https://microsoft.acehacker.com/aiunlocked/" target="_blank">Microsoft AI Unlocked</a></li>
                </ul>
            </div>
            <div class="footer-section">
                <h4><span>📬</span> Contact</h4>
                <p>📧 23f2002668@ds.study.iitm.ac.in</p>
                <p>📱 +91 8126524809</p>
                <p>📍 Ghaziabad, India</p>
                <div class="social-links">
                    <a href="https://github.com/23f2002668" class="social-link" target="_blank">G</a>
                    <a href="#" class="social-link">L</a>
                    <a href="#" class="social-link">X</a>
                </div>
            </div>
        </div>
        <div class="footer-bottom">
            <p>© 2026 <strong>Shahzada Moon</strong> | Team MOON-Lab | Built with ❤️ using Microsoft Azure AI + Salesforce</p>
        </div>
    </footer>
    
    <script>
        // Check connection on load
        window.onload = function() {
            checkConnection();
            // Hide cards initially
            document.getElementById('plannerCard').style.display = 'none';
            document.getElementById('retrieverCard').style.display = 'none';
            document.getElementById('executorCard').style.display = 'none';
        };
        
        function checkConnection() {
            fetch('/api/status')
                .then(response => response.json())
                .then(data => {
                    const dot = document.getElementById('statusDot');
                    const text = document.getElementById('statusText');
                    
                    if (data.connected) {
                        dot.className = 'status-dot connected';
                        text.textContent = '✅ Connected to Salesforce • Ready to process opportunities';
                    } else {
                        dot.className = 'status-dot disconnected';
                        text.textContent = '⚠️ Using mock data • ' + data.message;
                    }
                })
                .catch(error => {
                    document.getElementById('statusText').textContent = '⚠️ Connection error - using mock data';
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
            btnText.innerHTML = ' Processing...';
            result.textContent = '⏳ Processing opportunity ' + oppId + '...';
            
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
                        (data.executor.time_saved?.minutes_saved || 0) + ' min';
                    
                    const confidence = data.executor.avg_confidence || 0;
                    const confElement = document.getElementById('avgConfidence');
                    confElement.textContent = confidence + '%';
                    confElement.className = confidence >= 90 ? 'metric-value confidence-high' : 
                                           confidence >= 80 ? 'metric-value confidence-medium' : 
                                           'metric-value';
                    
                    document.getElementById('sfUpdated').textContent = 
                        data.executor.salesforce_updated ? '✅ Updated' : '⚠️ Simulation';
                    
                    // Show updates made in footer
                    const updatesList = document.getElementById('updatesList');
                    if (data.executor.updates_made && data.executor.updates_made.length > 0) {
                        let updates = '✅ ';
                        data.executor.updates_made.forEach((u, i) => {
                            updates += `${u.field}=${u.value} (${u.confidence}%)${i < data.executor.updates_made.length-1 ? ' • ' : ''}`;
                        });
                        updatesList.textContent = updates;
                    }
                }
            })
            .catch(error => {
                result.textContent = '❌ Error: ' + error;
            })
            .finally(() => {
                btn.disabled = false;
                spinner.style.display = 'none';
                btnText.innerHTML = '🚀 Process Opportunity';
            });
        }
        
        function copyJSON() {
            const result = document.getElementById('result').textContent;
            navigator.clipboard.writeText(result).then(() => {
                alert('✅ JSON copied to clipboard!');
            }).catch(() => {
                alert('❌ Failed to copy. Please select and copy manually.');
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
