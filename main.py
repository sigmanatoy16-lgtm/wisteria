from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
DataFile = "counts.json"

def LoadCounts():
    if not os.path.exists(DataFile):
        return {}
    with open(DataFile, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def SaveCounts(counts):
    with open(DataFile, "w") as f:
        json.dump(counts, f, indent=2)

@app.route('/increment', methods=['POST'])
def Increment():
    userid = request.args.get('userid')
    if not userid:
        return jsonify({"error": "Missing 'userid' parameter"}), 400
    counts = LoadCounts()
    userid_str = str(userid)
    counts[userid_str] = counts.get(userid_str, 0) + 1
    SaveCounts(counts)
    sorted_users = sorted(
        [{"user": uid, "count": cnt} for uid, cnt in counts.items()],
        key=lambda x: x["count"],
        reverse=True
    )
    return jsonify(sorted_users)

@app.route('/list', methods=['GET'])
def ListCounts():
    counts = LoadCounts()
    sorted_users = sorted(
        [{"user": uid, "count": cnt} for uid, cnt in counts.items()],
        key=lambda x: x["count"],
        reverse=True
    )
    return jsonify(sorted_users)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
