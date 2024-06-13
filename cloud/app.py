from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# In-memory storage for received data (for demonstration purposes)
received_data = []

@app.route('/data', methods=['POST'])
def receive_data():
    data = request.get_json()
    if data:
        received_data.append(data)
        return jsonify({"message": "Data received successfully"}), 200
    else:
        return jsonify({"message": "No data received"}), 400

@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(received_data), 200

@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Real-Time Data Visualization</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <script>
            async function fetchData() {
                const response = await fetch('/data');
                const data = await response.json();
                const timestamps = data.map(entry => entry.timestamp);
                const measurements = data.map(entry => entry.measurements[0].distance);
                return { timestamps, measurements };
            }

            async function updateChart(chart) {
                const data = await fetchData();
                chart.data.labels = data.timestamps;
                chart.data.datasets[0].data = data.measurements;
                chart.update();
            }

            window.onload = async function() {
                const ctx = document.getElementById('myChart').getContext('2d');
                const chart = new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: [],
                        datasets: [{
                            label: 'Distance',
                            data: [],
                            borderColor: 'rgba(75, 192, 192, 1)',
                            borderWidth: 1
                        }]
                    },
                    options: {
                        scales: {
                            x: { display: true },
                            y: { display: true }
                        }
                    }
                });

                setInterval(() => updateChart(chart), 10000);
            }
        </script>
    </head>
    <body>
        <h1>Real-Time Data Visualization</h1>
        <canvas id="myChart" width="400" height="200"></canvas>
    </body>
    </html>
    ''')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
