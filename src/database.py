from google.cloud import firestore
from src.config import Config
import datetime
import logging

# Configure Professional Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OutbreakRegistry:
    """
    MCP Tool: Handles persistent storage of disease outbreaks.
    """
    def __init__(self):
        self.db = firestore.Client(project=Config.PROJECT_ID)
        self.collection = self.db.collection(Config.COLLECTION_NAME)

    def log_incident(self, plant: str, disease: str, confidence: float, severity: str):
        """
        Logs a confirmed disease incident to the database.
        """
        try:
            data = {
                "timestamp": datetime.datetime.now(),
                "plant": plant,
                "disease": disease,
                "confidence": confidence,
                "severity": severity,
                "status": "OPEN"
            }
            doc_ref = self.collection.document()
            doc_ref.set(data)
            logger.info(f"Incident logged: {doc_ref.id}")
            return f"SUCCESS: Logged {disease} outbreak with ID {doc_ref.id}"
        except Exception as e:
            logger.error(f"Database Error: {e}")
            return "ERROR: Failed to log incident."

    def get_recent_stats(self):
        """Fetches recent stats for the dashboard."""
        try:
            docs = self.collection.order_by("timestamp", direction=firestore.Query.DESCENDING).limit(5).stream()
            return [{"Plant": d.get("plant"), "Disease": d.get("disease"), "Severity": d.get("severity")} for d in docs]
        except Exception:
            return []