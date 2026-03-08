# agents/planner.py
import json
from typing import Dict, List, Any, Optional
from config import Config
from tools.salesforce_client import SalesforceClient

try:
    from openai import AzureOpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("⚠️ openai not installed. Run: pip install openai")

class PlannerAgent:
    def __init__(self, salesforce_client: Optional[SalesforceClient] = None):
        print("  Initializing Planner Agent...")
        self.model = Config.PLANNER_MODEL
        self.sf = salesforce_client or SalesforceClient()
        self.use_real_llm = False
        
        if OPENAI_AVAILABLE and Config.ENDPOINT and Config.API_KEY:
            try:
                self.client = AzureOpenAI(
                    azure_endpoint=Config.ENDPOINT,
                    api_key=Config.API_KEY,
                    api_version="2024-12-01-preview"
                )
                self.use_real_llm = True
                print("  ✅ Using REAL Azure OpenAI")
            except Exception as e:
                print(f"  ⚠️ Azure OpenAI init failed: {str(e)[:50]}...")
    
    def analyze_opportunity(self, opportunity_id: str) -> Dict[str, Any]:
        print(f"\n🤔 PLANNER: Analyzing opportunity {opportunity_id}...")
        
        opportunities = self.sf.get_opportunities_with_missing_fields(10)
        opportunity = next((o for o in opportunities if o['Id'] == opportunity_id), None)
        
        if not opportunity:
            opportunity = {
                'Id': opportunity_id,
                'Name': f'Opportunity {opportunity_id}',
                'AccountId': 'ACC-001',
                'StageName': None,
                'CloseDate': None,
                'Amount': None,
                'CreatedDate': '2026-02-15'
            }
        
        missing_fields = []
        if not opportunity.get('StageName'):
            missing_fields.append('StageName')
        if not opportunity.get('CloseDate'):
            missing_fields.append('CloseDate')
        if not opportunity.get('Amount'):
            missing_fields.append('Amount')
        
        if not missing_fields:
            return {
                "opportunity_id": opportunity_id,
                "missing_fields": [],
                "message": "No missing fields found",
                "original_opportunity": opportunity
            }
        
        # Always use fallback plan (simulation mode)
        plan = self._fallback_plan(missing_fields, opportunity)
        
        result = {
            "opportunity_id": opportunity_id,
            "missing_fields": missing_fields,
            "plan": plan,
            "original_opportunity": opportunity,
            "status": "success"
        }
        
        print(f"  ✅ Planner detected {len(missing_fields)} missing fields: {', '.join(missing_fields)}")
        return result
    
    def _fallback_plan(self, missing_fields: List[str], opportunity: Dict) -> Dict:
        plan = {}
        for field in missing_fields:
            if field == 'StageName':
                plan[field] = "Check similar deals in same industry"
            elif field == 'CloseDate':
                plan[field] = "Use 45-day sales cycle from creation date"
            elif field == 'Amount':
                plan[field] = "Check account history for average deal size"
        return {"strategy": plan}