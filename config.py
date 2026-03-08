# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Central configuration for all agents"""
    
    # Azure Foundry connection
    ENDPOINT = os.getenv("AZURE_FOUNDRY_ENDPOINT")
    API_KEY = os.getenv("AZURE_FOUNDRY_API_KEY")
    
    # Model deployments
    PLANNER_MODEL = os.getenv("PLANNER_MODEL", "Phi-4-reasoning")
    RETRIEVER_MODEL = os.getenv("RETRIEVER_MODEL", "Phi-4-mini-instruct")
    EXECUTOR_MODEL = os.getenv("EXECUTOR_MODEL", "Phi-4-mini-instruct")
    
    # Salesforce Configuration
    SF_USERNAME = os.getenv("SF_USERNAME")
    SF_PASSWORD = os.getenv("SF_PASSWORD")
    SF_SECURITY_TOKEN = os.getenv("SF_SECURITY_TOKEN")
    SF_DOMAIN = os.getenv("SF_DOMAIN", "login")
    SF_CONSUMER_KEY = os.getenv("SF_CONSUMER_KEY")
    SF_CONSUMER_SECRET = os.getenv("SF_CONSUMER_SECRET")
    
    # Agent settings
    TEMPERATURE = 0.3
    MAX_TOKENS = 2000
    
    @classmethod
    def validate(cls):
        """Check if all required configs are set"""
        missing = []
        if not cls.ENDPOINT:
            missing.append("AZURE_FOUNDRY_ENDPOINT")
        if not cls.API_KEY:
            missing.append("AZURE_FOUNDRY_API_KEY")
        
        if missing:
            print(f"⚠️ Warning: Missing Azure credentials: {', '.join(missing)}")
            print("   Running in simulation mode")
        else:
            print(f"\n✅ Azure Configuration loaded:")
            print(f"  Endpoint: {cls.ENDPOINT}")
            print(f"  Planner: {cls.PLANNER_MODEL}")
            print(f"  Retriever: {cls.RETRIEVER_MODEL}")
            print(f"  Executor: {cls.EXECUTOR_MODEL}")
        
        return True