"""
Memory Bank Service - RAG with ChromaDB
Simulates Milvus for local development
Provides vector storage for user preferences and historical context
"""
import chromadb
from chromadb.config import Settings
from datetime import datetime
import os
import sys

# Add shared utils to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from shared.utils.logger import get_logger
from shared.utils.errors import MemoryBankError

logger = get_logger("memory-bank")

class MemoryBank:
    """
    Vector store for RAG (Retrieval-Augmented Generation)
    Stores user preferences, historical analysis, trade history
    """
    
    def __init__(self, persist_dir="./data/memory"):
        """
        Initialize ChromaDB client
        
        Args:
            persist_dir: Directory to persist vector database
        """
        try:
            os.makedirs(persist_dir, exist_ok=True)
            
            self.client = chromadb.Client(Settings(
                persist_directory=persist_dir,
                anonymized_telemetry=False
            ))
            
            # Create collections for different data types
            self.user_prefs = self.client.get_or_create_collection("user_preferences")
            self.analysis_history = self.client.get_or_create_collection("analysis_history")
            self.trade_history = self.client.get_or_create_collection("trade_history")
            
            logger.info("MemoryBank initialized", persist_dir=persist_dir)
            
        except Exception as e:
            raise MemoryBankError(f"Failed to initialize MemoryBank: {str(e)}")
    
    def store_user_preference(self, user_id: str, preference_key: str, content: str, metadata: dict = None):
        """
        Store user preference
        
        Args:
            user_id: User identifier
            preference_key: Type of preference (risk_tolerance, sectors, etc.)
            content: Preference description
            metadata: Additional metadata
        """
        try:
            metadata = metadata or {}
            metadata.update({
                "user_id": user_id,
                "preference_key": preference_key,
                "timestamp": datetime.now().isoformat()
            })
            
            doc_id = f"{user_id}_{preference_key}_{datetime.now().timestamp()}"
            
            self.user_prefs.add(
                documents=[content],
                metadatas=[metadata],
                ids=[doc_id]
            )
            
            logger.info("Stored user preference", 
                       user_id=user_id, 
                       preference_key=preference_key)
            
        except Exception as e:
            raise MemoryBankError(f"Failed to store preference: {str(e)}")
    
    def store_analysis(self, ticker: str, analysis_type: str, content: str, metadata: dict =None):
        """
        Store historical analysis
        
        Args:
            ticker: Stock symbol
            analysis_type: Type of analysis (technical, fundamental, etc.)
            content: Analysis text
            metadata: Additional metadata
        """
        try:
            metadata = metadata or {}
            metadata.update({
                "ticker": ticker,
                "analysis_type": analysis_type,
                "timestamp": datetime.now().isoformat()
            })
            
            doc_id = f"{ticker}_{analysis_type}_{datetime.now().timestamp()}"
            
            self.analysis_history.add(
                documents=[content],
                metadatas=[metadata],
                ids=[doc_id]
            )
            
            logger.info("Stored analysis", ticker=ticker, analysis_type=analysis_type)
            
        except Exception as e:
            raise MemoryBankError(f"Failed to store analysis: {str(e)}")
    
    def store_trade(self, ticker: str, action: str, price: float, reasoning: str, metadata: dict = None):
        """
        Store trade recommendation/execution
        
        Args:
            ticker: Stock symbol
            action: BUY/SELL/HOLD
            price: Entry price
            reasoning: Recommendation reasoning
            metadata: Additional metadata
        """
        try:
            metadata = metadata or {}
            metadata.update({
                "ticker": ticker,
                "action": action,
                "price": price,
                "timestamp": datetime.now().isoformat()
            })
            
            doc_id = f"trade_{ticker}_{datetime.now().timestamp()}"
            
            self.trade_history.add(
                documents=[reasoning],
                metadatas=[metadata],
                ids=[doc_id]
            )
            
            logger.info("Stored trade", ticker=ticker, action=action, price=price)
            
        except Exception as e:
            raise MemoryBankError(f"Failed to store trade: {str(e)}")
    
    def retrieve_user_preferences(self, user_id: str, query: str, n_results: int = 5):
        """
        Retrieve relevant user preferences
        
        Args:
            user_id: User identifier
            query: Query text for semantic search
            n_results: Number of results to return
        
        Returns:
            Query results
        """
        try:
            results = self.user_prefs.query(
                query_texts=[query],
                n_results=n_results,
                where={"user_id": user_id}
            )
            
            logger.info("Retrieved user preferences", 
                       user_id=user_id, 
                       results_count=len(results["documents"][0]) if results["documents"] else 0)
            
            return results
            
        except Exception as e:
            raise MemoryBankError(f"Failed to retrieve preferences: {str(e)}")
    
    def retrieve_past_analysis(self, ticker: str, n_results: int = 5):
        """
        Retrieve past analysis for a ticker
        
        Args:
            ticker: Stock symbol
            n_results: Number of results to return
        
        Returns:
            Query results
        """
        try:
            results = self.analysis_history.query(
                query_texts=[f"Analysis for {ticker}"],
                n_results=n_results,
                where={"ticker": ticker}
            )
            
            logger.info("Retrieved past analysis", 
                       ticker=ticker,
                       results_count=len(results["documents"][0]) if results["documents"] else 0)
            
            return results
            
        except Exception as e:
            raise MemoryBankError(f"Failed to retrieve analysis: {str(e)}")

# Singleton instance
_memory_bank = None

def get_memory_bank() -> MemoryBank:
    """Get or create singleton MemoryBank instance"""
    global _memory_bank
    if _memory_bank is None:
        _memory_bank = MemoryBank()
    return _memory_bank
