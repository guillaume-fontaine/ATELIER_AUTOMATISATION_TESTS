import sqlite3
import json

DB_FILE = "runs.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            api_name TEXT NOT NULL,
            passed INTEGER NOT NULL,
            failed INTEGER NOT NULL,
            error_rate REAL NOT NULL,
            latency_avg REAL NOT NULL,
            latency_p95 REAL NOT NULL,
            tests_json TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def save_run(run_data):
    init_db()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    summary = run_data["summary"]
    cursor.execute('''
        INSERT INTO runs (timestamp, api_name, passed, failed, error_rate, latency_avg, latency_p95, tests_json)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        run_data["timestamp"],
        run_data["api"],
        summary["passed"],
        summary["failed"],
        summary["error_rate"],
        summary["latency_ms_avg"],
        summary["latency_ms_p95"],
        json.dumps(run_data["tests"])
    ))
    conn.commit()
    conn.close()

def list_runs(limit=10):
    init_db()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, timestamp, api_name, passed, failed, error_rate, latency_avg, latency_p95, tests_json
        FROM runs
        ORDER BY id DESC
        LIMIT ?
    ''', (limit,))
    rows = cursor.fetchall()
    conn.close()
    
    runs = []
    for row in rows:
        runs.append({
            "id": row[0],
            "timestamp": row[1],
            "api": row[2],
            "summary": {
                "passed": row[3],
                "failed": row[4],
                "error_rate": row[5],
                "latency_ms_avg": row[6],
                "latency_ms_p95": row[7]
            },
            "tests": json.loads(row[8])
        })
    return runs
