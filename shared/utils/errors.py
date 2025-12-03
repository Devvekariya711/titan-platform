"""
Custom error classes for Titan Platform
Provides consistent error handling across services
"""


class TitanError(Exception):
    """Base exception for Titan Platform"""

    def __init__(self, message: str, error_code: str = "TITAN_ERROR"):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class DataFetchError(TitanError):
    """Raised when data fetching fails"""

    def __init__(self, message: str, ticker: str = None):
        self.ticker = ticker
        super().__init__(message, error_code="DATA_FETCH_ERROR")


class ToolExecutionError(TitanError):
    """Raised when tool execution fails"""

    def __init__(self, message: str, tool_name: str = None):
        self.tool_name = tool_name
        super().__init__(message, error_code="TOOL_EXECUTION_ERROR")


class AgentError(TitanError):
    """Raised when agent encounters an error"""

    def __init__(self, message: str, agent_name: str = None):
        self.agent_name = agent_name
        super().__init__(message, error_code="AGENT_ERROR")


class MemoryBankError(TitanError):
    """Raised when memory operations fail"""

    def __init__(self, message: str):
        super().__init__(message, error_code="MEMORY_BANK_ERROR")


class RiskVetoError(TitanError):
    """Raised when Risk Officer vetoes a trade"""

    def __init__(self, message: str, reason: str = None):
        self.reason = reason
        super().__init__(message, error_code="RISK_VETO")
