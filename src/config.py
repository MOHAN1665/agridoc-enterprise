import os
from dotenv import load_dotenv

# Load local .env file if it exists (for local dev)
load_dotenv()

class Config:
    # We still need Project ID for the Database (Firestore)
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
    
    # We need the API Key for the AI
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") 
    
    # Use the Pro model (It is free with the API Key!)
    MODEL_NAME = "gemini-2.5-flash" 
    COLLECTION_NAME = "agridoc_outbreaks"
    
    @staticmethod
    def validate():
        if not Config.PROJECT_ID:
            raise ValueError("GOOGLE_CLOUD_PROJECT environment variable is not set.")