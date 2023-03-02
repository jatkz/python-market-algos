"""
This module provides an api for candle metrics


    
    Note that the debug=True option in app.run() enables debug mode,
    which provides more detailed error messages and auto-reloads the
    app when changes are made to the code. You should not use debug mode
    in production, as it can expose security vulnerabilities and other
    issues. Instead, you should use a production-ready web server such as
    Gunicorn or uWSGI to deploy your app.
    
"""

import os
from flask import Flask, jsonify
from pymongo import MongoClient
import pandas as pd
from ta.momentum import rsi

app = Flask(__name__)


def mongo_connection():
    """_summary_

    Returns:
        _type_: map of collections
    """
    # MongoDB configuration
    MONGO_URI = os.environ.get(
        "MONGO_URI"
    )  # This should be set in your production environment
    MONGO_DB = os.environ.get("MONGODB_DB", "tdameritrade")  # Default to test database

    # Production options for MongoDB connection
    MONGODB_OPTIONS = {
        "retryWrites": True,  # retry writes in case of network failures
        "w": "majority",  # wait for majority write acknowledgement
        "maxPoolSize": 5,  # maximum number of connections in the connection pool
        "minPoolSize": 1,  # minimum number of connections in the connection pool
        "connectTimeoutMS": 5000,  # maximum time to establish a connection
        "maxIdleTimeMS": 30000,  # maximum time a connection can remain idle
        # "ssl": True,  # use SSL for secure connection
        # "ssl_cert_reqs": "CERT_NONE",  # do not require SSL certificate validation
    }

    # Connect to MongoDB
    client = MongoClient(MONGO_URI, **MONGODB_OPTIONS)
    db = client[MONGO_DB]
    collections = {"Short": db["Short"], "Medium": db["Medium"], "Macros": db["Macros"]}
    return collections


collections = mongo_connection()


def query_candle(collection, symbol_name):
    """_summary_

    Args:
        collection (str): mongo db collection name
        symbol (str): name such as "TSLA"

    Returns:
        _type_: list of candles in json format ohlc, volume, datetime
    """
    if collection not in collections:
        raise ValueError("Invalid collection")
    symbol = collections[collection].find_one({"symbol": symbol_name})
    if not symbol:
        raise ValueError("Invalid symbol")
    if not symbol["candles"] or len(symbol["candles"]) < 1:
        raise ValueError("Candles property does not exist or is empty")
    return symbol["candles"]


@app.route("/<collection>/<symbol>/rsi/<window>", methods=["GET"])
def get_rsi(collection, symbol, window):
    """_summary_

    Args:
        collection (_type_): _description_
        symbol (_type_): _description_
        n (_type_): _description_

    Returns:
        _type_: _description_
    """
    try:
        try:
            window = int(window)
        except ValueError:
            raise ValueError("Invalid n")

        candles = query_candle(collection, symbol)
        if len(candles) < window:
            raise ValueError("Not enough candles")

        dataframe = pd.DataFrame(candles)
        dataframe["rsi"] = rsi(close=dataframe["close"], window=window, fillna=True)
        return dataframe[["rsi", "datetime"]].to_json(orient="records")
    except Exception as exception:
        return jsonify(error=str(exception)), 500


@app.route("/create", methods=["POST"])
def create():
    # Get data from request
    data = request.get_json()

    # Insert data into MongoDB
    result = collection.insert_one(data)

    # Return success message
    return jsonify(
        {"message": "Data created successfully", "id": str(result.inserted_id)}
    )


@app.route("/read", methods=["GET"])
def read():
    # Find all data in MongoDB
    result = collection.find()

    # Convert result to list and jsonify it
    return jsonify(list(result))


@app.route("/update/<id>", methods=["PUT"])
def update(id):
    # Get data from request
    data = request.get_json()

    # Update data in MongoDB
    result = collection.update_one({"_id": ObjectId(id)}, {"$set": data})

    # Return success message
    return jsonify({"message": "Data updated successfully", "id": id})


if __name__ == "__main__":
    app.run(debug=True)
