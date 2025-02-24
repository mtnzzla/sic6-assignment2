from flask import Flask, request, make_response, jsonify
from datetime import datetime
from database import collection
from bson import json_util
import ujson

app = Flask(__name__)

@app.post('/distance')
def save_distance():
    data = request.get_json()
    if data:
        try:
            collection.insert_one({
                "value": data['distance'].get('value', 0),
                "status": data['distance']['context'].get('status', None),
                "timestamp": datetime.utcnow()
            })
            return jsonify({
                "success": True,
                "message": "Data terkirim!",
                "data": None
            })
        except IndexError:
            return jsonify({
                "success": False,
                "message": "Data invalid!",
                "data": None
            })
    else:
        return jsonify({
            "success": False,
            "message": "Data kosong!",
            "data": None
        })
    
@app.get("/distance")
def get_distance():
    data = collection.find()
    if data:
        return jsonify({
                "success": True,
                "message": "Respon sukses!",
                "data": ujson.loads(json_util.dumps(data, indent=4))
                })
    else:
        return jsonify({
            "success": False,
            "message": "Data kosong!",
            "data": None
        })

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")