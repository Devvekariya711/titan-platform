"""
Titan Platform - Simple Metrics Dashboard
Displays system observability metrics including agent statistics, 
tool performance, and resource usage.
"""
import os
import sys
import json
from datetime import datetime
from typing import Dict, List, Any
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.utils.logger import TitanLogger


class TitanDashboard:
    """Simple metrics dashboard for system observability"""
    
    def __init__(self, project_root: str = None):
        self.project_root = project_root or os.path.dirname(os.path.dirname(__file__))
        self.logs_dir = os.path.join(self.project_root, "logs")
        self.data_dir = os.path.join(self.project_root, "data")
        
    def get_agent_statistics(self) -> Dict[str, Any]:
        """Collect agent usage statistics from logs"""
        agent_stats = {}
        
        # Parse log files for agent decisions
        if not os.path.exists(self.logs_dir):
            return {"error": "Logs directory not found"}
        
        for log_file in Path(self.logs_dir).glob("titan-*.log"):
            try:
                with open(log_file, 'r') as f:
                    for line in f:
                        try:
                            log_entry = json.loads(line.strip())
                            if log_entry.get("event_type") == "agent_decision":
                                agent_name = log_entry.get("agent", "unknown")
                                
                                if agent_name not in agent_stats:
                                    agent_stats[agent_name] = {
                                        "call_count": 0,
                                        "avg_confidence": 0.0,
                                        "confidences": []
                                    }
                                
                                agent_stats[agent_name]["call_count"] += 1
                                confidence = log_entry.get("confidence", 0.0)
                                agent_stats[agent_name]["confidences"].append(confidence)
                        except json.JSONDecodeError:
                            continue
            except Exception as e:
                continue
        
        # Calculate averages
        for agent_name, stats in agent_stats.items():
            if stats["confidences"]:
                stats["avg_confidence"] = sum(stats["confidences"]) / len(stats["confidences"])
            del stats["confidences"]  # Remove raw data
        
        return agent_stats
    
    def get_tool_metrics(self) -> Dict[str, Any]:
        """Collect tool execution metrics from logger"""
        try:
            performance_stats = TitanLogger.get_performance_stats()
            
            # Filter for tool executions
            tool_metrics = {
                key: value for key, value in performance_stats.items()
                if "tool" in key.lower() or key in self._get_known_tools()
            }
            
            return tool_metrics
        except Exception as e:
            return {}
    
    def get_memory_bank_stats(self) -> Dict[str, Any]:
        """Get Memory Bank storage statistics"""
        memory_bank_dir = os.path.join(self.project_root, "services", "memory-bank", "chroma_data")
        
        if not os.path.exists(memory_bank_dir):
            return {
                "status": "not_initialized",
                "size_mb": 0,
                "collections": 0
            }
        
        # Calculate directory size
        total_size = 0
        file_count = 0
        for dirpath, dirnames, filenames in os.walk(memory_bank_dir):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                if os.path.exists(filepath):
                    total_size += os.path.getsize(filepath)
                    file_count += 1
        
        return {
            "status": "operational",
            "size_mb": round(total_size / (1024 * 1024), 2),
            "files": file_count,
            "location": memory_bank_dir
        }
    
    def get_backtest_cache_stats(self) -> Dict[str, Any]:
        """Get backtest cache statistics"""
        cache_dir = os.path.join(self.data_dir, "historical")
        
        if not os.path.exists(cache_dir):
            return {
                "status": "no_cache",
                "cached_tickers": 0,
                "cache_size_mb": 0
            }
        
        # Count CSV files (cached tickers)
        csv_files = list(Path(cache_dir).glob("*.csv"))
        tickers = [f.stem for f in csv_files]
        
        # Calculate cache size
        total_size = sum(f.stat().st_size for f in csv_files if f.exists())
        
        # Calculate cache hit ratio from logs
        hit_ratio = self._calculate_cache_hit_ratio()
        
        return {
            "status": "operational",
            "cached_tickers": len(tickers),
            "tickers": tickers[:10],  # Show first 10
            "cache_size_mb": round(total_size / (1024 * 1024), 2),
            "hit_ratio": hit_ratio
        }
    
    def _calculate_cache_hit_ratio(self) -> str:
        """Calculate cache hit ratio from logs"""
        # Simplified - would need actual cache hit/miss logging
        return "N/A (requires cache event logging)"
    
    def _get_known_tools(self) -> List[str]:
        """List of known tool names for filtering"""
        return [
            "get_market_data", "calculate_technicals", "analyze_price_action",
            "get_earnings_data", "calculate_pe_ratio", "analyze_order_book",
            "detect_liquidity", "find_support_resistance", "multi_source_news",
            "reddit_sentiment", "twitter_sentiment", "get_interest_rates",
            "get_gdp_data", "track_geopolitical_events", "sentiment_analyzer",
            "calculate_var", "check_compliance", "portfolio_correlation",
            "volatility_monitor", "detect_black_swans", "backtest_strategy",
            "monte_carlo_simulation", "memory_save", "memory_retrieve",
            "send_alert", "log_structured", "get_user_context", "store_agent_output"
        ]
    
    def generate_text_report(self) -> str:
        """Generate text-based dashboard report"""
        report = []
        report.append("=" * 80)
        report.append("TITAN PLATFORM - SYSTEM DASHBOARD")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("=" * 80)
        report.append("")
        
        # Agent Statistics
        report.append("📊 AGENT STATISTICS")
        report.append("-" * 80)
        agent_stats = self.get_agent_statistics()
        if agent_stats and "error" not in agent_stats:
            for agent_name, stats in sorted(agent_stats.items(), 
                                          key=lambda x: x[1]["call_count"], 
                                          reverse=True):
                report.append(f"  {agent_name}:")
                report.append(f"    Calls: {stats['call_count']}")
                report.append(f"    Avg Confidence: {stats['avg_confidence']:.2f}")
        else:
            report.append("  No agent statistics available (no logs found)")
        report.append("")
        
        # Tool Metrics
        report.append("🔧 TOOL PERFORMANCE")
        report.append("-" * 80)
        tool_metrics = self.get_tool_metrics()
        if tool_metrics:
            for tool_name, metrics in sorted(tool_metrics.items(), 
                                           key=lambda x: x[1]["avg_ms"]):
                report.append(f"  {tool_name}:")
                report.append(f"    Executions: {metrics['count']}")
                report.append(f"    Avg Time: {metrics['avg_ms']:.2f}ms")
                report.append(f"    Min/Max: {metrics['min_ms']:.2f}ms / {metrics['max_ms']:.2f}ms")
        else:
            report.append("  No tool metrics available")
        report.append("")
        
        # Memory Bank
        report.append("💾 MEMORY BANK")
        report.append("-" * 80)
        memory_stats = self.get_memory_bank_stats()
        report.append(f"  Status: {memory_stats['status']}")
        report.append(f"  Storage Size: {memory_stats['size_mb']} MB")
        report.append(f"  Files: {memory_stats.get('files', 'N/A')}")
        report.append("")
        
        # Backtest Cache
        report.append("📈 BACKTEST CACHE")
        report.append("-" * 80)
        cache_stats = self.get_backtest_cache_stats()
        report.append(f"  Status: {cache_stats['status']}")
        report.append(f"  Cached Tickers: {cache_stats['cached_tickers']}")
        report.append(f"  Cache Size: {cache_stats['cache_size_mb']} MB")
        if cache_stats.get('tickers'):
            report.append(f"  Tickers: {', '.join(cache_stats['tickers'])}")
        report.append(f"  Hit Ratio: {cache_stats.get('hit_ratio', 'N/A')}")
        report.append("")
        
        report.append("=" * 80)
        
        return "\n".join(report)
    
    def generate_html_dashboard(self) -> str:
        """Generate simple HTML dashboard"""
        agent_stats = self.get_agent_statistics()
        tool_metrics = self.get_tool_metrics()
        memory_stats = self.get_memory_bank_stats()
        cache_stats = self.get_backtest_cache_stats()
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Titan Platform Dashboard</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            border-bottom: 3px solid #4CAF50;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #555;
            margin-top: 30px;
        }}
        .metric-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .metric-card {{
            background-color: #f9f9f9;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #4CAF50;
        }}
        .metric-title {{
            font-weight: bold;
            color: #666;
            font-size: 14px;
        }}
        .metric-value {{
            font-size: 24px;
            color: #333;
            margin: 10px 0;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #4CAF50;
            color: white;
        }}
        .timestamp {{
            color: #999;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Titan Platform Dashboard</h1>
        <p class="timestamp">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <h2>📊 Agent Statistics</h2>
        <table>
            <thead>
                <tr>
                    <th>Agent Name</th>
                    <th>Calls</th>
                    <th>Avg Confidence</th>
                </tr>
            </thead>
            <tbody>
"""
        
        if agent_stats and "error" not in agent_stats:
            for agent_name, stats in sorted(agent_stats.items(), 
                                          key=lambda x: x[1]["call_count"], 
                                          reverse=True):
                html += f"""
                <tr>
                    <td>{agent_name}</td>
                    <td>{stats['call_count']}</td>
                    <td>{stats['avg_confidence']:.2f}</td>
                </tr>
"""
        else:
            html += "<tr><td colspan='3'>No data available</td></tr>"
        
        html += """
            </tbody>
        </table>
        
        <h2>🔧 Tool Performance</h2>
        <table>
            <thead>
                <tr>
                    <th>Tool Name</th>
                    <th>Executions</th>
                    <th>Avg Time (ms)</th>
                </tr>
            </thead>
            <tbody>
"""
        
        if tool_metrics:
            for tool_name, metrics in sorted(tool_metrics.items(), 
                                           key=lambda x: x[1]["avg_ms"]):
                html += f"""
                <tr>
                    <td>{tool_name}</td>
                    <td>{metrics['count']}</td>
                    <td>{metrics['avg_ms']:.2f}</td>
                </tr>
"""
        else:
            html += "<tr><td colspan='3'>No data available</td></tr>"
        
        html += f"""
            </tbody>
        </table>
        
        <h2>💾 System Resources</h2>
        <div class="metric-grid">
            <div class="metric-card">
                <div class="metric-title">Memory Bank Status</div>
                <div class="metric-value">{memory_stats['status']}</div>
                <div>{memory_stats['size_mb']} MB</div>
            </div>
            <div class="metric-card">
                <div class="metric-title">Backtest Cache</div>
                <div class="metric-value">{cache_stats['cached_tickers']} tickers</div>
                <div>{cache_stats['cache_size_mb']} MB</div>
            </div>
        </div>
    </div>
</body>
</html>
"""
        
        return html
    
    def save_html_dashboard(self, output_file: str = "dashboard.html"):
        """Save HTML dashboard to file"""
        html = self.generate_html_dashboard()
        output_path = os.path.join(self.project_root, output_file)
        
        with open(output_path, 'w') as f:
            f.write(html)
        
        return output_path


def main():
    """Main entry point for dashboard"""
    dashboard = TitanDashboard()
    
    # Generate text report
    print(dashboard.generate_text_report())
    
    # Generate HTML dashboard
    html_path = dashboard.save_html_dashboard()
    print(f"\n✅ HTML dashboard saved to: {html_path}")
    print(f"   Open in browser: file://{html_path}")


if __name__ == "__main__":
    main()
