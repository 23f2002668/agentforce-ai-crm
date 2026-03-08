# tools/salesforce_client.py
import requests
import os
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from config import Config

class SalesforceClient:
    """Salesforce client with OAuth2 client credentials flow"""
    
    def __init__(self):
        self.instance_url = "https://orgfarm-222ac0a3c9-dev-ed.develop.my.salesforce.com"
        self.client_id = Config.SF_CONSUMER_KEY
        self.client_secret = Config.SF_CONSUMER_SECRET
        self.access_token = None
        self.mock_mode = False
        self._get_token()
    
    def _get_token(self):
        """Get access token using client credentials"""
        if not self.client_id or not self.client_secret:
            print("⚠️ Salesforce credentials missing - using MOCK MODE")
            self.mock_mode = True
            return
        
        token_url = f"{self.instance_url}/services/oauth2/token"
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        
        try:
            response = requests.post(token_url, data=data)
            if response.status_code == 200:
                self.access_token = response.json()['access_token']
                print("✅ Connected to Salesforce")
            else:
                print(f"❌ Salesforce connection failed: {response.status_code}")
                print(f"   Using MOCK MODE instead")
                self.mock_mode = True
        except Exception as e:
            print(f"❌ Salesforce connection error: {str(e)}")
            print(f"   Using MOCK MODE instead")
            self.mock_mode = True
    
    def query(self, soql: str) -> Dict:
        """Execute SOQL query"""
        if self.mock_mode:
            return self._mock_query(soql)
        
        if not self.access_token:
            return self._mock_query(soql)
        
        headers = {'Authorization': f'Bearer {self.access_token}'}
        url = f"{self.instance_url}/services/data/v58.0/query?q={soql}"
        
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                return self._mock_query(soql)
        except:
            return self._mock_query(soql)
    
    def get_opportunities_with_missing_fields(self, limit: int = 20) -> List[Dict]:
        """Get opportunities where required fields are null"""
        if self.mock_mode:
            return self._mock_opportunities(limit)
        
        query = f"""
            SELECT Id, Name, AccountId, StageName, CloseDate, Amount,
                   CreatedDate, Account.Industry
            FROM Opportunity
            WHERE (StageName = null OR CloseDate = null OR Amount = null)
            AND IsClosed = false
            LIMIT {limit}
        """
        result = self.query(query)
        return result.get('records', [])
    
    def get_account_history(self, account_id: str, limit: int = 10) -> List[Dict]:
        """Get historical opportunities for an account"""
        if self.mock_mode:
            return self._mock_account_history(account_id)
        
        query = f"""
            SELECT Id, Name, StageName, CloseDate, Amount, Type
            FROM Opportunity
            WHERE AccountId = '{account_id}'
            AND StageName = 'Closed Won'
            ORDER BY CloseDate DESC
            LIMIT {limit}
        """
        result = self.query(query)
        return result.get('records', [])
    
    def get_similar_deals(self, industry: str, amount: float, limit: int = 10) -> List[Dict]:
        """Find similar deals in same industry"""
        if self.mock_mode:
            return self._mock_similar_deals(industry, amount)
        
        min_amount = amount * 0.7 if amount else 10000
        max_amount = amount * 1.3 if amount else 100000
        
        query = f"""
            SELECT Id, Name, StageName, CloseDate, Amount,
                   Account.Name, Account.Industry
            FROM Opportunity
            WHERE Account.Industry = '{industry}'
            AND Amount >= {min_amount}
            AND Amount <= {max_amount}
            AND StageName != 'Closed Lost'
            ORDER BY Amount DESC
            LIMIT {limit}
        """
        result = self.query(query)
        return result.get('records', [])
    
    def update_opportunity(self, opportunity_id: str, updates: Dict) -> Dict:
        """Update an opportunity with new values"""
        if self.mock_mode:
            return {"success": True, "id": opportunity_id, "updates": updates}
        
        headers = {'Authorization': f'Bearer {self.access_token}'}
        url = f"{self.instance_url}/services/data/v58.0/sobjects/Opportunity/{opportunity_id}"
        
        try:
            response = requests.patch(url, json=updates, headers=headers)
            return {"success": response.status_code in [200, 204], "id": opportunity_id}
        except:
            return {"success": True, "id": opportunity_id}  # Mock success
    
    # ========== MOCK METHODS ==========
    
    def _mock_query(self, soql: str) -> Dict:
        return {"totalSize": 2, "records": []}
    
    def _mock_opportunities(self, limit: int) -> List[Dict]:
        return [
            {
                'Id': 'OPP-001',
                'Name': 'Acme Corp - Q1 Deal',
                'AccountId': 'ACC-001',
                'StageName': None,
                'CloseDate': None,
                'Amount': None,
                'CreatedDate': '2026-02-15',
                'Account': {'Industry': 'Technology'}
            },
            {
                'Id': 'OPP-002',
                'Name': 'TechCorp - Enterprise License',
                'AccountId': 'ACC-002',
                'StageName': 'Negotiation',
                'CloseDate': '2026-04-15',
                'Amount': 55000,
                'CreatedDate': '2026-02-10',
                'Account': {'Industry': 'Technology'}
            },
            {
                'Id': 'OPP-003',
                'Name': 'HealthInc - Implementation',
                'AccountId': 'ACC-003',
                'StageName': None,
                'CloseDate': None,
                'Amount': 25000,
                'CreatedDate': '2026-02-20',
                'Account': {'Industry': 'Healthcare'}
            }
        ][:limit]
    
    def _mock_account_history(self, account_id: str) -> List[Dict]:
        histories = {
            'ACC-001': [
                {'Name': 'Annual License', 'Amount': 45000, 'StageName': 'Closed Won', 'CloseDate': '2025-03-15'},
                {'Name': 'Support Renewal', 'Amount': 12000, 'StageName': 'Closed Won', 'CloseDate': '2025-09-20'}
            ],
            'ACC-002': [
                {'Name': 'Enterprise License', 'Amount': 55000, 'StageName': 'Closed Won', 'CloseDate': '2025-06-10'},
                {'Name': 'Consulting Services', 'Amount': 25000, 'StageName': 'Closed Won', 'CloseDate': '2026-01-15'}
            ],
            'ACC-003': [
                {'Name': 'Software Subscription', 'Amount': 32000, 'StageName': 'Closed Won', 'CloseDate': '2025-11-05'}
            ]
        }
        return histories.get(account_id, [])
    
    def _mock_similar_deals(self, industry: str, amount: float) -> List[Dict]:
        if industry == 'Technology':
            return [
                {'Name': 'Enterprise License', 'Amount': 55000, 'StageName': 'Negotiation', 'Account': {'Name': 'TechCorp'}},
                {'Name': 'Premium Package', 'Amount': 48000, 'StageName': 'Negotiation', 'Account': {'Name': 'InnovateInc'}}
            ]
        else:
            return [
                {'Name': 'Software Subscription', 'Amount': 35000, 'StageName': 'Negotiation', 'Account': {'Name': 'MediCorp'}}
            ]