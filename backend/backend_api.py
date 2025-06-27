from flask import Flask, request, jsonify
import numpy as np
import joblib
from ai_scheduling import fcfs, sjf, round_robin, extract_features, algo_names
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # <-- Add this line
model = joblib.load('scheduling_model.pkl')

@app.route('/schedule', methods=['POST'])
def schedule():
    tasks = request.json['tasks']
    fcfs_result = fcfs([t.copy() for t in tasks])
    sjf_result = sjf([t.copy() for t in tasks])
    rr_result = round_robin([t.copy() for t in tasks], quantum=2)
    features = extract_features(tasks)
    pred = model.predict(features)[0]
    return jsonify({
        'fcfs': fcfs_result,
        'sjf': sjf_result,
        'rr': rr_result,
        'ai_recommendation': algo_names[pred]
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')