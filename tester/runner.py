from datetime import datetime, timezone
import json
import statistics
from .tests import run_tests

def execute_run():
    timestamp = datetime.now(timezone.utc).isoformat()
    tests = run_tests()
    
    passed = sum(1 for t in tests if t["status"] == "PASS")
    failed = sum(1 for t in tests if t["status"] != "PASS")
    total = len(tests)
    
    error_rate = failed / total if total > 0 else 0
    latencies = [t["latency_ms"] for t in tests if t["latency_ms"] is not None]
    
    latency_ms_avg = sum(latencies) / len(latencies) if latencies else 0
    latency_ms_p95 = statistics.quantiles(latencies, n=20)[18] if len(latencies) > 1 else (latencies[0] if latencies else 0)
    
    run_data = {
        "api": "Agify",
        "timestamp": timestamp,
        "summary": {
            "passed": passed,
            "failed": failed,
            "error_rate": error_rate,
            "latency_ms_avg": latency_ms_avg,
            "latency_ms_p95": latency_ms_p95
        },
        "tests": tests
    }
    
    return run_data
