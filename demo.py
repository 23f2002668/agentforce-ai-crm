# demo.py
import time
import json
from app import AgentForceCRM

def run_demo():
    print("\n" + "=" * 60)
    print("🎯 AGENTFORCE CRM - DEMO PRESENTATION")
    print("=" * 60)
    
    try:
        crm = AgentForceCRM()
        
        print("\n📌 DEMO: Processing OPP-001 (Acme Corp - Q1 Deal)")
        print("This opportunity has missing: stage, close_date, amount")
        print("-" * 40)
        
        start = time.time()
        result = crm.process_opportunity("OPP-001")
        elapsed = time.time() - start
        
        print(f"\n⏱️ Time taken: {elapsed:.2f} seconds")
        
        print("\n" + "=" * 40)
        print("📊 PERFORMANCE METRICS")
        print("=" * 40)
        
        fields = result.get("executor", {}).get("fields_updated", 0)
        minutes = result.get("executor", {}).get("time_saved", {}).get("minutes_saved", 0)
        confidence = result.get("executor", {}).get("avg_confidence", 0)
        salesforce_updated = result.get("executor", {}).get("salesforce_updated", False)
        
        print(f"Fields auto-completed: {fields}")
        print(f"Time saved: {minutes} minutes")
        print(f"Average confidence: {confidence}%")
        print(f"Salesforce updated: {'✅ YES' if salesforce_updated else '⚠️ SIMULATION'}")
        
        print("\n" + "=" * 40)
        print("🔄 AGENT COLLABORATION")
        print("=" * 40)
        print("1. Planner Agent: Detected missing fields and created strategy")
        print("2. Retriever Agent: Fetched account history and similar deals")
        print("3. Executor Agent: Updated records and calculated savings")
        
        print("\n✅ DEMO COMPLETE - All three agents worked together!")
        print("=" * 60)
        
        print("\n📋 Full Result:")
        print(json.dumps(result, indent=2))
        
    except Exception as e:
        print(f"\n❌ Demo error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_demo()