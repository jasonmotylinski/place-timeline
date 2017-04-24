"""Main API."""
from datetime import datetime
from flask import Flask, jsonify, request
from elasticsearch import Elasticsearch
from flask_cors import CORS

app = Flask(__name__)

CORS(app)
es = Elasticsearch()


@app.route('/')
def default():
    """Default route."""
    start = datetime.fromtimestamp(float(request.args.get('start')))
    end = datetime.fromtimestamp(float(request.args.get('end')))
    query = {
        "query":
        {
            "range": {
                "doc.ts": {
                    "gte": start.isoformat(),
                    "lte": end.isoformat()
                }
            }
        },
        "sort": [
            {"doc.ts":{"order" : "asc"}}
        ],
        "size":10000
    }
    return jsonify(es.search(index="tile_placements", body=query)["hits"]["hits"])


if __name__ == "__main__":
    app.run(debug=True)
