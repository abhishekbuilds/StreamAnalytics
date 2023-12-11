from flask import Flask, render_template, Response, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

symbol_updates = {}

def has_window_start(symbol, target_window_start):
    return any(update["window_start"] == target_window_start for update in symbol_updates.get(symbol, []))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/updateData', methods=['POST'])
def update_data():
    if request.headers['Content-Type'] == 'application/json':
        data_list = request.get_json()
        print(f"Received data: {data_list}")

        for data in data_list:
            data_dict = json.loads(data)
            if 'window' in data_dict and 's' in data_dict and 'average_price' in data_dict:
                symbol = data_dict['s']
                if symbol not in symbol_updates:
                    symbol_updates[symbol] = []

                window_start = data_dict['window']['start']
                average_price = data_dict['average_price']
                average_volume =  data_dict['average_volume']
                trade_count = data_dict['trade_count']
                
                if not has_window_start(symbol, window_start):
                    symbol_updates[symbol].append({
                        "window_start": window_start,
                        "average_price": average_price,
                        "average_volume": average_volume,
                        "trade_count": trade_count
                    })
                else:
                    for update in symbol_updates[symbol]:
                        if update["window_start"] == window_start:
                            update["average_price"] = average_price
                            update["average_volume"] = average_volume
                            update["trade_count"] = trade_count
                            break
                    print(symbol_updates)

        return jsonify({"message": "Data received successfully"})
    else:
        return jsonify({"error": "Unsupported Media Type"})

@app.route('/latestData', methods=['GET'])
def latest_data():
    return jsonify(symbol_updates)        

if __name__ == '__main__':
    app.run(host='localhost', port=5001, debug=True)
