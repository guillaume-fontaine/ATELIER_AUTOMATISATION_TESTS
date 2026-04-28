from flask import Flask, render_template, jsonify, request, redirect, url_for
from tester.runner import execute_run
import storage

app = Flask(__name__)

@app.route("/")
def consignes():
    return render_template('consignes.html')

@app.route("/dashboard")
def dashboard():
    runs = storage.list_runs()
    return render_template('dashboard.html', runs=runs)

@app.route("/run", methods=["POST", "GET"])
def trigger_run():
    # Déclenche manuellement ou via tâche planifiée
    run_data = execute_run()
    storage.save_run(run_data)
    
    # Si c'est une API JSON (ex: curl/tâche planifiée) on renvoie du JSON
    if request.headers.get("Accept") == "application/json" or request.method == "GET":
        return jsonify(run_data)
        
    return redirect(url_for('dashboard'))

@app.route("/health")
def health():
    return jsonify({
        "status": "UP",
        "api_target": "Agify",
        "message": "Service is running"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
