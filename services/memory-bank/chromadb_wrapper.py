"""
Memory Bank Service - RAG with ChromaDB
Simulates Milvus for local development
Provides vector storage for user preferences and historical context
"""
from shared.utils.errors import MemoryBankError
from shared.utils.logger import get_logger
import chromadb
from chromadb.config import Settings
from datetime import datetime
import os
import sys

# Add shared utils to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

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
            self.user_prefs = self.client.get_or_create_collection(
                "user_preferences")
            self.analysis_history = self.client.get_or_create_collection(
                "analysis_history")
            self.trade_history = self.client.get_or_create_collection(
                "trade_history")

            logger.info("MemoryBank initialized", persist_dir=persist_dir)

        except Exception as e:
            raise MemoryBankError(f"Failed to initialize MemoryBank: {str(e)}")

    def store_user_preference(
            self,
            user_id: str,
            preference_key: str,
            content: str,
            metadata: dict = None):
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

    def store_analysis(
            self,
            ticker: str,
            analysis_type: str,
            content: str,
            metadata: dict = None):
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

            logger.info(
                "Stored analysis",
                ticker=ticker,
                analysis_type=analysis_type)

        except Exception as e:
            raise MemoryBankError(f"Failed to store analysis: {str(e)}")

    def store_trade(
            self,
            ticker: str,
            action: str,
            price: float,
            reasoning: str,
            metadata: dict = None):
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

            logger.info(
                "Stored trade",
                ticker=ticker,
                action=action,
                price=price)

        except Exception as e:
            raise MemoryBankError(f"Failed to store trade: {str(e)}")

    def retrieve_user_preferences(
            self,
            user_id: str,
            query: str,
            n_results: int = 5):
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

            logger.info(
                "Retrieved user preferences",
                user_id=user_id,
                results_count=len(
                    results["documents"][0]) if results["documents"] else 0)

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

            logger.info("Retrieved past analysis", ticker=ticker, results_count=len(
                results["documents"][0]) if results["documents"] else 0)

            return results

        except Exception as e:
            raise MemoryBankError(f"Failed to retrieve analysis: {str(e)}")

    # ============ MONTH 3 ENHANCEMENTS ============

    def store_risk_profile(
            self,
            user_id: str,
            risk_tolerance: str,
            max_drawdown: float,
            preferred_sectors: list,
            metadata: dict = None):
        """
        Store user's risk profile

        Args:
            user_id: User identifier
            risk_tolerance: LOW/MEDIUM/HIGH
            max_drawdown: Maximum acceptable drawdown (%)
            preferred_sectors: List of preferred sectors
            metadata: Additional metadata
        """
        try:
            content = f"Risk Tolerance: {risk_tolerance}, Max Drawdown: {max_drawdown}%, Sectors: {
                ', '.join(preferred_sectors)}"

            metadata = metadata or {}
            metadata.update({
                "user_id": user_id,
                "preference_type": "risk_profile",
                "risk_tolerance": risk_tolerance,
                "max_drawdown": max_drawdown,
                "preferred_sectors": preferred_sectors,
                "timestamp": datetime.now().isoformat()
            })

            doc_id = f"{user_id}_risk_profile"

            # Upsert (update if exists)
            try:
                self.user_prefs.delete(ids=[doc_id])
            except Exception:
                pass

            self.user_prefs.add(
                documents=[content],
                metadatas=[metadata],
                ids=[doc_id]
            )

            logger.info(
                "Stored risk profile",
                user_id=user_id,
                risk_tolerance=risk_tolerance)

        except Exception as e:
            raise MemoryBankError(f"Failed to store risk profile: {str(e)}")

    def store_trading_style(self, user_id: str, style: str, timeframe: str,
                            position_sizing: str, metadata: dict = None):
        """
        Store user's trading style preferences

        Args:
            user_id: User identifier
            style: SWING/DAY/LONG_TERM
            timeframe: Preferred timeframe (1d, 1w, 1m, etc.)
            position_sizing: CONSERVATIVE/MODERATE/AGGRESSIVE
            metadata: Additional metadata
        """
        try:
            content = f"Trading Style: {style}, Timeframe: {timeframe}, Position Sizing: {position_sizing}"

            metadata = metadata or {}
            metadata.update({
                "user_id": user_id,
                "preference_type": "trading_style",
                "style": style,
                "timeframe": timeframe,
                "position_sizing": position_sizing,
                "timestamp": datetime.now().isoformat()
            })

            doc_id = f"{user_id}_trading_style"

            # Upsert
            try:
                self.user_prefs.delete(ids=[doc_id])
            except Exception:
                pass

            self.user_prefs.add(
                documents=[content],
                metadatas=[metadata],
                ids=[doc_id]
            )

            logger.info("Stored trading style", user_id=user_id, style=style)

        except Exception as e:
            raise MemoryBankError(f"Failed to store trading style: {str(e)}")

    def get_user_context(self, user_id: str):
        """
        Get comprehensive user profile

        Args:
            user_id: User identifier

        Returns:
            Dictionary with risk profile, trading style, and preferences
        """
        try:
            # Query for all user preferences
            results = self.user_prefs.query(
                query_texts=["user preferences"],
                n_results=10,
                where={"user_id": user_id}
            )

            context = {
                "user_id": user_id,
                "risk_profile": None,
                "trading_style": None,
                "preferences": []
            }

            if results and results["metadatas"]:
                for metadata in results["metadatas"][0]:
                    pref_type = metadata.get("preference_type")

                    if pref_type == "risk_profile":
                        context["risk_profile"] = {
                            "risk_tolerance": metadata.get("risk_tolerance"),
                            "max_drawdown": metadata.get("max_drawdown"),
                            "preferred_sectors": metadata.get("preferred_sectors")}
                    elif pref_type == "trading_style":
                        context["trading_style"] = {
                            "style": metadata.get("style"),
                            "timeframe": metadata.get("timeframe"),
                            "position_sizing": metadata.get("position_sizing")
                        }
                    else:
                        context["preferences"].append(metadata)

            logger.info("Retrieved user context", user_id=user_id,
                        has_risk_profile=context["risk_profile"] is not None)

            return context

        except Exception as e:
            raise MemoryBankError(f"Failed to get user context: {str(e)}")

    def update_preference_from_feedback(
            self,
            user_id: str,
            feedback_type: str,
            content: str):
        """
        Update preferences based on user feedback

        Args:
            user_id: User identifier
            feedback_type: Type of feedback (liked_recommendation, disliked_trade, etc.)
            content: Feedback content
        """
        try:
            metadata = {
                "user_id": user_id,
                "preference_type": "feedback",
                "feedback_type": feedback_type,
                "timestamp": datetime.now().isoformat()
            }

            doc_id = f"{user_id}_feedback_{datetime.now().timestamp()}"

            self.user_prefs.add(
                documents=[content],
                metadatas=[metadata],
                ids=[doc_id]
            )

            logger.info(
                "Stored user feedback",
                user_id=user_id,
                feedback_type=feedback_type)

        except Exception as e:
            raise MemoryBankError(f"Failed to store feedback: {str(e)}")

    def store_agent_output(self, agent_name: str, ticker: str, output: str,
                           confidence: float, metadata: dict = None):
        """
        Store agent output for accuracy tracking

        Args:
            agent_name: Name of the agent
            ticker: Stock ticker
            output: Agent's analysis output
            confidence: Confidence score (0-100)
            metadata: Additional metadata
        """
        try:
            metadata = metadata or {}
            metadata.update({
                "agent_name": agent_name,
                "ticker": ticker,
                "confidence": confidence,
                "timestamp": datetime.now().isoformat()
            })

            doc_id = f"{agent_name}_{ticker}_{datetime.now().timestamp()}"

            self.analysis_history.add(
                documents=[output],
                metadatas=[metadata],
                ids=[doc_id]
            )

            logger.info(
                "Stored agent output",
                agent_name=agent_name,
                ticker=ticker)

        except Exception as e:
            raise MemoryBankError(f"Failed to store agent output: {str(e)}")

    def retrieve_similar_analysis(
            self,
            ticker: str,
            timeframe_days: int = 30,
            n_results: int = 5):
        """
        Retrieve similar past analysis within timeframe

        Args:
            ticker: Stock ticker
            timeframe_days: Number of days to look back
            n_results: Number of results

        Returns:
            Similar analysis results
        """
        try:
            pass
            # Note: cutoff_date would be used for date filtering
            # but ChromaDB doesn't support date range queries easily

            results = self.analysis_history.query(
                query_texts=[f"Analysis for {ticker}"],
                n_results=n_results,
                where={
                    "ticker": ticker,
                    # Note: ChromaDB doesn't support date range queries easily
                    # In production, would filter results by timestamp
                }
            )

            logger.info("Retrieved similar analysis", ticker=ticker, results_count=len(
                results["documents"][0]) if results["documents"] else 0)

            return results

        except Exception as e:
            raise MemoryBankError(
                f"Failed to retrieve similar analysis: {
                    str(e)}")

    def get_accuracy_metrics(self, agent_name: str, ticker: str = None):
        """
        Get agent accuracy metrics

        Args:
            agent_name: Name of the agent
            ticker: Optional ticker filter

        Returns:
            Accuracy metrics (simplified for now)
        """
        try:
            where_clause = {"agent_name": agent_name}
            if ticker:
                where_clause["ticker"] = ticker

            # Query all outputs from this agent
            results = self.analysis_history.query(
                query_texts=[f"{agent_name} analysis"],
                n_results=100,
                where=where_clause
            )

            if not results or not results["metadatas"]:
                return {
                    "agent_name": agent_name,
                    "total_analyses": 0,
                    "average_confidence": 0.0
                }

            # Calculate average confidence
            confidences = [m.get("confidence", 0)
                           for m in results["metadatas"][0]]
            avg_confidence = sum(confidences) / \
                len(confidences) if confidences else 0.0

            metrics = {
                "agent_name": agent_name,
                "total_analyses": len(results["metadatas"][0]),
                "average_confidence": round(avg_confidence, 2),
                "ticker": ticker
            }

            logger.info("Calculated accuracy metrics", agent_name=agent_name,
                        total_analyses=metrics["total_analyses"])

            return metrics

        except Exception as e:
            raise MemoryBankError(f"Failed to get accuracy metrics: {str(e)}")

    def compact_old_data(self, days_to_keep: int = 90):
        """
        Archive/delete old data to keep database performant

        Args:
            days_to_keep: Number of days of data to retain

        Returns:
            Number of documents deleted
        """
        try:
            from datetime import timedelta
            cutoff_date = (
                datetime.now() -
                timedelta(
                    days=days_to_keep)).isoformat()

            # Note: ChromaDB doesn't have built-in date-based deletion
            # In production, would implement proper archival
            # For now, just log the intention

            logger.info(
                "Compact old data called",
                days_to_keep=days_to_keep,
                cutoff_date=cutoff_date,
                note="Archival not fully implemented - ChromaDB limitation")

            return {
                "status": "partial",
                "message": "Archival logged, full implementation pending"}

        except Exception as e:
            raise MemoryBankError(f"Failed to compact data: {str(e)}")

    def query_user_preferences(self, user_id: str, query: str, limit: int = 5):
        """
        Query user preferences (kept for backwards compatibility)
        Now redirects to retrieve_user_preferences
        """
        return self.retrieve_user_preferences(user_id, query, limit)


# Singleton instance
_memory_bank = None


def get_memory_bank() -> MemoryBank:
    """Get or create singleton MemoryBank instance"""
    global _memory_bank
    if _memory_bank is None:
        _memory_bank = MemoryBank()
    return _memory_bank
