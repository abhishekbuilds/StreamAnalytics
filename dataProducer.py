import os
import asyncio
import websockets
import json
import time
import csv
from kafka import KafkaProducer
from bson import json_util
from datetime import datetime

global run_dir
global seq
seq = 0

bulk_data_buffer = []

with open('config.json', 'r') as config_file:
    config = json.load(config_file)
kafka_topic = config['kafka_topic']
finnhub_token = config['finnhub_token']

def send_to_kafka(trades):
    producer = KafkaProducer(bootstrap_servers='localhost:9092')
    for trade in trades:
        producer.send(kafka_topic, value=trade.encode('utf-8'))
    producer.flush()

def replace_null_with_string(data):
    if data is None:
        return "null"
    return data   

def convert_timestamp(timestamp):
    timestamp /= 1000
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def create_run_logs_directory():
    run_logs_dir = "run_logs"
    if not os.path.exists(run_logs_dir):
        os.makedirs(run_logs_dir)
        print(f"Created '{run_logs_dir}' directory.")
    run_dir = os.path.join(run_logs_dir, f"run_{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}")
    os.makedirs(run_dir)
    print(f"Created '{run_dir}' directory.")
    return run_dir

def write_data_to_file(file_path, data):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    formatted_data = {
        "timestamp": timestamp,
        "data": json.loads(data)
    }

    with open(file_path, "a") as file:
        file.write(json.dumps(formatted_data, default=json_util.default, indent=2) + "\n")

async def connect_to_finnhub_websocket():
    socketUrl = 'wss://ws.finnhub.io?token=' + finnhub_token
    async with websockets.connect(socketUrl) as websocket:
        print("Connected to Finnhub WebSocket")

        subscription_messages = [
            {"type": "subscribe", "symbol": "BINANCE:BTCUSDT"},
            {"type": "subscribe", "symbol": "BINANCE:ETHUSDT"},
        ]

        for message in subscription_messages:
            await websocket.send(json.dumps(message))

        while True:
            try:
                data = await websocket.recv()
                print("Received data:", data)
                # Save received data to a file
                # received_data_filename = os.path.join(run_dir, "received_data.json")
                # write_data_to_file(received_data_filename, data)
                process_and_send_trade(data)
            except websockets.exceptions.ConnectionClosed as e:
                print(f"Connection closed unexpectedly: {e}")
                break

def process_and_send_trade(data):
    global seq
    global bulk_data_buffer

    json_data = json.loads(data)

    if 'data' in json_data:
        for item in json_data['data']:
            item['c'] = replace_null_with_string(item.get('c'))

            p = item.get('p')
            v = item.get('v')
            s = item.get('s')
            t = item.get('t')
            data_type = json_data['type']

            seq = seq + 1

            trade_data = {
                "id" : seq,
                "c": item['c'],
                "p": p,
                "s": s,
                "t": convert_timestamp(t),
                "v": v,
                "type": data_type
            }
            print("Processing Data:", trade_data)
            # sent_data_filename = os.path.join(run_dir, "sent_data.csv")
            # with open(sent_data_filename, mode='a', newline='') as file:
            #     csv_writer = csv.writer(file)
            #     csv_writer.writerow(trade_data.values())

            bulk_data_buffer.append(json.dumps(trade_data, default=json_util.default))
        
        send_to_kafka(bulk_data_buffer)
        bulk_data_buffer = []

if __name__ == '__main__':
    run_dir = create_run_logs_directory()
    asyncio.get_event_loop().run_until_complete(connect_to_finnhub_websocket())
