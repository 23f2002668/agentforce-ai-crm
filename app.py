# app.py
import json
from config import Config
from tools.salesforce_client import SalesforceClient
from agents.planner import PlannerAgent
from agents.retriever import RetrieverAgent
from agents.executor import ExecutorAgent

class AgentForceCRM:
    def __init__(self):
        print("=" * 60)
        print("🚀 AgentForce CRM - Three-Agent System")
        print("=" * 60)
        
        Config.validate()
        self.sf = SalesforceClient()
        self.planner = PlannerAgent(self.sf)
        self.retriever = RetrieverAgent(self.sf)
        self.executor = ExecutorAgent(self.sf)
        
        print("✅ All agents initialized")
        print("=" * 60)
    
    def process_opportunity(self, opportunity_id: str) -> dict:
        print(f"\n📋 PROCESSING OPPORTUNITY: {opportunity_id}")
        print("-" * 40)
        
        planner_result = self.planner.analyze_opportunity(opportunity_id)
        
        if not planner_result.get("missing_fields"):
            return planner_result
        
        opportunity = planner_result.get("original_opportunity", {})
        context_result = self.retriever.fetch_context(opportunity, planner_result.get("plan", {}))
        execution_result = self.executor.execute_plan(opportunity_id, planner_result, context_result)
        
        return {
            "opportunity_id": opportunity_id,
            "planner": {
                "missing_fields": planner_result.get("missing_fields", [])
            },
            "retriever": {
                "account_history_count": context_result.get("account_history_count", 0),
                "similar_deals_count": context_result.get("similar_deals_count", 0),
                "industry": context_result.get("industry", "Unknown")
            },
            "executor": {
                "updates_made": execution_result.get("updates_made", []),
                "fields_updated": execution_result.get("fields_updated", 0),
                "time_saved": execution_result.get("time_saved", {}),
                "avg_confidence": execution_result.get("avg_confidence", 0),
                "salesforce_updated": execution_result.get("salesforce_updated", False)
            }
        }

def main():
    crm = AgentForceCRM()
    
    print("\n📋 Available Opportunities:")
    print("  OPP-001: Acme Corp - Q1 Deal (missing: stage, close_date, amount)")
    print("  OPP-002: TechCorp - Enterprise License (complete)")
    print("  OPP-003: HealthInc - Implementation (missing: stage, close_date)")
    print()
    
    opportunity_id = input("Enter opportunity ID (or press Enter for OPP-001): ").strip()
    if not opportunity_id:
        opportunity_id = "OPP-001"
    
    result = crm.process_opportunity(opportunity_id)
    
    print("\n📊 FINAL RESULT:")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()