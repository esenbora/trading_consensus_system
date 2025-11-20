from flask import Flask, jsonify, request
from orchestrator import Orchestrator
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
orchestrator = Orchestrator()

@app.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "online", "system": "Multi-Agent Trading Consensus"})

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Invalid JSON payload"}), 400

        ticker = data.get('ticker')
        if not ticker:
            return jsonify({"error": "Ticker is required"}), 400

        # Validate ticker format (basic check)
        ticker = ticker.strip().upper()
        if not ticker or len(ticker) > 20:
            return jsonify({"error": "Invalid ticker format"}), 400

        result = orchestrator.run_debate(ticker)

        # Check if orchestrator returned an error
        if "error" in result:
            return jsonify({
                "message": f"Analysis failed for {ticker}",
                "status": "error",
                "error": result.get("error"),
                "details": result.get("details", "Unknown error")
            }), 500

        return jsonify({
            "message": f"Analysis completed for {ticker}",
            "status": "success",
            "consensus": result.get('decision', 'UNKNOWN'),
            "confidence": result.get('confidence', 0.0),
            "details": result
        })

    except Exception as e:
        return jsonify({
            "message": "Internal server error",
            "status": "error",
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
