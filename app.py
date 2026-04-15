from flask import Flask, request, jsonify
import alpaca_trade_api as tradeapi
import os

app = Flask(__name__)

API_KEY = os.environ.get("ALPACA_API_KEY")
SECRET_KEY = os.environ.get("ALPACA_SECRET_KEY")
BASE_URL = "https://paper-api.alpaca.markets"

api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL, api_version='v2')

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if not data:
        return jsonify({"error": "No data"}), 400

    action = data.get("action")
    symbol = "NQ1!"
    qty = 1

    try:
        if action == "buy":
            api.submit_order(
                symbol="NQ1!",
                qty=qty,
                side="buy",
                type="market",
                time_in_force="gtc"
            )
            return jsonify({"status": "buy order placed"}), 200

        elif action == "sell":
            api.submit_order(
                symbol="NQ1!",
                qty=qty,
                side="sell",
                type="market",
                time_in_force="gtc"
            )
            return jsonify({"status": "sell order placed"}), 200

        elif action == "close":
            api.close_position("NQ1!")
            return jsonify({"status": "position closed"}), 200

        else:
            return jsonify({"error": "Unknown action"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def index():
    return "Trading bot actif !", 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
