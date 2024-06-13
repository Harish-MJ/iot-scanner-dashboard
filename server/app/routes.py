from flask import request, jsonify, current_app as app
from flask_socketio import emit
from . import db, socketio
from .models import LaserData
import json

@app.route('/api/data', methods=['POST'])
def store_data():
    data = request.get_json()
    if data:
        if isinstance(data, list):
            for entry in data:
                new_data = LaserData(
                    timestamp=entry['timestamp'],
                    measurements=json.dumps(entry['measurements'])
                )
                db.session.add(new_data)
                socketio.emit('new_data', {'timestamp': entry['timestamp'], 'measurements': entry['measurements']})
        else:
            new_data = LaserData(
                timestamp=data['timestamp'],
                measurements=json.dumps(data['measurements'])
            )
            db.session.add(new_data)
            socketio.emit('new_data', {'timestamp': data['timestamp'], 'measurements': data['measurements']})
        db.session.commit()
        return jsonify({"message": "Data received successfully"}), 200
    else:
        return jsonify({"message": "No data received"}), 400

@app.route('/api/data', methods=['GET'])
def get_data():
    data = LaserData.query.all()
    result = [
        {
            'timestamp': entry.timestamp,
            'measurements': json.loads(entry.measurements)
        } for entry in data
    ]
    return jsonify(result), 200
