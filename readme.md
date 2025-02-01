# Realtime Stock Market Analytics

## Created By 
- Abhishek Singh (885199042)
  
## Overview
This project, is developed to enhance investors' ability to make informed decisions swiftly by providing access to real-time stock market data and analysis tools. This platform captures live trade data from Finnhub WebSocket and utilizes Kafka for data distribution, Apache Spark for stream processing, and Flask for backend implementation.

## Features
- **Real-time Data Streaming:** Using Finnhub's WebSocket to stream live data for US stocks, forex, and cryptocurrencies.
- **Data Analysis:** Spark Structured Streaming for processing live data and calculating metrics like trade count and average price.
- **Visualization:** Real-time data visualization with Chart.js, showcasing metrics in an interactive and user-friendly manner.

## Technologies Used
- Python
- Flask
- Kafka
- Apache Spark
- Spark Structured Streaming
- Websockets
- Chart.js

## Installation

### Prerequisites
- Python 3.x
- Apache Kafka
- Apache Spark

### Setup
1. Clone the repository: github.com/abhishekbuilds/StreamAnalytics
2. Install Python packages: pip install -r requirements.txt

### Configuration
- Update the config.json file with the necessary Kafka topic and Finnhub token.

## Usage
- Start the Kafka server and create a topic as specified in config.json.
- Run dataProducer.py to begin streaming data from Finnhub.
- Execute sparkApp.py for Spark Streaming and data processing.
- Launch the Flask server by running app.py.
- Open index.html in a browser to view the real-time analytics.
