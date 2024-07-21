from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Define the route for the webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    
    # Extract the necessary information from the incoming data
    index = data.get('Index')
    
    if index == 'NIFTY50':
        # Prepare the data to be sent to another API
        payload = {'index': index}
        
        # Send the data to another API
        response = requests.post('https://another-api-endpoint.com/data', json=payload)
        
        if response.status_code == 200:
            return jsonify({'status': 'success', 'message': 'Data sent successfully'}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Failed to send data'}), 500
    else:
        return jsonify({'status': 'error', 'message': 'Invalid data'}), 400

if __name__ == '__main__':
    app.run(port=5000, debug=True)
