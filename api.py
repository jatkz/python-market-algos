import os
from flask import Flask, jsonify
from pymongo import MongoClient
import pandas as pd
from ta.momentum import rsi

app = Flask(__name__)

# MongoDB configuration
MONGODB_URI = os.environ.get(
    "MONGODB_URI"
)  # This should be set in your production environment
MONGODB_DB = os.environ.get("MONGODB_DB", "mydatabase")
MONGODB_COLLECTION = os.environ.get("MONGODB_COLLECTION", "mycollection")
MONGODB_USERNAME = os.environ.get("MONGODB_USERNAME")
MONGODB_PASSWORD = os.environ.get("MONGODB_PASSWORD")

# Production options for MongoDB connection
MONGODB_OPTIONS = {
    "retryWrites": True,  # retry writes in case of network failures
    "w": "majority",  # wait for majority write acknowledgement
    "ssl": True,  # use SSL for secure connection
    "ssl_cert_reqs": "CERT_NONE",  # do not require SSL certificate validation
}

# Connect to MongoDB
client = MongoClient(
    MONGODB_URI, username=MONGODB_USERNAME, password=MONGODB_PASSWORD, **MONGODB_OPTIONS
)
db = client[MONGODB_DB]
short = db[MONGODB_COLLECTION]

collections = {"Short": db["Short"], "Medium": db["Medium"], "Macros": db["Macros"]}


@app.route("<collection>/<symbol>/rsi/<window>", methods=["GET"])
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

        # TODO make this reusable
        if collection not in collections:
            raise ValueError("Invalid collection")
        symbol = collections[collection].find_one({"symbol": symbol})
        if not symbol:
            raise ValueError("Invalid symbol")
        if not symbol["candles"] or len(symbol["candles"]) < window:
            raise ValueError("Not enough candles")


        dataframe = pd.DataFrame(list(symbol["candles"]))
        dataframe["rsi"] = rsi(close=dataframe["close"], window=window, fillna=True)
        return dataframe[["rsi", "datetime"]].to_json(orient="records")
    except Exception as e:
        return jsonify(error=str(e)), 500

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
