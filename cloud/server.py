from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    data = request.json.get('data', [])
    print(f"Received data: {data}")
    # Here you can implement saving the data to a database or processing it
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
